import time
import os
from light_up import LightUpPuzzle
from hill_climbing_variants import hill_climbing_deterministic, hill_climbing_random

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

# Ścieżka do pliku wynikowego
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hill_climbing_results.txt")

def write_to_file(text):
    """Zapisuje tekst do pliku wynikowego."""
    with open(output_file, "a") as f:
        f.write(text + "\n")

def main():
    # Usuń plik wynikowy, jeśli istnieje
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Inicjalizacja łamigłówki
    puzzle = LightUpPuzzle(example_grid)

    # Wygeneruj losowe początkowe rozwiązanie
    initial_solution = puzzle.random_solution()
    write_to_file("\nPoczątkowe losowe rozwiązanie:")
    # Zapisz rozwiązanie jako tekst
    solution_text = puzzle.get_solution_text(initial_solution)
    write_to_file(solution_text)
    initial_score = puzzle.objective_function(initial_solution)
    write_to_file(f"Wynik początkowego rozwiązania: {initial_score}")

    # Uruchom algorytm wspinaczkowy z deterministycznym wyborem sąsiada
    write_to_file("\n\nAlgorytm wspinaczkowy z deterministycznym wyborem sąsiada:")
    start_time = time.time()
    solution_deterministic = hill_climbing_deterministic(
        initial_solution=initial_solution,
        objective_function=puzzle.objective_function,
        get_neighbors=lambda sol: puzzle.get_neighbors(sol),
        verbose=False  # Wyłącz wyświetlanie postępów
    )
    det_time = time.time() - start_time

    write_to_file("\nRozwiązanie znalezione przez algorytm deterministyczny:")
    solution_text = puzzle.get_solution_text(solution_deterministic)
    write_to_file(solution_text)
    det_score = puzzle.objective_function(solution_deterministic)
    write_to_file(f"Wynik: {det_score}")
    write_to_file(f"Czas wykonania: {det_time:.2f} sekund")
    write_to_file(f"Czy rozwiązanie jest poprawne: {puzzle.is_valid_solution(solution_deterministic)}")

    # Uruchom algorytm wspinaczkowy z losowym wyborem sąsiada
    write_to_file("\n\nAlgorytm wspinaczkowy z losowym wyborem sąsiada:")
    start_time = time.time()
    solution_random = hill_climbing_random(
        initial_solution=initial_solution,
        objective_function=puzzle.objective_function,
        get_neighbors=lambda sol: puzzle.get_neighbors(sol),
        verbose=False  # Wyłącz wyświetlanie postępów
    )
    random_time = time.time() - start_time

    write_to_file("\nRozwiązanie znalezione przez algorytm z losowym wyborem:")
    solution_text = puzzle.get_solution_text(solution_random)
    write_to_file(solution_text)
    random_score = puzzle.objective_function(solution_random)
    write_to_file(f"Wynik: {random_score}")
    write_to_file(f"Czas wykonania: {random_time:.2f} sekund")
    write_to_file(f"Czy rozwiązanie jest poprawne: {puzzle.is_valid_solution(solution_random)}")

    # Porównanie wyników
    write_to_file("\n\nPorównanie wyników:")
    write_to_file(f"Algorytm deterministyczny: wynik = {det_score}, czas = {det_time:.2f} s")
    write_to_file(f"Algorytm z losowym wyborem: wynik = {random_score}, czas = {random_time:.2f} s")

    if det_score < random_score:
        write_to_file("Algorytm deterministyczny znalazł lepsze rozwiązanie.")
    elif random_score < det_score:
        write_to_file("Algorytm z losowym wyborem znalazł lepsze rozwiązanie.")
    else:
        write_to_file("Oba algorytmy znalazły rozwiązania o tym samym wyniku.")
    
    print(f"Wyniki zostały zapisane do pliku: {output_file}")

# Dodaj metodę do klasy LightUpPuzzle, która zwraca rozwiązanie jako tekst
def get_solution_text(self, solution):
    """Zwraca rozwiązanie jako tekst."""
    grid_text = ""
    for i in range(len(self.grid)):
        row = ""
        for j in range(len(self.grid[0])):
            cell = (i, j)
            if cell in solution:
                row += "💡 "
            elif self.grid[i][j] == -2:
                row += "■ "
            elif self.grid[i][j] >= 0:
                row += f"{self.grid[i][j]} "
            else:
                row += "-1 "
        grid_text += row.strip() + "\n"
    return grid_text

# Dodaj metodę do klasy LightUpPuzzle
LightUpPuzzle.get_solution_text = get_solution_text

# Uruchom główną funkcję
if __name__ == "__main__":
    main()