#!/usr/bin/env python3

import argparse
import sys
import time
import json
import numpy as np
from light_up import LightUpPuzzle
from optimization_algorithms import hill_climbing, simulated_annealing, tabu_search, genetic_algorithm, brute_force
from fixed_visualization import display_solution, get_illuminated_cells

def parse_grid_from_file(file_path):
    """
    Wczytuje siatkę łamigłówki z pliku.
    Format pliku: każda linia reprezentuje jeden wiersz siatki, wartości oddzielone spacjami.
    
    Przykład:
    -1 -1 -1 -1 -1
    -1 -2 -1 -2 -1
    -1 -1  0 -1 -1
    -1 -2 -1 -2 -1
    -1 -1 -1 -1 -1
    """
    with open(file_path, 'r') as file:
        grid = []
        for line in file:
            # Pomijamy puste linie i komentarze
            if line.strip() and not line.strip().startswith('#'):
                row = [int(val) for val in line.strip().split()]
                grid.append(row)
        return grid

def parse_grid_from_stdin():
    """
    Wczytuje siatkę łamigłówki ze standardowego wejścia.
    Format: każda linia reprezentuje jeden wiersz siatki, wartości oddzielone spacjami.
    Wczytywanie kończy się po napotkaniu pustej linii lub EOF.
    """
    print("Wprowadź siatkę łamigłówki (każdy wiersz w nowej linii, wartości oddzielone spacjami):")
    print("Zakończ wprowadzanie pustą linią lub Ctrl+D (EOF).")
    grid = []
    for line in sys.stdin:
        if not line.strip():
            break
        row = [int(val) for val in line.strip().split()]
        grid.append(row)
    return grid

def save_solution_to_file(solution, puzzle, file_path, algorithm_name, execution_time, score):
    """
    Zapisuje rozwiązanie do pliku w formacie JSON.
    """
    # Konwertuj zbiór krotek na listę list dla serializacji JSON
    solution_list = [[i, j] for i, j in solution]
    
    # Przygotuj dane do zapisu
    result = {
        "algorithm": algorithm_name,
        "execution_time": execution_time,
        "score": score,
        "solution": solution_list,
        "grid": puzzle.grid.tolist()
    }
    
    with open(file_path, 'w') as file:
        json.dump(result, file, indent=2)

def print_solution_ascii(solution, puzzle):
    """
    Wyświetla rozwiązanie w konsoli używając znaków ASCII zamiast emoji.
    """
    illuminated = get_illuminated_cells(puzzle, solution)
    
    for i in range(puzzle.height):
        row = []
        for j in range(puzzle.width):
            if (i, j) in solution:
                row.append('L')  # Żarówka (Lightbulb)
            elif puzzle.grid[i, j] >= -2:  # Czarne pole
                if puzzle.grid[i, j] == -2:
                    row.append('#')  # Czarne pole bez numeru
                else:
                    row.append(str(puzzle.grid[i, j]))  # Czarne pole z numerem
            elif (i, j) in illuminated:
                row.append('.')  # Oświetlone białe pole
            else:
                row.append('_')  # Nieoświetlone białe pole
        print(' '.join(row))
    print()

def main():
    # Konfiguracja parsera argumentów linii komend
    parser = argparse.ArgumentParser(description='Rozwiązywanie łamigłówki Light Up (Akari) przy użyciu różnych algorytmów optymalizacyjnych.')
    
    # Argumenty dotyczące wejścia
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', help='Ścieżka do pliku z siatką łamigłówki')
    input_group.add_argument('-i', '--stdin', action='store_true', help='Wczytaj siatkę łamigłówki ze standardowego wejścia')
    
    # Argumenty dotyczące algorytmu
    parser.add_argument('-a', '--algorithm', choices=['hill', 'annealing', 'tabu', 'genetic', 'brute', 'all'], 
                        default='all', help='Algorytm do użycia (domyślnie: wszystkie)')
    
    # Argumenty dotyczące wyjścia
    parser.add_argument('-o', '--output', help='Ścieżka do pliku wyjściowego dla rozwiązania')
    parser.add_argument('-v', '--verbose', action='store_true', help='Wyświetlaj szczegółowe informacje podczas działania algorytmu')
    parser.add_argument('--ascii', action='store_true', help='Użyj znaków ASCII zamiast emoji do wyświetlania rozwiązania')
    
    # Parametry dla algorytmów
    parser.add_argument('--max-iterations', type=int, default=1000, help='Maksymalna liczba iteracji dla algorytmów (domyślnie: 1000)')
    parser.add_argument('--max-bulbs', type=int, help='Maksymalna liczba żarówek dla algorytmu pełnego przeglądu')
    parser.add_argument('--max-combinations', type=int, default=1000000, help='Maksymalna liczba kombinacji dla algorytmu pełnego przeglądu')
    
    args = parser.parse_args()
    
    # Wczytaj siatkę łamigłówki
    if args.file:
        try:
            grid = parse_grid_from_file(args.file)
        except Exception as e:
            print(f"Błąd podczas wczytywania pliku: {e}")
            return 1
    else:  # args.stdin
        grid = parse_grid_from_stdin()
    
    # Sprawdź, czy siatka została poprawnie wczytana
    if not grid:
        print("Błąd: Pusta siatka łamigłówki.")
        return 1
    
    # Utwórz instancję łamigłówki
    puzzle = LightUpPuzzle(grid)
    
    # Wyświetl początkową siatkę
    print("Początkowa siatka łamigłówki:")
    for i in range(puzzle.height):
        row = []
        for j in range(puzzle.width):
            if puzzle.grid[i, j] == -1:
                row.append('_')  # Białe pole
            elif puzzle.grid[i, j] == -2:
                row.append('#')  # Czarne pole bez numeru
            else:
                row.append(str(puzzle.grid[i, j]))  # Czarne pole z numerem
        print(' '.join(row))
    print()
    
    # Wygeneruj losowe początkowe rozwiązanie
    initial_solution = puzzle.random_solution()
    
    print("Losowe początkowe rozwiązanie:")
    if args.ascii:
        print_solution_ascii(initial_solution, puzzle)
    else:
        display_solution(puzzle, initial_solution)
    
    initial_score = puzzle.objective_function(initial_solution)
    print(f"Wynik początkowego rozwiązania: {initial_score} (niższy jest lepszy, 0 jest idealne)\n")
    
    # Definicje algorytmów
    algorithms = {
        'hill': ("Wspinaczka Górska", lambda: hill_climbing(
            initial_solution=initial_solution,
            objective_function=puzzle.objective_function,
            get_neighbors=lambda sol: puzzle.get_neighbors(sol),
            max_iterations=args.max_iterations,
            verbose=args.verbose
        )),
        'annealing': ("Symulowane Wyżarzanie", lambda: simulated_annealing(
            initial_solution=initial_solution,
            objective_function=puzzle.objective_function,
            get_neighbors=lambda sol: puzzle.get_neighbors(sol),
            verbose=args.verbose
        )),
        'tabu': ("Przeszukiwanie z Tabu", lambda: tabu_search(
            initial_solution=initial_solution,
            objective_function=puzzle.objective_function,
            get_neighbors=lambda sol: puzzle.get_neighbors(sol),
            max_iterations=args.max_iterations,
            verbose=args.verbose
        )),
        'genetic': ("Algorytm Genetyczny", lambda: genetic_algorithm(
            initial_population_size=20,
            objective_function=puzzle.objective_function,
            random_solution_generator=lambda: puzzle.random_solution(),
            termination_condition='iterations',
            max_iterations=args.max_iterations,
            verbose=args.verbose
        )),
        'brute': ("Algorytm Pełnego Przeglądu", lambda: brute_force(
            domain_generator=lambda: puzzle.get_domain(),
            objective_function=puzzle.objective_function,
            max_bulbs=args.max_bulbs,
            max_combinations=args.max_combinations,
            verbose=args.verbose
        ))
    }
    
    # Wybierz algorytmy do uruchomienia
    if args.algorithm == 'all':
        selected_algorithms = algorithms.items()
    else:
        selected_algorithms = [(args.algorithm, algorithms[args.algorithm])]
    
    # Uruchom wybrane algorytmy
    for alg_key, (alg_name, alg_func) in selected_algorithms:
        print(f"\n=== {alg_name} ===\n")
        
        start_time = time.time()
        solution = alg_func()
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\nOstateczne rozwiązanie znalezione przez {alg_name} w {execution_time:.2f} sekundy:")
        
        if args.ascii:
            print_solution_ascii(solution, puzzle)
        else:
            display_solution(puzzle, solution)
        
        final_score = puzzle.objective_function(solution)
        print(f"Wynik końcowego rozwiązania: {final_score}")
        
        if final_score == 0:
            print("To jest idealne rozwiązanie!")
        else:
            print("To nie jest idealne rozwiązanie.")
        
        # Zapisz rozwiązanie do pliku, jeśli podano ścieżkę wyjściową
        if args.output:
            output_file = args.output
            if len(selected_algorithms) > 1:
                # Jeśli uruchamiamy wiele algorytmów, dodaj nazwę algorytmu do nazwy pliku
                name, ext = output_file.rsplit('.', 1) if '.' in output_file else (output_file, 'json')
                output_file = f"{name}_{alg_key}.{ext}"
            
            save_solution_to_file(solution, puzzle, output_file, alg_name, execution_time, final_score)
            print(f"Rozwiązanie zapisano do pliku: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())