class Media:
    _next_id = 1

    def __init__(self, title, year, genre):
        self.id = Media._next_id
        Media._next_id += 1
        self.title = title
        self.year = year
        self.genre = genre
        self.plays = 0

    def play(self):
        self.plays += 1

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "genre": self.genre,
            "plays": self.plays,
        }


class Movie(Media):
    def __str__(self):
        return f"{self.title} ({self.year})"

    def to_dict(self):
        return {**super().to_dict(), "type": "movie"}


class Series(Media):
    def __init__(self, title, year, genre, season, episode):
        super().__init__(title, year, genre)
        self.season = season
        self.episode = episode

    def __str__(self):
        return f"{self.title} S{self.season:02d}E{self.episode:02d}"

    def to_dict(self):
        return {
            **super().to_dict(),
            "type": "series",
            "season": self.season,
            "episode": self.episode,
        }
