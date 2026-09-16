class Book:
    """Book selected for reading in a book club."""

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
    ) -> None:
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year

    def matches_query(self, query: str) -> bool:
        """Check whether the book matches a search query."""
        normalized_query = query.lower()
        return (
            normalized_query in self.title.lower()
            or normalized_query in self.author.lower()
        )

    def to_data(self) -> dict:
        """Convert the object to JSON-compatible data."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
        }

    @classmethod
    def from_data(cls, data: dict) -> "Book":
        """Create a Book object from JSON-compatible data."""
        return cls(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
        )

    def __str__(self) -> str:
        return f"{self.title} — {self.author}, {self.year}"


def add_book(
    books: list[Book],
    title: str,
    author: str,
    year: int,
) -> Book:
    """Create a book and add it to the collection."""
    next_id = max((book.id for book in books), default=0) + 1
    book = Book(next_id, title, author, year)
    books.append(book)
    return book


def find_books(books: list[Book], query: str) -> list[Book]:
    """Find books by title or author."""
    return [book for book in books if book.matches_query(query)]
