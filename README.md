# MHE-light-up

# Light Up (Gra logiczna)

Light Up (znana również jako Akari) to rodzaj japońskiej łamigłówki logicznej, podobnej do Sudoku czy Nurikabe. Oto krótki opis:

## Zasady gry

1. Łamigłówka składa się z prostokątnej planszy z białymi i czarnymi polami.
2. Czarne pola mogą zawierać cyfry od 0 do 4 lub być puste.
3. Celem jest umieszczenie żarówek na niektórych białych polach w taki sposób, aby:
   - Każde białe pole było oświetlone przez co najmniej jedną żarówkę
   - Żarówki nie mogą się wzajemnie oświetlać
   - Liczba na czarnym polu wskazuje, ile żarówek musi być umieszczonych bezpośrednio obok niego (w pionie i poziomie)

## Właściwości oświetlenia

- Żarówka oświetla wszystkie białe pola w poziomie i pionie od miejsca, gdzie została umieszczona, aż do krawędzi planszy lub czarnego pola
- Żarówki nie mogą być umieszczane na czarnych polach
- Dwie żarówki nie mogą się wzajemnie oświetlać (być w tej samej linii poziomej lub pionowej bez czarnego pola między nimi)

## Podpowiedzi do rozwiązywania

- Czarne pola z liczbą 4 muszą mieć żarówki na wszystkich sąsiednich polach
- Czarne pola z liczbą 0 nie mogą mieć żadnych żarówek obok
- Czasem jedynym miejscem, które może być oświetlone, jest pole, na którym musi znajdować się żarówka

## Wizualizacja przykładowej planszy

```
┌───┬───┬───┬───┬───┐
│   │   │ ■ │   │   │
├───┼───┼───┼───┼───┤
│   │ ■ │ 1 │   │   │
├───┼───┼───┼───┼───┤
│ ■ │ 2 │   │ 0 │   │
├───┼───┼───┼───┼───┤
│   │   │   │ ■ │   │
├───┼───┼───┼───┼───┤
│   │   │ ■ │   │   │
└───┴───┴───┴───┴───┘
```

Gdzie:
- □ - białe pole (puste)
- ■ - czarne pole (bez liczby)
- 0,1,2,3,4 - czarne pole z liczbą
- 💡 - żarówka (w rozwiązaniu)

## Przykład rozwiązania

```
┌───┬───┬───┬───┬───┐
│💡 │   │ ■ │💡 │   │
├───┼───┼───┼───┼───┤
│   │ ■ │ 1 │   │   │
├───┼───┼───┼───┼───┤
│ ■ │ 2 │💡 │ 0 │   │
├───┼───┼───┼───┼───┤
│💡 │   │   │ ■ │💡 │
├───┼───┼───┼───┼───┤
│   │   │ ■ │   │   │
└───┴───┴───┴───┴───┘
```

Jest to ciekawa łamigłówka wymagająca logicznego myślenia i dedukcji, popularna w wielu zbiorach zagadek logicznych i aplikacjach z łamigłówkami.
