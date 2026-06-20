# Domowa Biblioteka 2.0

Aplikacja webowa do zarządzania domową biblioteką. Pozwala śledzić książki, autorów oraz wypożyczenia.

## Funkcje

- Lista wszystkich książek ze statusem (na półce / wypożyczona)
- Dodawanie książek i autorów
- Relacja wiele-do-wielu: książka może mieć wielu autorów, autor wiele książek
- Wypożyczanie i zwracanie książek
- Historia wypożyczeń dla każdej książki

## Uruchomienie lokalne

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/arturmachura/learning-git-task.git
cd learning-git-task/13.4
```

### 2. Utwórz i aktywuj wirtualne środowisko

```bash
# Windows
py -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Zainicjuj bazę danych

```bash
flask db init
flask db migrate -m "initial"
flask db upgrade
```

### 5. Uruchom aplikację

```bash
flask run
```

Aplikacja działa pod adresem: http://127.0.0.1:5000

## Struktura projektu

```
13.4/
├── app/
│   ├── __init__.py      # inicjalizacja Flask, SQLAlchemy, Migrate
│   ├── models.py        # modele: Book, Author, Loan
│   ├── routes.py        # widoki i logika
│   └── templates/       # szablony HTML (Bootstrap 5)
├── config.py            # konfiguracja aplikacji
├── biblioteka.py        # punkt wejścia + shell context
├── requirements.txt
└── .flaskenv
```

## Model danych

- **Author** — imię i nazwisko
- **Book** — tytuł, rok, ISBN; powiązana z autorami (M2M)
- **Loan** — kto wypożyczył, kiedy, czy zwrócił

## Technologie

- Python 3, Flask, Flask-SQLAlchemy, Flask-Migrate
- SQLite
- Bootstrap 5
