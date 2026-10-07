from django.http import Http404
from django.shortcuts import render

from models import find_book_by_id, find_discussions_by_book
from storage import load_all


def book_list(request):
    """Show all books."""
    _, _, books, _ = load_all()
    return render(request, "books/book_list.html", {"books": books})


def book_detail(request, book_id: int):
    """Show one book and its discussions."""
    _, _, books, discussions = load_all()
    book = find_book_by_id(books, book_id)
    if book is None:
        raise Http404("Книга не найдена")
    context = {
        "book": book,
        "discussions": find_discussions_by_book(discussions, book_id),
    }
    return render(request, "books/book_detail.html", context)
