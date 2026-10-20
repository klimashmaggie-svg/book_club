"""Tests for the Django web interface."""

import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookclub_web.settings")
django.setup()

from django.test import Client  # noqa: E402

pytestmark = pytest.mark.usefixtures("sqlite_db")


def test_main_pages_are_available() -> None:
    client = Client()

    assert client.get("/").status_code == 200
    assert client.get("/books/").status_code == 200
    assert client.get("/clubs/").status_code == 200
    assert client.get("/members/").status_code == 200
    assert client.get("/clubs/discussions/").status_code == 200
    assert client.get("/books/unreviewed/").status_code == 200
    assert client.get("/clubs/statistics/").status_code == 200


def test_base_template_connects_static_files() -> None:
    """The shared template connects the PR6 CSS, image and JavaScript."""
    content = Client().get("/").content.decode()

    assert "/static/homepage/css/style.css" in content
    assert "/static/homepage/js/main.js" in content
    assert "/static/homepage/img/logo.png" in content


def test_dynamic_pages_show_linked_objects() -> None:
    client = Client()

    book_response = client.get("/books/1/")
    club_response = client.get("/clubs/1/")
    discussion_response = client.get("/clubs/discussions/1/")
    member_response = client.get("/members/1/")

    assert book_response.status_code == 200
    assert "Преступление и наказание" in book_response.content.decode()
    assert club_response.status_code == 200
    assert "Классика" in club_response.content.decode()
    assert discussion_response.status_code == 200
    assert "Елена Морозова" in discussion_response.content.decode()
    assert member_response.status_code == 200
    assert "elena@example.com" in member_response.content.decode()


def test_unknown_objects_return_404() -> None:
    client = Client()

    assert client.get("/books/999/").status_code == 404
    assert client.get("/clubs/999/").status_code == 404
    assert client.get("/clubs/discussions/999/").status_code == 404
    assert client.get("/members/999/").status_code == 404
    for prefix in ("/books/", "/members/", "/clubs/", "/clubs/discussions/"):
        assert client.get(prefix + "9" * 30 + "/").status_code == 404


def test_pages_read_database_instead_of_json(sqlite_db) -> None:
    """UPDATE SQLite отражается и на странице книги, и в связанном JOIN-отзыве."""
    from contextlib import closing

    from db.database import get_connection

    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                "UPDATE books SET title = ? WHERE id = 1", ("Книга из SQLite",)
            )
    for url in ("/books/", "/books/1/", "/clubs/discussions/1/", "/clubs/1/"):
        content = Client().get(url).content.decode()
        assert "Книга из SQLite" in content
        assert "Преступление и наказание" not in content


def test_book_search_filters_and_injection() -> None:
    client = Client()
    content = client.get("/books/", {
        "q": "Булгаков", "year": "1950",
    }).content.decode()
    assert 'href="/books/2/"' in content
    assert 'href="/books/7/"' not in content
    content = client.get("/books/", {"q": "' OR 1=1 --"}).content.decode()
    assert "Книги не найдены." in content
    assert 'href="/books/1/"' not in content
    content = client.get("/books/", {"year": "не год"}).content.decode()
    assert "Укажите год" in content


def test_unreviewed_books_excludes_only_selected_members_reviews() -> None:
    content = Client().get("/books/unreviewed/", {"member": "1"}).content.decode()
    assert 'href="/books/1/"' not in content
    assert 'href="/books/3/"' in content
    assert "Елена Морозова" in content
    content = Client().get("/books/unreviewed/", {
        "member": "1", "q": "Преступление",
    }).content.decode()
    assert "Подходящих книг без отзыва этого участника не найдено." in content


@pytest.mark.parametrize("member", ["abc", "999", "-1", "9" * 100])
def test_invalid_search_member_is_handled(member) -> None:
    response = Client().get("/books/unreviewed/", {"member": member})
    assert response.status_code == 200
    assert "Выберите существующего участника." in response.content.decode()


def test_role_and_club_filters() -> None:
    content = Client().get("/members/", {"role": "moderator"}).content.decode()
    assert "Мария Смирнова" in content
    assert "Елена Морозова" not in content
    content = Client().get("/clubs/discussions/", {"club": "2"}).content.decode()
    assert "Евгений Онегин" in content
    assert "Преступление и наказание" not in content
    content = Client().get("/clubs/discussions/", {"club": "abc"}).content.decode()
    assert "Выберите существующий клуб." in content


def test_statistics_having_and_empty_result() -> None:
    content = Client().get("/clubs/statistics/").content.decode()
    assert "Отцы и дети" in content  # LEFT JOIN сохраняет книги без отзывов.
    content = Client().get("/clubs/statistics/", {"min_reviews": "1"}).content.decode()
    assert "Отцы и дети" not in content
    assert "Преступление и наказание" in content
    content = Client().get("/clubs/statistics/", {"min_reviews": "2"}).content.decode()
    assert "Нет книг с таким количеством отзывов." in content
    content = Client().get("/clubs/statistics/", {
        "min_reviews": "bad",
    }).content.decode()
    assert "Укажите минимальное число отзывов" in content


def test_empty_database_pages_are_still_available() -> None:
    from contextlib import closing

    from db.database import get_connection

    with closing(get_connection()) as connection:
        with connection:
            for table in (
                "club_discussions", "discussions", "books", "members", "clubs",
            ):
                connection.execute(f"DELETE FROM {table}")
    for path in ("/", "/books/", "/members/", "/clubs/", "/clubs/discussions/",
                 "/clubs/statistics/", "/books/unreviewed/"):
        assert Client().get(path).status_code == 200
    content = Client().get("/books/").content.decode()
    assert "Книги не найдены." in content
