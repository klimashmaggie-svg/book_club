from .book import Book
from .member import Member


class Discussion:
    """Discussion of a book inside a club."""

    def __init__(
        self,
        discussion_id: int,
        club_id: int,
        book: Book,
        author: Member,
        topic: str,
        messages: list[str] | None = None,
    ) -> None:
        # Обсуждение связывает клуб, книгу, автора и список сообщений.
        self.id = discussion_id
        self.club_id = club_id
        self.book = book
        self.author = author
        self.topic = topic
        self.messages = messages or []

    def add_message(self, member: Member, text: str) -> None:
        """Add a message to the discussion."""
        # Сообщение хранится вместе с именем автора для удобного вывода.
        self.messages.append(f"{member.name}: {text}")

    def to_data(self) -> dict:
        """Convert the object to JSON-compatible data."""
        # В JSON сохраняются id связанных объектов, а не сами объекты.
        return {
            "id": self.id,
            "club_id": self.club_id,
            "book_id": self.book.id,
            "author_id": self.author.id,
            "topic": self.topic,
            "messages": self.messages,
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        books: list[Book],
        members: list[Member],
    ) -> "Discussion":
        """Create a Discussion object using linked Book and Member objects."""
        # При загрузке нужно найти реальные объекты книги и автора по их id.
        book = _find_required_book(books, data["book_id"])
        author = _find_required_member(members, data["author_id"])
        return cls(
            discussion_id=data["id"],
            club_id=data["club_id"],
            book=book,
            author=author,
            topic=data["topic"],
            messages=data.get("messages", []),
        )

    def __str__(self) -> str:
        return (
            f"Обсуждение #{self.id}: {self.topic} "
            f"по книге «{self.book.title}»"
        )


def find_discussions_by_book(
    discussions: list[Discussion],
    book_id: int,
) -> list[Discussion]:
    """Find discussions for a selected book."""
    return [
        discussion
        for discussion in discussions
        if discussion.book.id == book_id
    ]


def _find_required_book(books: list[Book], book_id: int) -> Book:
    # Вспомогательная проверка нужна, чтобы не создать обсуждение без книги.
    for book in books:
        if book.id == book_id:
            return book
    raise ValueError(f"Book with id {book_id} was not found")


def _find_required_member(members: list[Member], member_id: int) -> Member:
    # Вспомогательная проверка нужна, чтобы не создать обсуждение без автора.
    for member in members:
        if member.id == member_id:
            return member
    raise ValueError(f"Member with id {member_id} was not found")
