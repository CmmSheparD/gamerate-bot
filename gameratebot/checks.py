def ensure_not_empty(s):
    if len(s) == 0:
        raise ValueError(f"Value of type {type(s)} is empty.")
    return s


def ensure_not_blanc(s: str) -> str:
    if ensure_not_empty(s).isspace():
        raise ValueError('String contains only whitespace characters.')
    return s
