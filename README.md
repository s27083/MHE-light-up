# Light Up (Akari) Solver

## Opis

Program do rozwiązywania łamigłówki Light Up (Akari) przy użyciu różnych algorytmów optymalizacyjnych:

- Wspinaczka Górska (Hill Climbing)
- Symulowane Wyżarzanie (Simulated Annealing)
- Przeszukiwanie z Tabu (Tabu Search)
- Algorytm Genetyczny (Genetic Algorithm)
- Algorytm Pełnego Przeglądu (Brute Force)

## Zasady łamigłówki Light Up

1. Żarówki można umieszczać tylko na białych polach
2. Żarówki nie mogą się wzajemnie oświetlać (tzn. nie mogą znajdować się w tym samym wierszu lub kolumnie, chyba że oddziela je czarne pole)
3. Żarówka oświetla całą kolumnę i wiersz, aż do napotkania czarnego pola
4. Czarne pola mogą zawierać cyfry od 0 do 4, wskazujące liczbę żarówek, które muszą znajdować się w sąsiedztwie tego pola
5. Wszystkie białe pola muszą być oświetlone

## Wymagania

- Python 3.6 lub nowszy
- NumPy (`pip install numpy`)

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchamianie

Program można uruchomić z linii komend, podając różne parametry:

```bash
python main.py [opcje]
```

### Opcje

#### Wejście (wymagane, wzajemnie wykluczające się)

- `-f, --file PLIK` - Wczytaj siatkę łamigłówki z pliku
- `-i, --stdin` - Wczytaj siatkę łamigłówki ze standardowego wejścia

#### Algorytm

- `-a, --algorithm {hill,annealing,tabu,genetic,brute,all}` - Wybierz algorytm do użycia (domyślnie: wszystkie)
  - `hill` - Wspinaczka Górska
  - `annealing` - Symulowane Wyżarzanie
  - `tabu` - Przeszukiwanie z Tabu
  - `genetic` - Algorytm Genetyczny
  - `brute` - Algorytm Pełnego Przeglądu
  - `all` - wszystkie algorytmy

#### Wyjście

- `-o, --output PLIK` - Zapisz rozwiązanie do pliku
- `-v, --verbose` - Wyświetlaj szczegółowe informacje podczas działania algorytmu
- `--ascii` - Użyj znaków ASCII zamiast emoji do wyświetlania rozwiązania

#### Parametry algorytmów

- `--max-iterations LICZBA` - Maksymalna liczba iteracji dla algorytmów (domyślnie: 1000)
  - Używane przez: `hill`, `tabu`, `genetic`
- `--max-bulbs LICZBA` - Maksymalna liczba żarówek dla algorytmu pełnego przeglądu
  - Używane przez: `brute`
- `--max-combinations LICZBA` - Maksymalna liczba kombinacji dla algorytmu pełnego przeglądu (domyślnie: 1000000)
  - Używane przez: `brute`

## Format pliku wejściowego

Plik wejściowy powinien zawierać siatkę łamigłówki, gdzie każda linia reprezentuje jeden wiersz siatki, a wartości są oddzielone spacjami:

- `-1` - białe pole (puste)
- `-2` - czarne pole bez numeru
- `0-4` - czarne pole z ograniczeniem liczbowym

Przykład:

```
-1 -1 -1 -1 -1
-1 -2 -1 -2 -1
-1 -1  0 -1 -1
-1 -2 -1 -2 -1
-1 -1 -1 -1 -1
```

## Przykłady użycia

### Uruchomienie wszystkich algorytmów dla łamigłówki z pliku

```bash
python main.py -f example_puzzle.txt
```

### Uruchomienie tylko algorytmu wspinaczki górskiej

```bash
python main.py -f example_puzzle.txt -a hill
```

### Uruchomienie algorytmu pełnego przeglądu z ograniczeniem liczby żarówek

```bash
python main.py -f example_puzzle.txt -a brute --max-bulbs 5
```

### Uruchomienie algorytmu genetycznego z określoną liczbą iteracji

```bash
python main.py -f example_puzzle.txt -a genetic --max-iterations 500 -v
```

### Zapisanie rozwiązania do pliku

```bash
python main.py -f example_puzzle.txt -a annealing -o solution.json
```

### Wczytanie łamigłówki ze standardowego wejścia

```bash
python main.py -i
```

### Użycie znaków ASCII zamiast emoji

```bash
python main.py -f example_puzzle.txt --ascii
```

## Format pliku wyjściowego

Plik wyjściowy jest w formacie JSON i zawiera następujące informacje:

- `algorithm` - nazwa użytego algorytmu
- `execution_time` - czas wykonania algorytmu w sekundach
- `score` - wynik końcowego rozwiązania (0 oznacza idealne rozwiązanie)
- `solution` - lista współrzędnych żarówek w rozwiązaniu
- `grid` - oryginalna siatka łamigłówki

## Struktura projektu

- `main.py` - główny plik programu, obsługujący interfejs linii komend
- `light_up.py` - implementacja reprezentacji łamigłówki i jej głównych funkcji
- `optimization_algorithms.py` - implementacja algorytmów optymalizacyjnych
- `example.py` - przykładowe użycie implementacji na konkretnej łamigłówce (starsza wersja)
- `example_puzzle.txt` - przykładowa łamigłówka w formacie pliku wejściowego
- `requirements.txt` - lista zależności

