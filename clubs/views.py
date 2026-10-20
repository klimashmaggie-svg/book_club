from django.http import Http404
from django.shortcuts import render

from db.database import fetch_all, fetch_one


def club_list(request):
    """Show all book clubs."""
    clubs = fetch_all("clubs")
    return render(request, "clubs/club_list.html", {"clubs": clubs})


def discussion_list(request):
    """Показать отзывы с книгами и авторами; фильтр по клубу выполняет SQL."""
    selected = request.GET.get("club", "").strip()
    club_id = None
    error = ""
    if selected:
        try:
            club_id = int(selected)
            if not 1 <= club_id <= 9223372036854775807:
                raise ValueError
            if fetch_one("club", (club_id,)) is None:
                raise ValueError
        except ValueError:
            error = "Выберите существующий клуб."
    discussions = [] if error else fetch_all("discussions", (club_id,))
    return render(
        request,
        "clubs/discussion_list.html",
        {"discussions": discussions, "clubs": fetch_all("clubs"),
         "selected": selected, "error": error},
    )


def club_detail(request, club_id: int):
    """Show one club and its discussions."""
    if club_id > 9223372036854775807:
        raise Http404("Клуб не найден")
    club = fetch_one("club", (club_id,))
    if club is None:
        raise Http404("Клуб не найден")
    return render(request, "clubs/club_detail.html", {
        "club": club, "discussions": fetch_all("discussions", (club_id,)),
    })


def discussion_detail(request, discussion_id: int):
    """Show a member's review and its linked book."""
    if discussion_id > 9223372036854775807:
        raise Http404("Обсуждение не найдено")
    discussion = fetch_one("discussion", (discussion_id,))
    if discussion is None:
        raise Http404("Обсуждение не найдено")
    return render(
        request,
        "clubs/discussion_detail.html",
        {"discussion": discussion},
    )


def statistics(request):
    """COUNT, GROUP BY и HAVING: статистика книг, клубов и участников."""
    threshold = request.GET.get("min_reviews", "0").strip()
    error = ""
    try:
        minimum = int(threshold)
        if not 0 <= minimum <= 1000000:
            raise ValueError
    except ValueError:
        minimum = 0
        error = "Укажите минимальное число отзывов от 0 до 1000000."
    context = {
        **dict(fetch_one("book_totals")),
        **dict(fetch_one("community_totals")),
        "book_statistics": [] if error else fetch_all("book_statistics", (minimum,)),
        "club_statistics": fetch_all("clubs"),
        "member_statistics": fetch_all("member_statistics"),
        "threshold": threshold, "error": error,
    }
    return render(request, "clubs/statistics.html", context)
