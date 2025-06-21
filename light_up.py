import random
import numpy as np
from typing import List, Tuple, Set

class LightUpPuzzle:
    def __init__(self, grid: List[List[int]]):
        """
        Inicjalizacja łamigłówki Light Up.
        
        grid: tablica 2D gdzie:
         - -1 oznacza białe pole (puste)
         - -2 oznacza czarne pole bez numeru
         - 0-4 oznaczają czarne pola z odpowiednimi ograniczeniami liczbowymi
        """
        self.grid = np.array(grid)
        self.height, self.width = self.grid.shape
        self.white_cells = self._get_white_cells()
        
    def _get_white_cells(self) -> List[Tuple[int, int]]:
        """Zwraca współrzędne wszystkich białych pól na planszy."""
        white_cells = []
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i, j] == -1:
                    white_cells.append((i, j))
        return white_cells
        
    def get_domain(self) -> List[Tuple[int, int]]:
        """Zwraca listę wszystkich możliwych pozycji żarówek (białych pól) jako domenę dla algorytmu pełnego przeglądu."""
        return self.white_cells.copy()
    
    def random_solution(self) -> Set[Tuple[int, int]]:
        """Generuje losowe rozwiązanie (losowe rozmieszczenie żarówek na białych polach)."""
        # Umieszcza żarówki losowo na około 1/3 białych pól
        num_bulbs = max(1, len(self.white_cells) // 3)
        return set(random.sample(self.white_cells, num_bulbs))
    
    def get_neighbors(self, solution: Set[Tuple[int, int]], max_changes: int = 3) -> List[Set[Tuple[int, int]]]:
        """
        Generuje sąsiednie rozwiązania poprzez:
        1. Dodanie nowej żarówki
        2. Usunięcie istniejącej żarówki
        3. Przeniesienie żarówki (usunięcie jednej, dodanie innej)
        
        Zwraca listę sąsiednich rozwiązań.
        """
        neighbors = []
        
        # 1. Dodaje nową żarówkę (jeśli są dostępne białe pola)
        available_cells = set(self.white_cells) - solution
        if available_cells:
            for _ in range(min(max_changes, len(available_cells))):
                new_bulb = random.choice(list(available_cells))
                new_solution = solution.copy()
                new_solution.add(new_bulb)
                neighbors.append(new_solution)
                available_cells.remove(new_bulb)
        
        # 2. Usuwa istniejącą żarówkę (jeśli jakieś są)
        if solution:
            for _ in range(min(max_changes, len(solution))):
                remove_bulb = random.choice(list(solution))
                new_solution = solution.copy()
                new_solution.remove(remove_bulb)
                neighbors.append(new_solution)
        
        # 3. Przenosi żarówkę (usuwa jedną, dodaje inną)
        if solution and available_cells:
            for _ in range(max_changes):
                remove_bulb = random.choice(list(solution))
                add_bulb = random.choice(list(available_cells))
                
                new_solution = solution.copy()
                new_solution.remove(remove_bulb)
                new_solution.add(add_bulb)
                neighbors.append(new_solution)
        
        return neighbors
    
    def objective_function(self, solution: Set[Tuple[int, int]]) -> int:
        """
        Ocenia rozwiązanie na podstawie spełnienia ograniczeń i pokrycia.
        Niższy wynik jest lepszy (0 oznacza idealne rozwiązanie).
        
        Kary:
        1. Żarówki oświetlające się wzajemnie
        2. Czarne pola z numerami i nieprawidłową liczbą sąsiednich żarówek
        3. Nieoświetlone białe pola
        """
        penalty = 0
        
        # Tworzy mapę oświetlonych pól
        illuminated = self._get_illuminated_cells(solution)
        
        # 1. Kara za żarówki oświetlające się wzajemnie
        for bulb in solution:
            if self._count_illuminating_bulbs(bulb, solution) > 0:
                penalty += 100  # Wysoka kara za żarówki oświetlające się wzajemnie
        
        # 2. Kara za czarne pola numerowane z nieprawidłową liczbą sąsiednich żarówek
        for i in range(self.height):
            for j in range(self.width):
                if 0 <= self.grid[i, j] <= 4:  # Czarne pole z numerem
                    adjacent_bulbs = self._count_adjacent_bulbs((i, j), solution)
                    if adjacent_bulbs != self.grid[i, j]:
                        penalty += 50 * abs(adjacent_bulbs - self.grid[i, j])
        
        # 3. Kara za nieoświetlone białe pola
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i, j] == -1 and (i, j) not in illuminated:
                    penalty += 10
        
        return penalty
    
    def _get_illuminated_cells(self, solution: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """Zwraca wszystkie pola oświetlone przez żarówki w rozwiązaniu."""
        illuminated = set()
        
        for bulb in solution:
            i, j = bulb
            illuminated.add(bulb)  # Sama żarówka jest oświetlona
            
            # Oświetla we wszystkich czterech kierunkach aż do napotkania czarnego pola
            # Góra
            for r in range(i-1, -1, -1):
                if self.grid[r, j] >= -2:  # Napotkano czarne pole
                    break
                illuminated.add((r, j))
            
            # Dół
            for r in range(i+1, self.height):
                if self.grid[r, j] >= -2:  # Napotkano czarne pole
                    break
                illuminated.add((r, j))
            
            # Lewo
            for c in range(j-1, -1, -1):
                if self.grid[i, c] >= -2:  # Napotkano czarne pole
                    break
                illuminated.add((i, c))
            
            # Prawo
            for c in range(j+1, self.width):
                if self.grid[i, c] >= -2:  # Napotkano czarne pole
                    break
                illuminated.add((i, c))
        
        return illuminated
    
    def _count_illuminating_bulbs(self, bulb: Tuple[int, int], solution: Set[Tuple[int, int]]) -> int:
        """Liczy ile innych żarówek oświetla tę żarówkę."""
        i, j = bulb
        count = 0
        
        # Sprawdza we wszystkich czterech kierunkach aż do napotkania czarnego pola
        # Góra
        for r in range(i-1, -1, -1):
            if self.grid[r, j] >= -2:  # Napotkano czarne pole
                break
            if (r, j) in solution:
                count += 1
                break
        
        # Dół
        for r in range(i+1, self.height):
            if self.grid[r, j] >= -2:  # Napotkano czarne pole
                break
            if (r, j) in solution:
                count += 1
                break
        
        # Lewo
        for c in range(j-1, -1, -1):
            if self.grid[i, c] >= -2:  # Napotkano czarne pole
                break
            if (i, c) in solution:
                count += 1
                break
        
        # Prawo
        for c in range(j+1, self.width):
            if self.grid[i, c] >= -2:  # Napotkano czarne pole
                break
            if (i, c) in solution:
                count += 1
                break
        
        return count
    
    def _count_adjacent_bulbs(self, cell: Tuple[int, int], solution: Set[Tuple[int, int]]) -> int:
        """Liczy liczbę żarówek sąsiadujących z danym polem."""
        i, j = cell
        count = 0
        
        for ni, nj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= ni < self.height and 0 <= nj < self.width and (ni, nj) in solution:
                count += 1
        
        return count
    
    def is_valid_solution(self, solution: Set[Tuple[int, int]]) -> bool:
        """Sprawdza czy rozwiązanie jest poprawne (spełnia wszystkie ograniczenia)."""
        return self.objective_function(solution) == 0
    
    def print_solution(self, solution: Set[Tuple[int, int]]):
        """Wyświetla aktualny stan rozwiązania."""
        illuminated = self._get_illuminated_cells(solution)
        
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if (i, j) in solution:
                    row.append('💡')  # Żarówka
                elif self.grid[i, j] >= -2:  # Czarne pole
                    if self.grid[i, j] == -2:
                        row.append('■')  # Czarne pole bez numeru
                    else:
                        row.append(str(self.grid[i, j]))  # Czarne pole z numerem
                elif (i, j) in illuminated:
                    row.append('✓')  # Oświetlone białe pole
                else:
                    row.append('□')  # Nieoświetlone białe pole
            print(' '.join(row))
        print()