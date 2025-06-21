import time
from light_up import LightUpPuzzle
from hill_climbing_variants import hill_climbing_deterministic, hill_climbing_random
from fixed_visualization import display_solution, get_illuminated_cells

# Przykładowa siatka łamigłówki Light Up
example_grid = [
    [-1, -1, -1, -1, -1, -1, -1],
    [-1, -2, -1, -2, -1, -2, -1],
    [-1, -1, -1, -1, -1, -1, -1],
    [-1, -2, -1, -2, -1, -2, -1],
    [-1, -1, -1, -1, -1, -1, -1],
    [-1, -2, -1, -2, -1, -2, -1],
    [-1, -1, -1, -1, -1, -1, -1]
]

def main():
    # Inicjalizacja łamigłówki
    puzzle = LightUpPuzzle(example_grid)

    # Wygeneruj losowe początkowe rozwiązanie
    initial_solution = puzzle.random_solution()
    print("\nPoczątkowe losowe rozwiązanie:")
    display_solution(puzzle, initial_solution)
    initial_score = puzzle.objective_function(initial_solution)
    print(f"Wynik początkowego rozwiązania: {initial_score}")

    # Uruchom algorytm wspinaczkowy z deterministycznym wyborem sąsiada
    print("\n\nAlgorytm wspinaczkowy z deterministycznym wyborem sąsiada:")
    start_time = time.time()
    solution_deterministic = hill_climbing_deterministic(
        initial_solution=initial_solution,
        objective_function=puzzle.objective_function,
        get_neighbors=lambda sol: puzzle.get_neighbors(sol),
        verbose=True
    )
    det_time = time.time() - start_time

    print("\nRozwiązanie znalezione przez algorytm deterministyczny:")
    display_solution(puzzle, solution_deterministic)
    det_score = puzzle.objective_function(solution_deterministic)
    print(f"Wynik: {det_score}")
    print(f"Czas wykonania: {det_time:.2f} sekund")
    print(f"Czy rozwiązanie jest poprawne: {puzzle.is_valid_solution(solution_deterministic)}")

    # Uruchom algorytm wspinaczkowy z losowym wyborem sąsiada
    print("\n\nAlgorytm wspinaczkowy z losowym wyborem sąsiada:")
    start_time = time.time()
    solution_random = hill_climbing_random(
        initial_solution=initial_solution,
        objective_function=puzzle.objective_function,
        get_neighbors=lambda sol: puzzle.get_neighbors(sol),
        verbose=True
    )
    random_time = time.time() - start_time

    print("\nRozwiązanie znalezione przez algorytm z losowym wyborem:")
    display_solution(puzzle, solution_random)
    random_score = puzzle.objective_function(solution_random)
    print(f"Wynik: {random_score}")
    print(f"Czas wykonania: {random_time:.2f} sekund")
    print(f"Czy rozwiązanie jest poprawne: {puzzle.is_valid_solution(solution_random)}")

    # Porównanie wyników
    print("\n\nPorównanie wyników:")
    print(f"Algorytm deterministyczny: wynik = {det_score}, czas = {det_time:.2f} s")
    print(f"Algorytm z losowym wyborem: wynik = {random_score}, czas = {random_time:.2f} s")

    if det_score < random_score:
        print("Algorytm deterministyczny znalazł lepsze rozwiązanie.")
    elif random_score < det_score:
        print("Algorytm z losowym wyborem znalazł lepsze rozwiązanie.")
    else:
        print("Oba algorytmy znalazły rozwiązania o tym samym wyniku.")

# Uruchom główną funkcję
if __name__ == "__main__":
    main()