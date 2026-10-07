"""Проверки новой логики клубов и обсуждений."""

from models import Book, Club, Discussion, Member, add_club


def test_discussion_combines_member_book_and_review() -> None:
    """Обсуждение связывает участника, книгу и текст отзыва."""
    member = Member(1, "Вера Соколова", "vera@example.com")
    book = Book(1, "Отцы и дети", "Иван Тургенев", 1862)

    discussion = Discussion(1, member, book, "Интересный конфликт поколений.")

    assert discussion.member is member
    assert discussion.book is book
    assert discussion.review == "Интересный конфликт поколений."
    assert discussion.is_about(book)


def test_club_stores_discussions() -> None:
    """Клуб является коллекцией связанных обсуждений."""
    member = Member(1, "Ирина Лебедева", "irina@example.com")
    book = Book(1, "Мы", "Евгений Замятин", 1924)
    discussion = Discussion(1, member, book, "Роман о свободе.")
    club = Club(1, "Клуб фантастики", "Читаем фантастику")

    club.add_discussion(discussion)

    assert club.discussions == [discussion]
    assert club.to_data()["discussion_ids"] == [1]


def test_club_does_not_duplicate_discussion() -> None:
    """Обсуждение с тем же id не добавляется в клуб повторно."""
    member = Member(1, "Олег Соколов", "oleg@example.com")
    book = Book(1, "Мы", "Евгений Замятин", 1924)
    first = Discussion(1, member, book, "Первый отзыв.")
    copy = Discussion(1, member, book, "Копия отзыва.")
    club = Club(1, "Клуб фантастики", "Читаем фантастику", [first])

    club.add_discussion(copy)

    assert club.discussions == [first]


def test_club_creates_discussion() -> None:
    """Клуб создаёт обсуждение и сразу добавляет его в свой список."""
    member = Member(1, "Мария Смирнова", "maria@example.com")
    book = Book(1, "Евгений Онегин", "Александр Пушкин", 1833)
    club = Club(1, "Клуб классики", "Читаем классику")

    discussion = club.create_discussion(1, member, book, "Хорошая книга.")

    assert discussion in club.discussions
    assert discussion.member is member
    assert discussion.book is book


def test_add_club() -> None:
    """Функция создаёт клуб и добавляет его в коллекцию."""
    clubs: list[Club] = []

    club = add_club(clubs, "Современная проза", "Обсуждаем новые книги")

    assert club in clubs
    assert club.id == 1
