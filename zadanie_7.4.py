import random
from datetime import date


class Media:
    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre
        self.plays = 0

    def play(self):
        self.plays += 1


class Movie(Media):
    def __str__(self):
        return f"{self.title} ({self.year})"


class Series(Media):
    def __init__(self, title, year, genre, season, episode):
        super().__init__(title, year, genre)
        self.season = season
        self.episode = episode

    def __str__(self):
        return f"{self.title} S{self.season:02d}E{self.episode:02d}"


def get_movies(library):
    return sorted([item for item in library if isinstance(item, Movie)], key=lambda x: x.title)


def get_series(library):
    return sorted([item for item in library if isinstance(item, Series)], key=lambda x: x.title)


def search(library, title):
    return [item for item in library if item.title.lower() == title.lower()]


def generate_views(library):
    item = random.choice(library)
    item.plays += random.randint(1, 100)


def run_generate_views(library, times=10):
    for _ in range(times):
        generate_views(library)


def top_titles(library, count=5, content_type=None):
    if content_type == Movie:
        filtered = get_movies(library)
    elif content_type == Series:
        filtered = get_series(library)
    else:
        filtered = list(library)
    return sorted(filtered, key=lambda x: x.plays, reverse=True)[:count]


def add_season(library, title, year, genre, season, episodes_count):
    for episode in range(1, episodes_count + 1):
        library.append(Series(title, year, genre, season=season, episode=episode))


def count_episodes(library, title):
    return sum(1 for item in library if isinstance(item, Series) and item.title.lower() == title.lower())


if __name__ == "__main__":
    print("Biblioteka filmów")

    library = [
        Movie("Kiler", 1997, "Komedia"),
        Movie("Seksmisja", 1984, "Komedia"),
        Movie("Miś", 1981, "Komedia"),
        Movie("Bogowie", 2014, "Dramat"),
        Movie("Kler", 2018, "Dramat"),
        Movie("Kurier", 2019, "Thriller"),
        Movie("25 lat niewinności. Sprawa Tomka Komendy", 2020, "Dramat"),
        Movie("Broad Peak", 2022, "Dramat"),
    ]
    add_season(library, "Ranczo", 2006, "Komedia", season=1, episodes_count=13)
    add_season(library, "Wataha", 2014, "Kryminał", season=1, episodes_count=6)
    add_season(library, "Ślepnąc od świateł", 2018, "Kryminał", season=1, episodes_count=6)
    add_season(library, "Rojst", 2018, "Kryminał", season=1, episodes_count=6)
    add_season(library, "Wielka woda", 2022, "Dramat", season=1, episodes_count=6)
    add_season(library, "Sexify", 2021, "Komedia", season=1, episodes_count=8)
    add_season(library, "Belfer", 2016, "Kryminał", season=1, episodes_count=10)

    run_generate_views(library)

    today = date.today().strftime("%d.%m.%Y")
    print(f"Najpopularniejsze filmy i seriale dnia {today}")

    for t in top_titles(library, count=3):
        print(f"{t} | odtworzenia: {t.plays}")
