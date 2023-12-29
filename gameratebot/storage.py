from datetime import date
from pymysql import connect
from pymysql.converters import escape_string

from util import get_close_matches_icase
from title import GameTitle

from config import db_name, db_user, db_socket, db_password


def _connect_to_db():
    return connect(unix_socket=db_socket, database=db_name, user=db_user,
                   password=db_password)


def get_user_accounts(tg_id):
    query = f'SELECT id, nickname FROM Users WHERE tg_id = {tg_id};'
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def add_user(tg_id, nickname=None):
    query = f'INSERT INTO Users (tg_id) VALUES ({tg_id});' \
        if nickname is None \
        else \
        f"INSERT INTO Users (tg_id, nickname) " \
        f"VALUES ({tg_id}, '{escape_string(nickname)}');"
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def add_title(title: GameTitle):
    query = f'INSERT INTO GameTitles ' \
            '(title, studio, director, release_date, posterID) ' \
            'VALUES (%s, %s, %s, %s, %s);'
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query, (title.title, title.studio, title.director,
                       title.release_date.isoformat(), title.poster_id))
        connection.commit()


def get_titles(*, title: str = None, studio: str = None, director: str = None,
               prior_to: date = None, after: date = None):
    filters = []
    if title is not None:
        filters.append(f"title LIKE '%{escape_string(title)}%'")
    if studio is not None:
        filters.append(f"studio = '{escape_string(studio)}'")
    if director is not None:
        filters.append(f"director = '{escape_string(director)}'")
    if prior_to is not None:
        filters.append(f"release_date <= '{prior_to}'")
    if after is not None:
        filters.append(f"release_date >= '{after}'")

    filters = ' AND '.join(filters)
    query = 'SELECT ' \
            'GameTitles.id, ' \
            'title, ' \
            'studio, ' \
            'director, ' \
            'release_date, '\
            'posterID, ' \
            'AVG(score) ' \
            'FROM GameTitles left join Reviews ' \
            'on GameTitles.id = Reviews.game ' \
            f'WHERE {filters} ' \
            'GROUP BY GameTitles.id;'
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return _map_db_title_entries(result)


def get_title_by_id(db_id: int):
    query = 'SELECT ' \
            'GameTitles.id, ' \
            'title, ' \
            'studio, ' \
            'director, ' \
            'release_date, ' \
            'posterID, ' \
            'AVG(score) ' \
            'FROM GameTitles left join Reviews ' \
            'on GameTitles.id = Reviews.game ' \
            f'WHERE GameTitles.id = {db_id};'
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return _map_db_title_entries(result)[0]


def match_title(candidate: str):
    """Find a matching title."""
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute('SELECT title FROM GameTitles;')
        titles = map(lambda entry: entry[0], cursor.fetchall())
    best_match = get_close_matches_icase(candidate, titles, 1)
#    return _storage[best_match[0]] if len(best_match) != 0 else None
    return get_titles(title=best_match[0])


def get_all_titles():
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM GameTitles;')
        result = cursor.fetchall()
    return _map_db_title_entries(result)


def _map_db_title_entries(entries):
    return tuple(map(lambda entry: GameTitle(*entry[1:], entry[0]), entries))


def add_review(title: int, user: int, score: int):
    query = 'INSERT INTO Reviews ' \
            '(user, game, score) ' \
            'VALUES (%s, %s, %s);'
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query, (user, title, score))
        connection.commit()


def get_reviews(*, title: int = None, user: int = None,
                fetch_text: bool = False):
    filters = []
    if title is not None:
        filters.append(f"game = {title}")
    if user is not None:
        filters.append(f"Users.tg_id = {user}")

    filters = ' AND '.join(filters)
    query = 'SELECT ' \
            'Reviews.id, ' \
            'user, ' \
            'game, ' \
            'score ' \
            'FROM Reviews ' \
            f'WHERE {filters};'
    if fetch_text:
        idx = query.find(' FROM')
        query = query[:idx] + ', review' + query[idx:]
    if user is not None:
        idx = query.find(' WHERE')
        query = query[:idx] + ' join Users on Users.id = Reviews.user' \
            + query[idx:]
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def update_review(title: int, user: int, score: int):
    query = 'UPDATE Reviews ' \
            'SET score = %s ' \
            'WHERE user = %s AND game = %s;'
    connection = _connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query, (score, user, title))
        connection.commit()
