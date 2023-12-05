from util import get_close_matches_icase
from title import GameTitle


_storage = {}


def add_title(title: GameTitle):
    _storage[title.title] = title


def get_title(title: str):
    return _storage.get(title)


def match_title(candidate: str):
    title = _storage.get(candidate)
    if title is None:
        best_match = get_close_matches_icase(candidate, _storage.keys(), 1)
        title = _storage[best_match[0]] if len(best_match) != 0 else None
    return title


def get_all():
    return tuple(_storage.values())
