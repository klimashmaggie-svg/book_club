from django.http import Http404
from django.shortcuts import render

from db.database import fetch_all, fetch_one


def book_list(request):
    """Показать каталог SQLite и поиск по тексту и году издания."""
    query = request.GET.get("q", "").strip()
    year = request.GET.get("year", "").strip()
    error = ""
    min_year = None
    if year:
        try:
            min_year = int(year)
            if not 0 <= min_year <= 9999:
                raise ValueError
        except ValueError:
            error = "Укажите год от 0 до 9999."
    if error:
        books = []
    elif query or year:
        books = fetch_all("search_books", (query, min_year))
    else:
        books = fetch_all("books")
    return render(request, "books/book_list.html", {
        "books": books, "query": query, "year": year, "error": error,
    })


def book_detail(request, book_id: int):
    """Найти книгу SQL-запросом и показать связанные отзывы через JOIN."""
    if book_id > 9223372036854775807:
        raise Http404("Книга не найдена")
    book = fetch_one("book", (book_id,))
    if book is None:
        raise Http404("Книга не найдена")
    context = {
        "book": book,
        "discussions": fetch_all("book_discussions", (book_id,)),
    }
    return render(request, "books/book_detail.html", context)


def unreviewed_books(request):
    """Книги без отзыва выбранного участника: NOT EXISTS и параметры ?."""
    selected = request.GET.get("member", "").strip()
    query = request.GET.get("q", "").strip()
    member = None
    books = []
    error = ""
    if selected:
        try:
            member_id = int(selected)
            if not 1 <= member_id <= 9223372036854775807:
                raise ValueError
            member = fetch_one("member", (member_id,))
        except ValueError:
            member = None
        if member is None:
            error = "Выберите существующего участника."
        else:
            books = fetch_all("unreviewed_books", (member["id"], query))
    return render(request, "books/unreviewed.html", {
        "books": books, "members": fetch_all("members"),
        "member": member, "selected": selected, "query": query, "error": error,
    })
