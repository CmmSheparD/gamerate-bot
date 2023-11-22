from checks import ensure_not_blanc


class GameTitle:
    def __init__(self, title: str, poster_id: str):
        self.title = ensure_not_blanc(title)
        self.poster_id = ensure_not_blanc(poster_id)


class GameTitleBuilder:
    def __init__(self):
        self.title = None
        self.poster_id = None

    def set_title(self, title: str):
        self.title = ensure_not_blanc(title)

    def set_poster_id(self, poster_id: str):
        self.poster_id = ensure_not_blanc(poster_id)

    def finalize(self):
        """Return built GameTitle and reset builder object."""
        instance = GameTitle(self.title, self.poster_id)
        self.title = None
        self.poster_id = None
        return instance
