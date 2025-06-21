import random
from typing import Callable, TypeVar, List, Set, Tuple, Dict, Any, FrozenSet

T = TypeVar('T')

def tabu_search_enhanced(
    initial_solution: Set[Tuple[int, int]],
    objective_function: Callable[[Set[Tuple[int, int]]], int],
    get_neighbors: Callable[[Set[Tuple[int, int]]], List[Set[Tuple[int, int]]]],
    tabu_list_size: int = 10,
    unlimited_tabu: bool = False,
    max_iterations: int = 1000,
    max_iterations_without_improvement: int = 100,
    backtracking: bool = False,
    verbose: bool = False
) -> Set[Tuple[int, int]]:
    """
    Rozszerzony algorytm przeszukiwania z tabu, który unika ponownego odwiedzania niedawno zbadanych rozwiązań.
    Obsługuje nieograniczony rozmiar listy tabu oraz mechanizm cofania się do ostatniego punktu roboczego.
    
    Argumenty:
        initial_solution: Rozwiązanie początkowe
        objective_function: Funkcja do minimalizacji
        get_neighbors: Funkcja generująca sąsiadów rozwiązania
        tabu_list_size: Rozmiar listy tabu (ignorowany, gdy unlimited_tabu=True)
        unlimited_tabu: Czy używać nieograniczonej listy tabu
        max_iterations: Maksymalna liczba iteracji
        max_iterations_without_improvement: Maksymalna liczba iteracji bez poprawy przed cofnięciem
        backtracking: Czy używać mechanizmu cofania się do ostatniego punktu roboczego
        verbose: Czy wyświetlać postępy
        
    Zwraca:
        Najlepsze znalezione rozwiązanie
    """
    current_solution = initial_solution
    current_score = objective_function(current_solution)
    
    best_solution = current_solution
    best_score = current_score
    
    # Dla Light Up używamy zamrożonych zbiorów (frozenset) dla listy tabu, ponieważ zbiory nie są hashowalne
    tabu_set = set()  # Zbiór zamrożonych zbiorów dla szybszego wyszukiwania
    tabu_list = []    # Lista zamrożonych zbiorów dla zachowania kolejności (gdy nie unlimited_tabu)
    
    # Lista punktów roboczych (rozwiązań, z których można kontynuować obliczenia)
    # Każdy punkt roboczy to krotka (rozwiązanie, wynik, iteracja)
    working_points = []
    
    iterations_without_improvement = 0
    iteration = 0
    
    while iteration < max_iterations:
        neighbors = get_neighbors(current_solution)
        
        # Odfiltruj sąsiadów znajdujących się na liście tabu
        non_tabu_neighbors = [n for n in neighbors if frozenset(n) not in tabu_set]
        
        # Jeśli mamy sąsiadów, którzy nie są na liście tabu
        if non_tabu_neighbors:
            # Znajdź najlepszego sąsiada nie będącego na liście tabu
            best_neighbor = None
            best_neighbor_score = float('inf')
            
            for neighbor in non_tabu_neighbors:
                score = objective_function(neighbor)
                
                # Kryterium aspiracji: akceptuj ruch tabu, jeśli prowadzi do nowego globalnego najlepszego
                if score < best_score or (best_neighbor is None or score < best_neighbor_score):
                    best_neighbor = neighbor
                    best_neighbor_score = score
            
            # Sprawdź, czy znaleźliśmy punkt roboczy (sąsiad lepszy od obecnego rozwiązania)
            if best_neighbor_score < current_score and backtracking:
                working_points.append((current_solution, current_score, iteration))
            
            # Aktualizuj bieżące rozwiązanie
            current_solution = best_neighbor
            current_score = best_neighbor_score
            
            # Aktualizuj najlepsze rozwiązanie jeśli potrzeba
            if current_score < best_score:
                best_solution = current_solution
                best_score = current_score
                iterations_without_improvement = 0
                
                if best_score == 0:
                    if verbose:
                        print(f"Znaleziono idealne rozwiązanie w iteracji {iteration}")
                    break
            else:
                iterations_without_improvement += 1
        else:
            # Jeśli wszyscy sąsiedzi są na liście tabu
            if backtracking and working_points:
                # Cofnij się do ostatniego punktu roboczego
                if verbose:
                    print(f"Iteracja {iteration}: Wszystkie ruchy na liście tabu, cofam się do punktu roboczego")
                
                # Wybierz ostatni punkt roboczy
                current_solution, current_score, working_point_iteration = working_points.pop()
                
                # Wyczyść listę tabu dla ruchów po punkcie roboczym
                if unlimited_tabu:
                    # Jeśli używamy nieograniczonej listy tabu, usuwamy tylko ruchy po punkcie roboczym
                    tabu_set = set(t for t, it in tabu_set if it <= working_point_iteration)
                else:
                    # Jeśli używamy ograniczonej listy tabu, po prostu ją czyścimy
                    tabu_set.clear()
                    tabu_list.clear()
                
                iterations_without_improvement = 0
            else:
                # Jeśli nie ma punktów roboczych lub nie używamy cofania, po prostu kontynuuj
                iterations_without_improvement += 1
        
        # Sprawdź, czy należy się cofnąć z powodu braku poprawy
        if backtracking and iterations_without_improvement >= max_iterations_without_improvement and working_points:
            if verbose:
                print(f"Iteracja {iteration}: Brak poprawy przez {iterations_without_improvement} iteracji, cofam się do punktu roboczego")
            
            # Wybierz ostatni punkt roboczy
            current_solution, current_score, working_point_iteration = working_points.pop()
            
            # Wyczyść listę tabu dla ruchów po punkcie roboczym
            if unlimited_tabu:
                # Jeśli używamy nieograniczonej listy tabu, usuwamy tylko ruchy po punkcie roboczym
                new_tabu_set = set()
                for t in tabu_set:
                    if isinstance(t, tuple) and len(t) == 2 and isinstance(t[1], int) and t[1] <= working_point_iteration:
                        new_tabu_set.add(t)
                tabu_set = new_tabu_set
            else:
                # Jeśli używamy ograniczonej listy tabu, po prostu ją czyścimy
                tabu_set.clear()
                tabu_list.clear()
            
            iterations_without_improvement = 0
        
        # Aktualizuj listę tabu
        frozen_solution = frozenset(current_solution)
        if unlimited_tabu:
            tabu_set.add((frozen_solution, iteration))
        else:
            tabu_set.add(frozen_solution)
            tabu_list.append(frozen_solution)
            if len(tabu_list) > tabu_list_size:
                removed = tabu_list.pop(0)
                tabu_set.remove(removed)
        
        if verbose and iteration % 10 == 0:
            print(f"Iteracja {iteration}: Najlepszy wynik = {best_score}, Bieżący wynik = {current_score}, Rozmiar listy tabu = {len(tabu_set)}")
        
        iteration += 1
    
    if verbose:
        print(f"Końcowy najlepszy wynik: {best_score}")
        print(f"Liczba iteracji: {iteration}")
        print(f"Rozmiar listy tabu: {len(tabu_set)}")
    
    return best_solution

# Przykład użycia dla problemu Light Up:
"""
Przykład użycia:

from light_up import LightUpPuzzle
from tabu_search_variants import tabu_search_enhanced

# Inicjalizacja łamigłówki
puzzle = LightUpPuzzle(example_grid)

# Wygeneruj losowe początkowe rozwiązanie
initial_solution = puzzle.random_solution()

# Uruchom algorytm tabu z ograniczonym rozmiarem listy tabu
solution_limited = tabu_search_enhanced(
    initial_solution=initial_solution,
    objective_function=puzzle.objective_function,
    get_neighbors=lambda sol: puzzle.get_neighbors(sol),
    tabu_list_size=10,
    unlimited_tabu=False,
    backtracking=False,
    verbose=True
)

# Uruchom algorytm tabu z nieograniczonym rozmiarem listy tabu
solution_unlimited = tabu_search_enhanced(
    initial_solution=initial_solution,
    objective_function=puzzle.objective_function,
    get_neighbors=lambda sol: puzzle.get_neighbors(sol),
    unlimited_tabu=True,
    backtracking=False,
    verbose=True
)

# Uruchom algorytm tabu z mechanizmem cofania się
solution_backtracking = tabu_search_enhanced(
    initial_solution=initial_solution,
    objective_function=puzzle.objective_function,
    get_neighbors=lambda sol: puzzle.get_neighbors(sol),
    tabu_list_size=10,
    unlimited_tabu=False,
    backtracking=True,
    verbose=True
)
"""