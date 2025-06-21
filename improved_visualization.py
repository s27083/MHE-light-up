import os
import sys
import numpy as np
from light_up import LightUpPuzzle

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

# Bardziej złożona siatka z ograniczeniami liczbowymi
complex_grid = [
    [-1, -1, -1, -1, -1, -1, -1],
    [-1, 2, -1, -2, -1, 1, -1],
    [-1, -1, -1, -1, -1, -1, -1],
    [-1, -2, -1, 0, -1, -2, -1],
    [-1, -1, -1, -1, -1, -1, -1],
    [-1, 1, -1, -2, -1, 3, -1],
    [-1, -1, -1, -1, -1, -1, -1]
]

def get_illuminated_cells_manual(puzzle, solution):
    """
    Ręczna implementacja metody do znajdowania oświetlonych pól.
    """
    height, width = puzzle.grid.shape
    illuminated = set(solution)  # Żarówki są oświetlone
    
    # Dla każdej żarówki, znajdź pola, które oświetla
    for i, j in solution:
        # Góra
        r = i - 1
        while r >= 0 and puzzle.grid[r, j] == -1:
            illuminated.add((r, j))
            r -= 1
        
        # Dół
        r = i + 1
        while r < height and puzzle.grid[r, j] == -1:
            illuminated.add((r, j))
            r += 1
        
        # Lewo
        c = j - 1
        while c >= 0 and puzzle.grid[i, c] == -1:
            illuminated.add((i, c))
            c -= 1
        
        # Prawo
        c = j + 1
        while c < width and puzzle.grid[i, c] == -1:
            illuminated.add((i, c))
            c += 1
    
    return illuminated

def display_solution(puzzle, solution):
    """
    Wyświetla rozwiązanie łamigłówki Light Up w czytelnej formie.
    
    Legenda:
    - 💡: Żarówka
    - ■: Czarne pole bez numeru
    - 0-4: Czarne pole z ograniczeniem liczbowym
    - □: Nieoświetlone białe pole
    - ✓: Oświetlone białe pole
    """
    # Pobierz wszystkie oświetlone pola
    illuminated = get_illuminated_cells_manual(puzzle, solution)
    
    # Usuń żarówki z listy oświetlonych pól dla lepszej wizualizacji
    illuminated_without_bulbs = illuminated - set(solution)
    
    # Wyświetl informacje o liczbie pól
    print(f"Liczba żarówek: {len(solution)}")
    print(f"Liczba wszystkich oświetlonych pól: {len(illuminated)}")
    print(f"Liczba oświetlonych białych pól (bez żarówek): {len(illuminated_without_bulbs)}")
    
    # Wyświetl siatkę
    height, width = puzzle.grid.shape
    grid_text = ""
    for i in range(height):
        row = ""
        for j in range(width):
            cell = (i, j)
            if cell in solution:
                row += "💡 "  # Żarówka
            elif puzzle.grid[i, j] == -2:
                row += "■ "  # Czarne pole bez numeru
            elif puzzle.grid[i, j] >= 0:
                # Czarne pole z ograniczeniem liczbowym
                row += f"{puzzle.grid[i, j]} "
            elif cell in illuminated_without_bulbs:
                row += "✓ "  # Oświetlone białe pole
            else:
                row += "□ "  # Nieoświetlone białe pole
        grid_text += row.strip() + "\n"
    print(grid_text)

def main():
    # Wyczyść konsolę
    os.system('clear')
    
    # Wyłącz buforowanie wyjścia
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
    
    # Inicjalizacja łamigłówki z prostą siatką
    puzzle = LightUpPuzzle(example_grid)
    
    # Wygeneruj losowe początkowe rozwiązanie
    initial_solution = puzzle.random_solution()
    
    print("Przykład prostej siatki:")
    print("\nPoczątkowe losowe rozwiązanie (nowy format):")
    display_solution(puzzle, initial_solution)
    
    # Inicjalizacja łamigłówki ze złożoną siatką
    complex_puzzle = LightUpPuzzle(complex_grid)
    
    # Wygeneruj losowe początkowe rozwiązanie
    complex_solution = complex_puzzle.random_solution()
    
    print("\nPrzykład złożonej siatki z ograniczeniami liczbowymi:")
    print("\nPoczątkowe losowe rozwiązanie (nowy format):")
    display_solution(complex_puzzle, complex_solution)
    
    print("\nLegenda:")
    print("💡: Żarówka")
    print("■: Czarne pole bez numeru")
    print("0-4: Czarne pole z ograniczeniem liczbowym")
    print("□: Nieoświetlone białe pole")
    print("✓: Oświetlone białe pole")

if __name__ == "__main__":
    main()