"""ПР7: целостность SQLite, импорт JSON и результаты SQL-запросов."""

import json
import sqlite3
from contextlib import closing

import pytest

from db.database import (
    ROOT,
    fetch_all,
    fetch_one,
    get_connection,
    get_queries,
    initialize_database,
)
from db.import_json import import_data


def test_import_preserves_ids_and_links(sqlite_db):
    assert fetch_one("book_totals")["books_count"] == 7
    assert dict(fetch_one("community_totals")) == {
        "members_count": 5, "clubs_count": 3, "discussions_count": 3,
    }
    row = fetch_one("discussion", (1,))
    assert isinstance(row, sqlite3.Row)
    assert row["book_id"] == 1
    assert row["member_id"] == 1
    assert row["book_title"] == "Преступление и наказание"
    assert [row["id"] for row in fetch_all("discussions", (2,))] == [2]
    with closing(get_connection()) as connection:
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []


def test_repeated_import_preserves_updates_and_new_rows(sqlite_db):
    with closing(get_connection()) as connection:
        with connection:
            connection.execute("UPDATE books SET title = 'Изменено' WHERE id = 1")
            connection.execute("INSERT INTO books VALUES (99, 'Новая', 'Автор', 2020)")
    counts = import_data(db_path=sqlite_db)
    assert counts["books"] == 8
    assert counts["club_discussions"] == 3
    assert fetch_one("book", (1,))["title"] == "Изменено"
    import_data(db_path=sqlite_db, update_existing=True)
    assert fetch_one("book", (1,))["title"] == "Преступление и наказание"
    assert fetch_one("book", (99,))["title"] == "Новая"


def test_failed_import_rolls_back_every_change(sqlite_db, tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    for name in ("books", "members", "clubs", "discussions"):
        data = json.loads((ROOT / "data" / f"{name}.json").read_text())
        if name == "books":
            data[0]["title"] = "Не должно сохраниться"
        if name == "discussions":
            data[0]["book_id"] = 12345
        (source / f"{name}.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(sqlite3.IntegrityError):
        import_data(data_dir=source, db_path=sqlite_db, update_existing=True)
    assert fetch_one("book", (1,))["title"] == "Преступление и наказание"
    assert len(fetch_all("discussions", (None,))) == 3


def test_schema_foreign_keys_and_duplicate_links(sqlite_db):
    initialize_database(sqlite_db)
    with closing(get_connection()) as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("INSERT INTO club_discussions VALUES (1, 1)")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("INSERT INTO club_discussions VALUES (999, 1)")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM books WHERE id = 1")


def test_all_documented_queries_execute(sqlite_db):
    """Каждый запрос из SQL-каталога проверяется с нужным числом параметров."""
    parameters = {
        "books": (), "members": (), "search_books": ("", None),
        "members_by_role": ("reader",), "discussions": (None,),
        "book_discussions": (1,), "book_totals": (), "community_totals": (),
        "book_statistics": (0,), "clubs": (), "unreviewed_books": (1, ""),
        "book": (1,), "member": (1,), "club": (1,), "discussion": (1,),
        "member_discussions": (1,), "featured_discussions": (3, 0),
        "member_statistics": (),
    }
    assert set(get_queries()) == set(parameters)
    for name, values in parameters.items():
        assert fetch_all(name, values)


def test_statistics_include_zero_and_correct_counts(sqlite_db):
    books = {row["id"]: row["discussion_count"]
             for row in fetch_all("book_statistics", (0,))}
    assert books == {1: 1, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1, 7: 0}
    assert len(fetch_all("book_statistics", (1,))) == 3
    assert fetch_all("book_statistics", (2,)) == []
    assert fetch_all("featured_discussions", (1, 1))[0]["id"] == 2


def test_missing_database_does_not_create_empty_file(tmp_path):
    path = tmp_path / "missing.sqlite"
    with pytest.raises(FileNotFoundError, match="db.import_json"):
        get_connection(path)
    assert not path.exists()
