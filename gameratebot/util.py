from difflib import get_close_matches
from typing import AnyStr, Iterable, List


def get_close_matches_icase(word: AnyStr,
                            possibilities: Iterable[AnyStr],
                            n: int = 3,
                            cutoff: float = 0.6) -> List[AnyStr]:
    """Case-ignorant wrapper for difflib.get_close_matches."""
    word = word.lower()
    uniform_to_original_map = {s.lower(): s for s in possibilities}
    return [uniform_to_original_map[uniform_match]
            for uniform_match in
            get_close_matches(word, uniform_to_original_map.keys(), n, cutoff)]
