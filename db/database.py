"""Подключение SQLite, создание схемы и выполнение именованных SQL-запросов."""

import sqlite3
from contextlib import closing
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "bookclub.sqlite"
SCHEMA_PATH = ROOT / "sql" / "schema.sql"
QUERIES_PATH = ROOT / "sql" / "queries.sql"


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Открыть существующую базу с именованными полями и проверкой связей."""
    path = Path(db_path) if db_path is not None else DB_PATH
    if not path.is_file():
        raise FileNotFoundError(
            f"База {path} не найдена. Выполните: python -m db.import_json"
        )
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path: Path | None = None) -> None:
    """Создать файл и таблицы; повторный запуск сохраняет имеющиеся данные."""
    path = Path(db_path) if db_path is not None else DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


@cache
def get_queries() -> dict[str, str]:
    """Прочитать запросы после меток -- name: из единого SQL-файла."""
    queries = {}
    name = None
    statement = ""
    for line in QUERIES_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("-- name:"):
            if name is not None:
                raise ValueError(f"Незавершённый SQL-запрос: {name}")
            name = line.removeprefix("-- name:").strip()
        elif name is not None:
            statement += line + "\n"
            # SQLite определяет конец команды, учитывая кавычки и комментарии.
            if sqlite3.complete_statement(statement):
                if name in queries:
                    raise ValueError(f"Повтор имени SQL-запроса: {name}")
                queries[name] = statement
                name, statement = None, ""
    if name is not None:
        raise ValueError(f"Незавершённый SQL-запрос: {name}")
    return queries


def fetch_all(name: str, parameters: tuple = ()) -> list[sqlite3.Row]:
    """Выполнить SELECT; значения передаются отдельно от текста SQL."""
    with closing(get_connection()) as connection:
        return connection.execute(get_queries()[name], parameters).fetchall()


def fetch_one(name: str, parameters: tuple = ()) -> sqlite3.Row | None:
    """Получить одну строку либо None; соединение закрывается после чтения."""
    with closing(get_connection()) as connection:
        return connection.execute(get_queries()[name], parameters).fetchone()
