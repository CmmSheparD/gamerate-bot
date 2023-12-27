from typing import Union
from datetime import date

from checks import ensure_not_blanc


class GameTitle:
    def __init__(self, title: str, studio: str, director: str,
                 release_date: Union[date, str], poster_id: str,
                 average_score: float = None, db_id: int = None):
        self.title = ensure_not_blanc(title)
        self.studio = ensure_not_blanc(studio)
        self.director = ensure_not_blanc(director)
        if isinstance(release_date, str):
            self.release_date = date.fromisoformat(release_date)
        else:
            self.release_date = release_date
        self.poster_id = ensure_not_blanc(poster_id)
        self.average_score = average_score
        self.db_id = db_id


class GameTitleBuilder:
    def __init__(self):
        self.title = None
        self.studio = None
        self.director = None
        self.release_date = None
        self.poster_id = None
        self.average_score = None

    def set_title(self, title: str):
        self.title = ensure_not_blanc(title)

    def set_studio(self, studio: str):
        self.studio = ensure_not_blanc(studio)

    def set_director(self, director: str):
        self.director = ensure_not_blanc(director)

    def set_release_date(self, release_date: Union[date, str]):
        if isinstance(release_date, str):
            self.release_date = date.fromisoformat(release_date)
        else:
            self.release_date = release_date

    def set_poster_id(self, poster_id: str):
        self.poster_id = ensure_not_blanc(poster_id)

    def set_average_score(self, average_score):
        self.average_score = average_score

    def finalize(self):
        """Return built GameTitle and reset builder object."""
        instance = GameTitle(self.title, self.studio, self.director,
                             self.release_date, self.poster_id,
                             self.average_score)
        self.title = None
        self.studio = None
        self.director = None
        self.release_date = None
        self.poster_id = None
        self.average_score = None
        return instance
