# Flask – Aplikacja do wyszukiwania felg

## Opis projektu
Projekt zaliczeniowy z przedmiotu **Języki programowania**.  
Aplikacja webowa napisana we **Flasku**, umożliwiająca:

- logowanie użytkowników,
- przeglądanie listy felg zapisanych w bazie danych,
- wyszukiwanie felg po podstawowych parametrach,
- sortowanie wyników,
- obsługę błędów bazy danych.

Projekt skupia się na **logice w Pythonie**, a nie na rozbudowanym frontendzie.

---

## Funkcjonalności
- Logowanie i wylogowanie użytkownika (sesje Flask)
- Dostęp do aplikacji tylko dla zalogowanych
- Baza danych SQLite (`app.db`)
- Lista felg (marka, średnica, szerokość, PCD)
- Wyszukiwarka (marka, PCD)
- Sortowanie felg (algorytm bąbelkowy)
- Obsługa wyjątków (`try / except`)
- Programowanie obiektowe (klasa `Wheel`)

---

## Wykorzystane technologie
- Python 3
- Flask
- SQLite
- HTML + Bootstrap 5
- Jinja2