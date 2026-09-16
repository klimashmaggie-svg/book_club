from pathlib import Path

import storage
from models import Book, Club, Discussion, Member


def test_save_and_load_objects(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr(storage, "BOOKS_FILE", tmp_path / "books.json")
    monkeypatch.setattr(storage, "MEMBERS_FILE", tmp_path / "members.json")
    monkeypatch.setattr(
        storage,
        "DISCUSSIONS_FILE",
        tmp_path / "discussions.json",
    )
    monkeypatch.setattr(storage, "CLUBS_FILE", tmp_path / "clubs.json")

    member = Member(1, "Анна Климаш", "anna@example.com", "owner")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    discussion = Discussion(1, 1, book, member, "Главный конфликт")
    club = Club(1, "Клуб классики", "Читаем классику", [member], [book])
    club.discussions.append(discussion)

    storage.save_all([club], [member], [book], [discussion])
    clubs, members, books, discussions = storage.load_all()

    assert clubs[0].name == "Клуб классики"
    assert members[0].name == "Анна Климаш"
    assert books[0].title == "Преступление и наказание"
    assert discussions[0].book is books[0]
    assert discussions[0].author is members[0]
