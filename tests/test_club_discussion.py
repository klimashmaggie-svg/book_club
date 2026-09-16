import pytest

from models import Book, Club, Discussion, Member, add_club


def test_club_creation_and_string_representation() -> None:
    member = Member(1, "Анна Климаш", "anna@example.com", "owner")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    club = Club(1, "Клуб классики", "Читаем классику", [member], [book])

    assert club.id == 1
    assert club.members == [member]
    assert club.books == [book]
    assert "Клуб классики" in str(club)


def test_club_creates_discussion_with_linked_objects() -> None:
    member = Member(1, "Анна Климаш", "anna@example.com", "owner")
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
    member = Member(1, "Анна Климаш", "anna@example.com", "owner")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    discussion = Discussion(1, 1, book, member, "Главный конфликт")

    discussion.add_message(member, "Начинаем обсуждение.")

    assert discussion.messages == ["Анна Климаш: Начинаем обсуждение."]


def test_discussion_requires_book_in_club() -> None:
    member = Member(1, "Анна Климаш", "anna@example.com", "owner")
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)
    club = Club(1, "Клуб классики", "Читаем классику", [member])

    with pytest.raises(ValueError):
        club.create_discussion(1, book, member, "Главный конфликт")


def test_add_club() -> None:
    clubs: list[Club] = []

    club = add_club(clubs, "Современная проза", "Обсуждаем новые книги")

    assert club in clubs
    assert club.id == 1
