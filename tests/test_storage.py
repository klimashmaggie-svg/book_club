"""Проверка сохранения новой объектной модели в JSON."""

from pathlib import Path

import storage
from models import Book, Club, Discussion, Member


def test_save_and_load_objects(tmp_path: Path, monkeypatch) -> None:
    """После загрузки клуб хранит обсуждение с книгой и участником."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr(storage, "BOOKS_FILE", tmp_path / "books.json")
    monkeypatch.setattr(storage, "MEMBERS_FILE", tmp_path / "members.json")
    monkeypatch.setattr(
        storage,
        "DISCUSSIONS_FILE",
        tmp_path / "discussions.json",
    )
    monkeypatch.setattr(storage, "CLUBS_FILE", tmp_path / "clubs.json")

    member = Member(1, "Полина Миронова", "polina@example.com")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    discussion = Discussion(1, member, book, "Сильный психологический роман.")
    club = Club(1, "Клуб классики", "Читаем классику", [discussion])

    storage.save_all([club], [member], [book], [discussion])
    clubs, members, books, discussions = storage.load_all()

    assert discussions[0].member is members[0]
    assert discussions[0].book is books[0]
    assert discussions[0].review == "Сильный психологический роман."
    assert clubs[0].discussions == [discussions[0]]
