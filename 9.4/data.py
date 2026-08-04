from library import Movie, Series


def load_initial_data(library):
    movies = [
        Movie("Kiler", 1997, "Komedia"),
        Movie("Seksmisja", 1984, "Komedia"),
        Movie("Miś", 1981, "Komedia"),
        Movie("Bogowie", 2014, "Dramat"),
        Movie("Kler", 2018, "Dramat"),
        Movie("Kurier", 2019, "Thriller"),
        Movie("Broad Peak", 2022, "Dramat"),
    ]
    library.extend(movies)

    series_seasons = [
        ("Ranczo", 2006, "Komedia", 1, 13),
        ("Wataha", 2014, "Kryminał", 1, 6),
        ("Ślepnąc od świateł", 2018, "Kryminał", 1, 6),
        ("Rojst", 2018, "Kryminał", 1, 6),
        ("Wielka woda", 2022, "Dramat", 1, 6),
        ("Belfer", 2016, "Kryminał", 1, 10),
    ]
    for title, year, genre, season, episodes in series_seasons:
        for ep in range(1, episodes + 1):
            library.append(Series(title, year, genre, season=season, episode=ep))
