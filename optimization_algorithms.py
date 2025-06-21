import random
import math
import time
import itertools
from typing import Callable, Set, Tuple, TypeVar, List, Dict, Any

T = TypeVar('T')

def hill_climbing(
    initial_solution: T,
    objective_function: Callable[[T], int],
    get_neighbors: Callable[[T], List[T]],
    max_iterations: int = 1000,
    verbose: bool = False
) -> T:
    """
    Prosty algorytm wspinaczki górskiej, który zawsze przechodzi do lepszego sąsiada.
    
    Argumenty:
        initial_solution: Rozwiązanie początkowe
        objective_function: Funkcja do minimalizacji
        get_neighbors: Funkcja generująca sąsiadów rozwiązania
        max_iterations: Maksymalna liczba iteracji
        verbose: Czy wyświetlać postępy
        
    Zwraca:
        Najlepsze znalezione rozwiązanie
    """
    current_solution = initial_solution
    current_score = objective_function(current_solution)
    
    iteration = 0
    while iteration < max_iterations:
        neighbors = get_neighbors(current_solution)
        
        # Znajdź najlepszego sąsiada
        best_neighbor = None
        best_neighbor_score = float('inf')
        
        for neighbor in neighbors:
            score = objective_function(neighbor)
            if score < best_neighbor_score:
                best_neighbor = neighbor
                best_neighbor_score = score
        
        # Jeśli nie ma poprawy, osiągnęliśmy lokalne optimum
        if best_neighbor_score >= current_score:
            if verbose:
                print(f"Zatrzymano na iteracji {iteration}: Brak poprawy")
            break
            
        # Przejdź do najlepszego sąsiada
        current_solution = best_neighbor
        current_score = best_neighbor_score
        
        if verbose and iteration % 10 == 0:
            print(f"Iteracja {iteration}: wynik = {current_score}")
            
        iteration += 1
        
        # Jeśli znaleźliśmy idealne rozwiązanie, zatrzymaj
        if current_score == 0:
            if verbose:
                print(f"Znaleziono idealne rozwiązanie w iteracji {iteration}")
            break
    
    if verbose:
        print(f"Końcowy wynik: {current_score}")
        
    return current_solution

def simulated_annealing(
    initial_solution: T,
    objective_function: Callable[[T], int],
    get_neighbors: Callable[[T], List[T]],
    annealing_schedule: str = 'exponential',
    initial_temperature: float = 100.0,
    cooling_rate: float = 0.95,
    min_temperature: float = 0.1,
    iterations_per_temperature: int = 10,
    sampling_method: str = 'uniform',
    normal_sigma: float = 1.0,
    verbose: bool = False
) -> T:
    """
    Algorytm symulowanego wyżarzania, który może uciec z lokalnych optimów.
    
    Argumenty:
        initial_solution: Rozwiązanie początkowe
        objective_function: Funkcja do minimalizacji
        get_neighbors: Funkcja generująca sąsiadów rozwiązania
        annealing_schedule: Schemat wyżarzania ('exponential', 'linear', 'logarithmic', 'boltzmann')
        initial_temperature: Temperatura początkowa
        cooling_rate: Współczynnik chłodzenia
        min_temperature: Minimalna temperatura przed zatrzymaniem
        iterations_per_temperature: Liczba iteracji dla każdej temperatury
        sampling_method: Metoda losowania sąsiada ('uniform', 'normal')
        normal_sigma: Odchylenie standardowe dla rozkładu normalnego (używane tylko gdy sampling_method='normal')
        verbose: Czy wyświetlać postępy
        
    Zwraca:
        Najlepsze znalezione rozwiązanie
    """
    current_solution = initial_solution
    current_score = objective_function(current_solution)
    
    best_solution = current_solution
    best_score = current_score
    
    temperature = initial_temperature
    iteration = 0
    start_time = time.time()
    
    # Funkcje schematów wyżarzania
    def exponential_cooling(t, alpha):
        return t * alpha
    
    def linear_cooling(t, alpha, initial_t):
        return initial_t - alpha * iteration
    
    def logarithmic_cooling(t, alpha, initial_t):
        return initial_t / (1 + alpha * math.log(1 + iteration))
    
    def boltzmann_cooling(t, alpha, initial_t):
        return initial_t / (1 + alpha * math.log(1 + iteration))
    
    # Funkcja do wyboru sąsiada z rozkładu normalnego
    def select_neighbor_normal(neighbors, current_solution, sigma=normal_sigma):
        if not neighbors:
            return None
        
        # Oblicz "odległości" między sąsiadami a bieżącym rozwiązaniem
        # W przypadku zbioru żarówek, odległość to liczba różnych elementów
        distances = []
        for neighbor in neighbors:
            # Dla zbiorów, odległość to suma elementów, które są w jednym zbiorze, ale nie w drugim
            distance = len(neighbor.symmetric_difference(current_solution))
            distances.append(distance)
        
        # Normalizuj odległości
        if max(distances) > 0:
            normalized_distances = [d / max(distances) for d in distances]
        else:
            normalized_distances = [1.0 for _ in distances]
        
        # Oblicz wagi na podstawie rozkładu normalnego
        weights = [math.exp(-(d**2) / (2 * sigma**2)) for d in normalized_distances]
        
        # Normalizuj wagi, aby sumowały się do 1
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        else:
            # Jeśli wszystkie wagi są zerowe, użyj rozkładu jednostajnego
            weights = [1.0 / len(neighbors) for _ in neighbors]
        
        # Wybierz sąsiada na podstawie wag
        return random.choices(neighbors, weights=weights, k=1)[0]
    
    while temperature > min_temperature:
        for _ in range(iterations_per_temperature):
            neighbors = get_neighbors(current_solution)
            if not neighbors:
                continue
            
            # Wybierz sąsiada zgodnie z wybraną metodą losowania
            if sampling_method == 'normal':
                next_solution = select_neighbor_normal(neighbors, current_solution)
                if next_solution is None:
                    continue
            else:  # uniform
                next_solution = random.choice(neighbors)
            
            next_score = objective_function(next_solution)
            
            # Oblicz prawdopodobieństwo akceptacji
            delta = next_score - current_score
            
            # Zawsze akceptuj lepsze rozwiązania, czasami akceptuj gorsze
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_solution = next_solution
                current_score = next_score
                
                # Aktualizuj najlepsze rozwiązanie jeśli potrzeba
                if current_score < best_score:
                    best_solution = current_solution
                    best_score = current_score
                    
                    if best_score == 0:
                        if verbose:
                            print(f"Znaleziono idealne rozwiązanie w iteracji {iteration}")
                        return best_solution
        
        # Aktualizuj temperaturę zgodnie z wybranym schematem wyżarzania
        if annealing_schedule == 'linear':
            temperature = linear_cooling(temperature, cooling_rate, initial_temperature)
        elif annealing_schedule == 'logarithmic':
            temperature = logarithmic_cooling(temperature, cooling_rate, initial_temperature)
        elif annealing_schedule == 'boltzmann':
            temperature = boltzmann_cooling(temperature, cooling_rate, initial_temperature)
        else:  # exponential (domyślny)
            temperature = exponential_cooling(temperature, cooling_rate)
        
        iteration += 1
        
        if verbose and iteration % 5 == 0:
            elapsed_time = time.time() - start_time
            print(f"Iteracja {iteration}: Temperatura = {temperature:.4f}, Najlepszy wynik = {best_score}, Czas: {elapsed_time:.2f}s")
    
    if verbose:
        elapsed_time = time.time() - start_time
        print(f"Końcowy najlepszy wynik: {best_score}")
        print(f"Liczba iteracji: {iteration}")
        print(f"Czas wykonania: {elapsed_time:.2f} sekund")
    
    return best_solution 

def genetic_algorithm(
    initial_population_size: int,
    objective_function: Callable[[T], int],
    random_solution_generator: Callable[[], T],
    crossover_method: str = 'uniform',
    mutation_method: str = 'swap',
    termination_condition: str = 'iterations',
    max_iterations: int = 100,
    max_time_seconds: int = 60,
    mutation_rate: float = 0.2,
    elite_size: int = 2,
    tournament_size: int = 3,
    verbose: bool = False
) -> T:
    """
    Algorytm genetyczny dla problemu Light Up.
    
    Argumenty:
        initial_population_size: Rozmiar początkowej populacji
        objective_function: Funkcja do minimalizacji
        random_solution_generator: Funkcja generująca losowe rozwiązanie
        crossover_method: Metoda krzyżowania ('uniform' lub 'one_point')
        mutation_method: Metoda mutacji ('swap' lub 'flip')
        termination_condition: Warunek zakończenia ('iterations' lub 'time')
        max_iterations: Maksymalna liczba iteracji
        max_time_seconds: Maksymalny czas wykonania w sekundach
        mutation_rate: Prawdopodobieństwo mutacji
        elite_size: Liczba najlepszych osobników przechodzących bez zmian do następnej generacji
        tournament_size: Rozmiar turnieju w selekcji turniejowej
        verbose: Czy wyświetlać postępy
        
    Zwraca:
        Najlepsze znalezione rozwiązanie
    """
    # Generuj początkową populację
    population = [random_solution_generator() for _ in range(initial_population_size)]
    
    # Ocena początkowej populacji
    fitness_scores = [objective_function(individual) for individual in population]
    
    # Znajdź najlepszego osobnika
    best_individual = population[fitness_scores.index(min(fitness_scores))]
    best_score = min(fitness_scores)
    
    # Inicjalizacja zmiennych dla warunku zakończenia
    iteration = 0
    start_time = time.time()
    
    # Główna pętla algorytmu
    while True:
        # Sprawdź warunek zakończenia
        if termination_condition == 'iterations' and iteration >= max_iterations:
            break
        elif termination_condition == 'time' and (time.time() - start_time) >= max_time_seconds:
            break
        
        # Selekcja - używamy selekcji turniejowej
        selected_individuals = []
        for _ in range(initial_population_size - elite_size):
            tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
            winner = min(tournament, key=lambda x: x[1])[0]
            selected_individuals.append(winner)
        
        # Elityzm - zachowaj najlepszych osobników
        elite_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i])[:elite_size]
        elite_individuals = [population[i] for i in elite_indices]
        
        # Nowa populacja
        new_population = elite_individuals.copy()
        
        # Krzyżowanie i mutacja
        while len(new_population) < initial_population_size:
            # Wybierz rodziców
            parent1 = random.choice(selected_individuals)
            parent2 = random.choice(selected_individuals)
            
            # Krzyżowanie
            if crossover_method == 'uniform':
                child = _uniform_crossover(parent1, parent2)
            else:  # one_point
                child = _one_point_crossover(parent1, parent2)
            
            # Mutacja
            if random.random() < mutation_rate:
                if mutation_method == 'swap':
                    child = _swap_mutation(child, random_solution_generator)
                else:  # flip
                    child = _flip_mutation(child, random_solution_generator)
            
            new_population.append(child)
        
        # Aktualizuj populację
        population = new_population
        
        # Ocena nowej populacji
        fitness_scores = [objective_function(individual) for individual in population]
        
        # Aktualizuj najlepszego osobnika
        current_best_score = min(fitness_scores)
        if current_best_score < best_score:
            best_score = current_best_score
            best_individual = population[fitness_scores.index(best_score)]
            
            if best_score == 0:
                if verbose:
                    print(f"Znaleziono idealne rozwiązanie w iteracji {iteration}")
                break
        
        if verbose and iteration % 5 == 0:
            print(f"Iteracja {iteration}: Najlepszy wynik = {best_score}")
        
        iteration += 1
    
    if verbose:
        print(f"Końcowy najlepszy wynik: {best_score}")
        print(f"Liczba iteracji: {iteration}")
        print(f"Czas wykonania: {time.time() - start_time:.2f} sekund")
    
    return best_individual

def _uniform_crossover(parent1: Set[Tuple[int, int]], parent2: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """
    Krzyżowanie równomierne - każdy element ma 50% szans na pochodzenie od każdego z rodziców.
    """
    child = set()
    
    # Dodaj elementy, które są w obu rodzicach
    common_elements = parent1.intersection(parent2)
    child.update(common_elements)
    
    # Dla elementów, które są tylko w jednym rodzicu, dodaj je z 50% prawdopodobieństwem
    only_parent1 = parent1 - parent2
    only_parent2 = parent2 - parent1
    
    for element in only_parent1:
        if random.random() < 0.5:
            child.add(element)
    
    for element in only_parent2:
        if random.random() < 0.5:
            child.add(element)
    
    return child

def _one_point_crossover(parent1: Set[Tuple[int, int]], parent2: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """
    Krzyżowanie jednopunktowe - konwertuje zbiory na listy, wybiera punkt podziału i łączy elementy.
    """
    # Konwersja zbiorów na posortowane listy dla deterministycznego krzyżowania
    parent1_list = sorted(list(parent1))
    parent2_list = sorted(list(parent2))
    
    # Wybierz punkt podziału
    if not parent1_list or not parent2_list:
        # Jeśli któryś z rodziców jest pusty, zwróć kopię drugiego
        return parent1.copy() if parent1 else parent2.copy()
    
    # Wybierz punkt podziału
    crossover_point = random.randint(0, max(len(parent1_list), len(parent2_list)))
    
    # Stwórz dziecko
    child_list = []
    
    # Dodaj elementy od pierwszego rodzica do punktu podziału
    if crossover_point <= len(parent1_list):
        child_list.extend(parent1_list[:crossover_point])
    else:
        child_list.extend(parent1_list)
    
    # Dodaj elementy od drugiego rodzica od punktu podziału
    if crossover_point <= len(parent2_list):
        child_list.extend(parent2_list[crossover_point:])
    
    # Konwersja z powrotem na zbiór, aby usunąć duplikaty
    return set(child_list)

def _swap_mutation(solution: Set[Tuple[int, int]], random_solution_generator: Callable[[], T]) -> Set[Tuple[int, int]]:
    """
    Mutacja przez zamianę - usuwa losowy element i dodaje nowy losowy element.
    """
    mutated = solution.copy()
    
    # Jeśli rozwiązanie jest puste, dodaj losowy element
    if not mutated:
        random_solution = random_solution_generator()
        if random_solution:
            mutated.add(next(iter(random_solution)))
        return mutated
    
    # Usuń losowy element
    element_to_remove = random.choice(list(mutated))
    mutated.remove(element_to_remove)
    
    # Dodaj nowy losowy element (z losowego rozwiązania)
    random_solution = random_solution_generator()
    if random_solution:
        # Wybierz element, którego nie ma jeszcze w rozwiązaniu
        potential_elements = [e for e in random_solution if e not in mutated]
        if potential_elements:
            mutated.add(random.choice(potential_elements))
    
    return mutated

def _flip_mutation(solution: Set[Tuple[int, int]], random_solution_generator: Callable[[], T]) -> Set[Tuple[int, int]]:
    """
    Mutacja przez odwrócenie - z pewnym prawdopodobieństwem usuwa lub dodaje elementy.
    """
    mutated = solution.copy()
    
    # Generuj losowe rozwiązanie, aby uzyskać potencjalne elementy do dodania
    random_solution = random_solution_generator()
    all_potential_elements = set(random_solution)
    
    # Dla każdego elementu w rozwiązaniu, z pewnym prawdopodobieństwem usuń go
    elements_to_remove = []
    for element in mutated:
        if random.random() < 0.2:  # 20% szans na usunięcie
            elements_to_remove.append(element)
    
    for element in elements_to_remove:
        mutated.remove(element)
    
    # Dla każdego potencjalnego elementu, z pewnym prawdopodobieństwem dodaj go
    potential_elements = all_potential_elements - mutated
    for element in potential_elements:
        if random.random() < 0.1:  # 10% szans na dodanie
            mutated.add(element)
    
    return mutated

def tabu_search(
    initial_solution: T,
    objective_function: Callable[[T], int],
    get_neighbors: Callable[[T], List[T]],
    tabu_list_size: int = 10,
    max_iterations: int = 1000,
    verbose: bool = False
) -> T:
    """
    Algorytm przeszukiwania z tabu, który unika ponownego odwiedzania niedawno zbadanych rozwiązań.
    
    Argumenty:
        initial_solution: Rozwiązanie początkowe
        objective_function: Funkcja do minimalizacji
        get_neighbors: Funkcja generująca sąsiadów rozwiązania
        tabu_list_size: Rozmiar listy tabu
        max_iterations: Maksymalna liczba iteracji
        verbose: Czy wyświetlać postępy
        
    Zwraca:
        Najlepsze znalezione rozwiązanie
    """
    current_solution = initial_solution
    current_score = objective_function(current_solution)
    
    best_solution = current_solution
    best_score = current_score
    
    # Dla Light Up używamy prostej listy tabu rozwiązań
    # Dla bardziej złożonych problemów można użyć atrybutów ruchu
    tabu_list = []
    
    iteration = 0
    while iteration < max_iterations:
        neighbors = get_neighbors(current_solution)
        
        # Odfiltruj sąsiadów znajdujących się na liście tabu
        non_tabu_neighbors = [n for n in neighbors if n not in tabu_list]
        
        if not non_tabu_neighbors:
            # Jeśli wszyscy sąsiedzi są na liście tabu, możemy pominąć lub użyć kryterium aspiracji
            # Tutaj po prostu przechodzimy do następnej iteracji
            iteration += 1
            continue
            
        # Znajdź najlepszego sąsiada nie będącego na liście tabu
        best_neighbor = None
        best_neighbor_score = float('inf')
        
        for neighbor in non_tabu_neighbors:
            score = objective_function(neighbor)
            
            # Kryterium aspiracji: akceptuj ruch tabu, jeśli prowadzi do nowego globalnego najlepszego
            if score < best_score or score < best_neighbor_score:
                best_neighbor = neighbor
                best_neighbor_score = score
        
        # Aktualizuj bieżące rozwiązanie
        current_solution = best_neighbor
        current_score = best_neighbor_score
        
        # Aktualizuj najlepsze rozwiązanie jeśli potrzeba
        if current_score < best_score:
            best_solution = current_solution
            best_score = current_score
            
            if best_score == 0:
                if verbose:
                    print(f"Znaleziono idealne rozwiązanie w iteracji {iteration}")
                break
        
        # Aktualizuj listę tabu (dodaj nowe rozwiązanie i usuń najstarsze jeśli potrzeba)
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)
            
        if verbose and iteration % 10 == 0:
            print(f"Iteracja {iteration}: Najlepszy wynik = {best_score}")
            
        iteration += 1
    
    if verbose:
        print(f"Końcowy najlepszy wynik: {best_score}")
        
    return best_solution


def brute_force(
    domain_generator: Callable[[], List[Tuple[int, int]]],
    objective_function: Callable[[Set[Tuple[int, int]]], int],
    max_bulbs: int = None,
    max_combinations: int = 1000000,
    verbose: bool = False
) -> Set[Tuple[int, int]]:
    """
    Algorytm pełnego przeglądu, który sprawdza wszystkie możliwe kombinacje żarówek.
    
    Argumenty:
        domain_generator: Funkcja zwracająca listę wszystkich możliwych pozycji żarówek (białych pól)
        objective_function: Funkcja do minimalizacji
        max_bulbs: Maksymalna liczba żarówek do rozważenia (jeśli None, sprawdza wszystkie możliwe liczby)
        max_combinations: Maksymalna liczba kombinacji do sprawdzenia (zabezpieczenie przed zbyt dużą liczbą kombinacji)
        verbose: Czy wyświetlać postępy
        
    Zwraca:
        Najlepsze znalezione rozwiązanie
    """
    # Pobierz wszystkie możliwe pozycje żarówek (białe pola)
    all_positions = domain_generator()
    
    best_solution = set()
    best_score = float('inf')
    
    # Określ maksymalną liczbę żarówek do rozważenia
    if max_bulbs is None:
        max_bulbs = len(all_positions)
    else:
        max_bulbs = min(max_bulbs, len(all_positions))
    
    total_combinations = 0
    combinations_checked = 0
    
    # Dla każdej możliwej liczby żarówek
    for num_bulbs in range(max_bulbs + 1):
        # Oblicz liczbę kombinacji dla tej liczby żarówek
        num_combinations = math.comb(len(all_positions), num_bulbs)
        total_combinations += num_combinations
        
        if verbose:
            print(f"Sprawdzanie {num_combinations} kombinacji dla {num_bulbs} żarówek...")
        
        # Jeśli przekroczymy maksymalną liczbę kombinacji, przerwij
        if total_combinations > max_combinations:
            if verbose:
                print(f"Przekroczono maksymalną liczbę kombinacji ({max_combinations}). Przerywanie...")
            break
        
        # Generuj wszystkie kombinacje dla tej liczby żarówek
        for combination in itertools.combinations(all_positions, num_bulbs):
            solution = set(combination)
            score = objective_function(solution)
            combinations_checked += 1
            
            # Aktualizuj najlepsze rozwiązanie jeśli potrzeba
            if score < best_score:
                best_solution = solution
                best_score = score
                
                if verbose:
                    print(f"Znaleziono lepsze rozwiązanie: {best_score}")
                
                # Jeśli znaleźliśmy idealne rozwiązanie, możemy zakończyć
                if best_score == 0:
                    if verbose:
                        print(f"Znaleziono idealne rozwiązanie po sprawdzeniu {combinations_checked} kombinacji")
                    return best_solution
            
            # Co jakiś czas wyświetl postęp
            if verbose and combinations_checked % 10000 == 0:
                print(f"Sprawdzono {combinations_checked} kombinacji. Najlepszy wynik: {best_score}")
    
    if verbose:
        print(f"Sprawdzono {combinations_checked} z {total_combinations} możliwych kombinacji")
        print(f"Końcowy najlepszy wynik: {best_score}")
    
    return best_solution