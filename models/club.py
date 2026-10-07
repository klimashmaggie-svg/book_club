from .book import Book
from .discussion import Discussion
from .member import Member

# Хранит список обсуждений и добавляет новые.


class Club:
    """Book club that stores a collection of discussions."""

    def __init__(
        self,
        club_id: int,
        name: str,
        description: str,
        discussions: list[Discussion] | None = None,
    ) -> None:
        self.id = club_id
        self.name = name
        self.description = description
        self.discussions = discussions or []

    def add_discussion(self, discussion: Discussion) -> None:
        """Add a discussion if a discussion with this id is not in the club."""
        if not any(item.id == discussion.id for item in self.discussions):
            self.discussions.append(discussion)

    def create_discussion(
        self,
        discussion_id: int,
        member: Member,
        book: Book,
        review: str,
    ) -> Discussion:
        """Create a discussion from a member, a book and a review."""
        discussion = Discussion(discussion_id, member, book, review)
        self.add_discussion(discussion)
        return discussion

    def to_data(self) -> dict:
        """Convert the club to JSON-compatible data."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "discussion_ids": [item.id for item in self.discussions],
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        discussions: list[Discussion],
    ) -> "Club":
        """Create a club and link its discussion objects by id."""
        discussion_ids = data.get("discussion_ids", [])
        return cls(
            club_id=data["id"],
            name=data["name"],
            description=data["description"],
            discussions=[
                item for item in discussions if item.id in discussion_ids
            ],
        )

    def __str__(self) -> str:
        return f"{self.name}: обсуждений — {len(self.discussions)}"


def add_club(
    clubs: list[Club],
    name: str,
    description: str,
) -> Club:
    """Create a club and add it to the collection."""
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


def find_club_by_id(clubs: list[Club], club_id: int) -> Club | None:
    """Find one club by id."""
    return next((club for club in clubs if club.id == club_id), None)
