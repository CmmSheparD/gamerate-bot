from checks import ensure_not_blanc


class GameTitle:
    def __init__(self, title: str, studio: str, director: str,
                 release_year: int, poster_id: str):
        self.title = ensure_not_blanc(title)
        self.studio = ensure_not_blanc(studio)
        self.director = ensure_not_blanc(director)
        self.release_year = release_year
        self.poster_id = ensure_not_blanc(poster_id)


class GameTitleBuilder:
    def __init__(self):
        self.title = None
        self.studio = None
        self.director = None
        self.release_year = None
        self.poster_id = None

    def set_title(self, title: str):
        self.title = ensure_not_blanc(title)

    def set_studio(self, studio: str):
        self.studio = ensure_not_blanc(studio)

    def set_director(self, director: str):
        self.director = ensure_not_blanc(director)

    def set_release_year(self, release_year: int):
        self.release_year = release_year

    def set_poster_id(self, poster_id: str):
        self.poster_id = ensure_not_blanc(poster_id)

    def finalize(self):
        """Return built GameTitle and reset builder object."""
        instance = GameTitle(self.title, self.studio, self.director,
                             self.release_year, self.poster_id)
        self.title = None
        self.studio = None
        self.director = None
        self.release_year = None
        self.poster_id = None
        return instance
