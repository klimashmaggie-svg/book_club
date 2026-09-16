from models import Member, add_member, find_members


def test_member_creation() -> None:
    member = Member(1, "Анна Климаш", "anna@example.com", "owner")

    assert member.id == 1
    assert member.name == "Анна Климаш"
    assert member.email == "anna@example.com"
    assert member.role == "owner"
    assert member.is_moderator
    assert "Анна Климаш" in str(member)


def test_member_search() -> None:
    members = [
        Member(1, "Анна Климаш", "anna@example.com", "owner"),
        Member(2, "Иван Петров", "ivan@example.com"),
    ]

    result = find_members(members, "ivan")

    assert result == [members[1]]


def test_add_member() -> None:
    members: list[Member] = []

    member = add_member(members, "Мария Смирнова", "maria@example.com")

    assert member in members
    assert member.id == 1
    assert not member.is_moderator
