from .book import Book
from .member import Member


class Discussion:
    """A member's review of a selected book."""

    def __init__(
        self,
        discussion_id: int,
        member: Member,
        book: Book,
        review: str,
    ) -> None:
        # Обсуждение объединяет участника, книгу и его отзыв.
        self.id = discussion_id
        self.member = member
        self.book = book
        self.review = review

    def is_about(self, book: Book) -> bool:
        """Return True if the discussion is linked to the selected book."""
        return self.book.id == book.id

    def to_data(self) -> dict:
        """Convert the discussion to JSON-compatible data."""
        return {
            "id": self.id,
            "member_id": self.member.id,
            "book_id": self.book.id,
            "review": self.review,
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        books: list[Book],
        members: list[Member],
    ) -> "Discussion":
        """Create a discussion and restore linked objects by id."""
        book = _find_required_book(books, data["book_id"])
        member = _find_required_member(members, data["member_id"])
        return cls(
            discussion_id=data["id"],
            member=member,
            book=book,
            review=data["review"],
        )

    def __str__(self) -> str:
        return (
            f"{self.member.name} о книге «{self.book.title}»: "
            f"{self.review}"
        )


def find_discussions_by_book(
    discussions: list[Discussion],
    book_id: int,
) -> list[Discussion]:
    """Find discussions for a selected book."""
    return [item for item in discussions if item.book.id == book_id]


def find_discussion_by_id(
    discussions: list[Discussion],
    discussion_id: int,
) -> Discussion | None:
    """Find one discussion by id."""
    return next(
        (item for item in discussions if item.id == discussion_id),
        None,
    )


def _find_required_book(books: list[Book], book_id: int) -> Book:
    for book in books:
        if book.id == book_id:
            return book
    raise ValueError(f"Book with id {book_id} was not found")


def _find_required_member(members: list[Member], member_id: int) -> Member:
    for member in members:
        if member.id == member_id:
            return member
    raise ValueError(f"Member with id {member_id} was not found")
