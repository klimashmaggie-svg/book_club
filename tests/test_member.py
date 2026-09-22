"""Проверки создания участников, их ролей, добавления и поиска."""

from models import Member, add_member, find_members


def test_member_creation() -> None:
    """Поля участника и строковое представление сохраняют его данные."""
    member = Member(1, "Елена Морозова", "elena@example.com", "owner")

    assert member.id == 1
    assert member.name == "Елена Морозова"
    assert member.email == "elena@example.com"
    assert member.role == "owner"
    assert member.is_moderator
    assert "Елена Морозова" in str(member)


def test_member_roles() -> None:
    """Владелец и модератор могут модерировать, читатель не может."""
    owner = Member(1, "Олег Соколов", "oleg@example.com", "owner")
    moderator = Member(2, "Дарья Белова", "daria@example.com", "moderator")
    reader = Member(3, "Роман Орлов", "roman@example.com")

    assert owner.is_moderator
    assert moderator.is_moderator
    assert not reader.is_moderator
    assert reader.role == "reader"


def test_member_search() -> None:
    """Поиск имени не зависит от регистра букв."""
    members = [
        Member(1, "София Волкова", "sofia@example.com", "owner"),
        Member(2, "Иван Петров", "ivan@example.com"),
    ]

    result = find_members(members, "ИВАН")

    assert result == [members[1]]


def test_member_search_by_email() -> None:
    """Участника можно найти и по части адреса электронной почты."""
    members = [
        Member(1, "Кира Алексеева", "kira@example.com"),
        Member(2, "Павел Новиков", "pavel@books.ru"),
    ]

    assert find_members(members, "BOOKS.RU") == [members[1]]


def test_add_member() -> None:
    """Новый участник попадает в список и получает следующий id."""
    members = [Member(3, "Алина Сергеева", "alina@example.com")]

    member = add_member(members, "Мария Смирнова", "maria@example.com")

    assert member in members
    assert member.id == 4
    assert not member.is_moderator
