"""Tests for the Django web interface."""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookclub_web.settings")
django.setup()

from django.test import Client  # noqa: E402


def test_main_pages_are_available() -> None:
    client = Client()

    assert client.get("/").status_code == 200
    assert client.get("/books/").status_code == 200
    assert client.get("/clubs/").status_code == 200
    assert client.get("/members/").status_code == 200
    assert client.get("/clubs/discussions/").status_code == 200


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
