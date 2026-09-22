"""Проверки связей клуба с участниками, книгами и обсуждениями."""

import pytest

from models import Book, Club, Discussion, Member, add_club


def test_club_creation_and_string_representation() -> None:
    """Клуб хранит объекты участников и книг и показывает их число."""
    member = Member(1, "Наталья Федорова", "natalia@example.com", "owner")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    club = Club(1, "Клуб классики", "Читаем классику", [member], [book])

    assert club.id == 1
    assert club.members == [member]
    assert club.books == [book]
    assert "Клуб классики" in str(club)


def test_club_creates_discussion_with_linked_objects() -> None:
    """Обсуждение ссылается на книгу и автора из клуба."""
    member = Member(1, "Артем Козлов", "artem@example.com", "owner")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    club = Club(1, "Клуб классики", "Читаем классику")

    club.add_member(member)
    club.add_book(book)
    discussion = club.create_discussion(1, book, member, "Главный конфликт")

    assert discussion in club.discussions
    assert discussion.book is book
    assert discussion.author is member
    assert discussion.club_id == club.id


def test_discussion_adds_messages() -> None:
    """В сообщениях сохраняются имена разных участников и их текст."""
    member = Member(1, "Вера Соколова", "vera@example.com", "owner")
    second_member = Member(2, "Максим Егоров", "maxim@example.com")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    discussion = Discussion(1, 1, book, member, "Главный конфликт")

    discussion.add_message(member, "Начинаем обсуждение.")
    discussion.add_message(second_member, "Мне понравилась концовка.")

    assert discussion.messages == [
        "Вера Соколова: Начинаем обсуждение.",
        "Максим Егоров: Мне понравилась концовка.",
    ]


def test_club_does_not_duplicate_member() -> None:
    """Повторное добавление того же участника не создает копию."""
    member = Member(1, "Лидия Андреева", "lidia@example.com")
    club = Club(1, "Клуб классики", "Читаем классику")

    club.add_member(member)
    club.add_member(member)

    assert club.members == [member]


def test_club_contains_two_subclubs() -> None:
    """Основной клуб может хранить два других клуба как объекты."""
    club = Club(1, "Клуб классики", "Читаем классику")
    first = Club(2, "Клуб романов", "Читаем романы")
    second = Club(3, "Клуб фантастики", "Читаем фантастику")

    club.add_subclub(first)
    club.add_subclub(second)

    assert club.subclubs == [first, second]
    assert club.to_data()["subclub_ids"] == [2, 3]


def test_discussion_requires_member_in_club() -> None:
    """Посторонний участник не может создать обсуждение клуба."""
    member = Member(1, "Петр Васильев", "petr@example.com")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    club = Club(1, "Клуб классики", "Читаем классику", books=[book])

    with pytest.raises(ValueError, match="club member"):
        club.create_discussion(1, book, member, "Главный конфликт")


def test_discussion_requires_book_in_club() -> None:
    """Обсуждение нельзя создать для книги вне списка клуба."""
    member = Member(1, "Юлия Тихонова", "yulia@example.com", "owner")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    club = Club(1, "Клуб классики", "Читаем классику", [member])

    with pytest.raises(ValueError):
        club.create_discussion(1, book, member, "Главный конфликт")


def test_add_club() -> None:
    """Функция создает клуб и добавляет его в коллекцию."""
    clubs: list[Club] = []

    club = add_club(clubs, "Современная проза", "Обсуждаем новые книги")

    assert club in clubs
    assert club.id == 1
