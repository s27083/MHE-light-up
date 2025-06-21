from light_up import LightUpPuzzle
from optimization_algorithms import hill_climbing, simulated_annealing, tabu_search, genetic_algorithm, brute_force
from fixed_visualization import display_solution, get_illuminated_cells
import time

def main():
    # Przykładowa łamigłówka
    # -1: białe pole (puste)
    # -2: czarne pole bez numeru
    # 0-4: czarne pole z ograniczeniem liczbowym
    example_grid = [
        [-1, -1, -1, -1, -1, -1, -1],
        [-1,  1, -1, -2, -1,  0, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -2, -1,  2, -1, -2, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1,  3, -1, -2, -1,  1, -1],
        [-1, -1, -1, -1, -1, -1, -1],
    ]
    
    puzzle = LightUpPuzzle(example_grid)
    
    print("Początkowa siatka łamigłówki:")
    # Wyświetl siatkę używając tej samej reprezentacji co funkcja wyświetlająca rozwiązanie
    for i in range(puzzle.height):
        row = []
        for j in range(puzzle.width):
            if puzzle.grid[i, j] == -1:
                row.append('□')  # Białe pole
            elif puzzle.grid[i, j] == -2:
                row.append('■')  # Czarne pole bez numeru
            else:
                row.append(str(puzzle.grid[i, j]))  # Czarne pole z numerem
        print(' '.join(row))
    print()
    
    # Wygeneruj losowe początkowe rozwiązanie
    initial_solution = puzzle.random_solution()
    
    print("Losowe początkowe rozwiązanie:")
    display_solution(puzzle, initial_solution)
    
    initial_score = puzzle.objective_function(initial_solution)
    print(f"Wynik początkowego rozwiązania: {initial_score} (niższy jest lepszy, 0 jest idealne)\n")
    
    # Porównaj różne algorytmy optymalizacyjne
    algorithms = [
        ("Algorytm Pełnego Przeglądu", lambda initial, objective, get_neighbors, verbose: 
            brute_force(
                domain_generator=lambda: puzzle.get_domain(),
                objective_function=objective,
                max_bulbs=5,  # Ograniczamy liczbę żarówek do 5 dla wydajności
                max_combinations=10000,  # Ograniczamy liczbę kombinacji do 10000 dla wydajności
                verbose=verbose
            )
        ),
        ("Wspinaczka Górska", hill_climbing),
        ("Symulowane Wyżarzanie (Exponential + Uniform)", lambda initial, objective, get_neighbors, verbose: 
            simulated_annealing(
                initial,
                objective,
                get_neighbors,
                'exponential',  # annealing_schedule
                100.0,          # initial_temperature
                0.95,           # cooling_rate
                0.1,            # min_temperature
                10,             # iterations_per_temperature
                'uniform',      # sampling_method
                1.0,            # normal_sigma
                verbose
            )
        ),
        ("Symulowane Wyżarzanie (Linear + Normal)", lambda initial, objective, get_neighbors, verbose: 
            simulated_annealing(
                initial,
                objective,
                get_neighbors,
                'linear',        # annealing_schedule
                100.0,           # initial_temperature
                0.5,             # cooling_rate
                0.1,             # min_temperature
                10,              # iterations_per_temperature
                'normal',        # sampling_method
                0.5,             # normal_sigma
                verbose
            )
        ),
        ("Symulowane Wyżarzanie (Logarithmic + Normal)", lambda initial, objective, get_neighbors, verbose: 
            simulated_annealing(
                initial,
                objective,
                get_neighbors,
                'logarithmic',    # annealing_schedule
                100.0,            # initial_temperature
                0.1,              # cooling_rate
                0.1,              # min_temperature
                10,               # iterations_per_temperature
                'normal',         # sampling_method
                1.0,              # normal_sigma
                verbose
            )
        ),
        ("Symulowane Wyżarzanie (Boltzmann + Uniform)", lambda initial, objective, get_neighbors, verbose: 
            simulated_annealing(
                initial,
                objective,
                get_neighbors,
                'boltzmann',      # annealing_schedule
                100.0,            # initial_temperature
                0.1,              # cooling_rate
                0.1,              # min_temperature
                10,               # iterations_per_temperature
                'uniform',        # sampling_method
                1.0,              # normal_sigma
                verbose
            )
        ),
        ("Przeszukiwanie z Tabu", tabu_search),
        ("Algorytm Genetyczny (Uniform + Swap)", lambda initial, objective, get_neighbors, verbose: 
            genetic_algorithm(
                initial_population_size=50,
                objective_function=objective,
                random_solution_generator=lambda: puzzle.random_solution(),
                crossover_method='uniform',
                mutation_method='swap',
                termination_condition='iterations',
                max_iterations=1000,
                elite_size=5,
                verbose=verbose
            )
        ),
        ("Algorytm Genetyczny (One Point + Flip)", lambda initial, objective, get_neighbors, verbose: 
            genetic_algorithm(
                initial_population_size=50,
                objective_function=objective,
                random_solution_generator=lambda: puzzle.random_solution(),
                crossover_method='one_point',
                mutation_method='flip',
                termination_condition='iterations',
                max_iterations=1000,
                elite_size=5,
                verbose=verbose
            )
        )
    ]
    
    for name, algorithm in algorithms:
        print(f"\n=== {name} ===")
        start_time = time.time()
        
        # Uruchom algorytm optymalizacyjny
        if name == "Algorytm Pełnego Przeglądu":
            solution = algorithm(
                None,  # Ignorowany parametr initial_solution
                puzzle.objective_function,
                lambda sol: puzzle.get_neighbors(sol),
                True  # verbose
            )
        else:
            solution = algorithm(
                initial_solution,
                puzzle.objective_function,
                lambda sol: puzzle.get_neighbors(sol),
                True  # verbose
            )
        
        end_time = time.time()
        
        print(f"\nOstateczne rozwiązanie znalezione przez {name} w {end_time - start_time:.2f} sekundy:")
        display_solution(puzzle, solution)
        
        final_score = puzzle.objective_function(solution)
        print(f"Wynik końcowego rozwiązania: {final_score}")
        
        if final_score == 0:
            print("To jest idealne rozwiązanie!")
        else:
            print("To nie jest idealne rozwiązanie.")

if __name__ == "__main__":
    main()