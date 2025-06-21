import random
from typing import Callable, TypeVar, List, Set, Tuple

T = TypeVar('T')

def hill_climbing_deterministic(
    initial_solution: T,
    objective_function: Callable[[T], int],
    get_neighbors: Callable[[T], List[T]],
    max_iterations: int = 1000,
    verbose: bool = False
) -> T:
    """
    Klasyczny algorytm wspinaczki górskiej z deterministycznym wyborem najlepszego sąsiada.
    
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

def hill_climbing_random(
    initial_solution: T,
    objective_function: Callable[[T], int],
    get_neighbors: Callable[[T], List[T]],
    max_iterations: int = 1000,
    verbose: bool = False
) -> T:
    """
    Algorytm wspinaczki górskiej z losowym wyborem sąsiada spośród lepszych sąsiadów.
    
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
    
    best_solution = current_solution
    best_score = current_score
    
    iteration = 0
    while iteration < max_iterations:
        neighbors = get_neighbors(current_solution)
        
        # Znajdź wszystkich lepszych sąsiadów
        better_neighbors = []
        
        for neighbor in neighbors:
            score = objective_function(neighbor)
            if score < current_score:
                better_neighbors.append((neighbor, score))
        
        # Jeśli nie ma lepszych sąsiadów, osiągnęliśmy lokalne optimum
        if not better_neighbors:
            if verbose:
                print(f"Zatrzymano na iteracji {iteration}: Brak lepszych sąsiadów")
            break
            
        # Losowo wybierz jednego z lepszych sąsiadów
        selected_neighbor, selected_score = random.choice(better_neighbors)
        
        # Przejdź do wybranego sąsiada
        current_solution = selected_neighbor
        current_score = selected_score
        
        # Aktualizuj najlepsze znalezione rozwiązanie
        if current_score < best_score:
            best_solution = current_solution
            best_score = current_score
        
        if verbose and iteration % 10 == 0:
            print(f"Iteracja {iteration}: wynik = {current_score}, najlepszy wynik = {best_score}")
            
        iteration += 1
        
        # Jeśli znaleźliśmy idealne rozwiązanie, zatrzymaj
        if current_score == 0:
            if verbose:
                print(f"Znaleziono idealne rozwiązanie w iteracji {iteration}")
            break
    
    if verbose:
        print(f"Końcowy wynik: {best_score}")
        
    return best_solution


