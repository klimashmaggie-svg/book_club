"""Проверки создания книг, поиска и добавления в коллекцию."""

from models import Book, add_book, find_books


def test_book_creation() -> None:
    """Книга хранит свои поля и выводится в читаемом виде."""
    book = Book(1, "Преступление и наказание", "Федор Достоевский", 1866)

    assert book.id == 1
    assert book.title == "Преступление и наказание"
    assert book.author == "Федор Достоевский"
    assert book.year == 1866
    assert "Преступление" in str(book)


def test_book_search() -> None:
    """Поиск находит книгу по автору независимо от регистра."""
    books = [
        Book(1, "Преступление и наказание", "Федор Достоевский", 1866),
        Book(2, "Мастер и Маргарита", "Михаил Булгаков", 1967),
    ]

    result = find_books(books, "булгаков")

    assert result == [books[1]]


def test_add_book() -> None:
    """Новая книга добавляется в список с первым свободным id."""
    books: list[Book] = []

    book = add_book(books, "Евгений Онегин", "Александр Пушкин", 1833)

    assert book in books
    assert book.id == 1
