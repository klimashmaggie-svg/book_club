from .book import Book
from .discussion import Discussion
from .member import Member


class Club:
    """Book club that unites members, books and discussions."""

    def __init__(
        self,
        club_id: int,
        name: str,
        description: str,
        members: list[Member] | None = None,
        books: list[Book] | None = None,
        discussions: list[Discussion] | None = None,
        subclubs: list["Club"] | None = None,
    ) -> None:
        # Клуб хранит не id, а реальные объекты участников, книг и обсуждений.
        self.id = club_id
        self.name = name
        self.description = description
        self.members = members or []
        self.books = books or []
        self.discussions = discussions or []
        self.subclubs = subclubs or []

    def add_subclub(self, club: "Club") -> None:
        """Add another club inside this club."""
        if club is self or club in self.subclubs:
            raise ValueError("A club cannot contain itself or duplicate a subclub")
        self.subclubs.append(club)

    def add_member(self, member: Member) -> None:
        """Add a member to the club if they are not already included."""
        # Сравниваем id, чтобы не добавить копию того же участника.
        if not self.has_member(member):
            self.members.append(member)

    def has_member(self, member: Member) -> bool:
        """Return True if the member belongs to the club."""
        return any(item.id == member.id for item in self.members)

    def add_book(self, book: Book) -> None:
        """Add a book to the club reading list."""
        # Одна и та же книга не должна дублироваться в списке клуба.
        if not any(item.id == book.id for item in self.books):
            self.books.append(book)

    def create_discussion(
        self,
        discussion_id: int,
        book: Book,
        author: Member,
        topic: str,
    ) -> Discussion:
        """Create a discussion linked with this club, a book and a member."""
        # Обсуждение можно создать только для книги, добавленной в клуб.
        if not any(item.id == book.id for item in self.books):
            raise ValueError("The book must be added to the club first")
        # Автор обсуждения должен быть участником этого клуба.
        if not self.has_member(author):
            raise ValueError("The discussion author must be a club member")

        # Discussion получает ссылки на объекты Book и Member.
        discussion = Discussion(
            discussion_id=discussion_id,
            club_id=self.id,
            book=book,
            author=author,
            topic=topic,
        )
        self.discussions.append(discussion)
        return discussion

    def to_data(self) -> dict:
        """Convert the object to JSON-compatible data."""
        # Для связей сохраняются id объектов, чтобы JSON оставался простым.
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "member_ids": [member.id for member in self.members],
            "book_ids": [book.id for book in self.books],
            "discussion_ids": [
                discussion.id for discussion in self.discussions
            ],
            "subclub_ids": [club.id for club in self.subclubs],
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        members: list[Member],
        books: list[Book],
        discussions: list[Discussion],
    ) -> "Club":
        """Create a Club object using linked objects."""
        # По id из JSON выбираем уже созданные объекты участников, книг
        # и обсуждений. Так восстанавливаются связи между объектами.
        return cls(
            club_id=data["id"],
            name=data["name"],
            description=data["description"],
            members=[
                member
                for member in members
                if member.id in data.get("member_ids", [])
            ],
            books=[
                book for book in books if book.id in data.get("book_ids", [])
            ],
            discussions=[
                discussion
                for discussion in discussions
                if discussion.id in data.get("discussion_ids", [])
            ],
        )

    def __str__(self) -> str:
        return (
            f"{self.name}: участников — {len(self.members)}, "
            f"книг — {len(self.books)}, "
            f"обсуждений — {len(self.discussions)}"
        )


def add_club(
    clubs: list[Club],
    name: str,
    description: str,
) -> Club:
    """Create a club and add it to the collection."""
    # Новый id выбирается на основе уже существующих клубов.
    next_id = max((club.id for club in clubs), default=0) + 1
    club = Club(next_id, name, description)
    clubs.append(club)
    return club


def find_clubs(clubs: list[Club], query: str) -> list[Club]:
    """Find clubs by name or description."""
    normalized_query = query.lower()
    return [
        club
        for club in clubs
        if normalized_query in club.name.lower()
        or normalized_query in club.description.lower()
    ]
