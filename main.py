from models import find_books, find_clubs, find_discussions_by_book
from storage import load_all, save_all


def main() -> None:
    """Run a short console demonstration of the book club project."""
    clubs, members, books, discussions = load_all()

    print("BookClub: объектная модель книжного клуба")
    print()

    print("Клубы:")
    for club in clubs:
        print(f"- {club}")

    print()
    print("Участники:")
    for member in members:
        print(f"- {member}")

    print()
    print("Книги:")
    for book in books:
        print(f"- {book}")

    print()
    print("Обсуждения:")
    for discussion in discussions:
        print(f"- {discussion}")
        for message in discussion.messages:
            print(f"  {message}")

    if clubs and books:
        print()
        print("Поиск книги по запросу 'достоевский':")
        for book in find_books(books, "достоевский"):
            print(f"- {book}")

        print()
        print("Поиск клуба по запросу 'классик':")
        for club in find_clubs(clubs, "классик"):
            print(f"- {club.name}")

        print()
        print(f"Обсуждения книги «{books[0].title}»:")
        for discussion in find_discussions_by_book(discussions, books[0].id):
            print(f"- {discussion.topic}")

    save_all(clubs, members, books, discussions)


if __name__ == "__main__":
    main()
