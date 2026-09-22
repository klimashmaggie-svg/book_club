class Member:
    """Member of a book club."""

    def __init__(
        self,
        member_id: int,
        name: str,
        email: str,
        role: str = "reader",
    ) -> None:
        # Атрибуты объекта описывают конкретного участника клуба.
        self.id = member_id
        self.name = name
        self.email = email
        self.role = role

    @property
    def is_moderator(self) -> bool:
        """Return True if the member can moderate discussions."""
        # Свойство позволяет обращаться как к обычному полю: member.is_moderator.
        return self.role in ("moderator", "owner")

    def to_data(self) -> dict:
        """Convert the object to JSON-compatible data."""
        # В JSON сохраняются простые значения, а не сам объект Member.
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }

    @classmethod
    def from_data(cls, data: dict) -> "Member":
        """Create a Member object from JSON-compatible data."""
        # Если роль не указана в JSON, участник считается обычным читателем.
        return cls(
            member_id=data["id"],
            name=data["name"],
            email=data["email"],
            role=data.get("role", "reader"),
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.email}), роль: {self.role}"


def add_member(
    members: list[Member],
    name: str,
    email: str,
    role: str = "reader",
) -> Member:
    """Create a member and add it to the collection."""
    # Новый id выбирается на основе уже существующих участников.
    next_id = max((member.id for member in members), default=0) + 1
    member = Member(next_id, name, email, role)
    members.append(member)
    return member


def find_members(members: list[Member], query: str) -> list[Member]:
    """Find members by name or email."""
    normalized_query = query.lower()
    return [
        member
        for member in members
        if normalized_query in member.name.lower()
        or normalized_query in member.email.lower()
    ]
