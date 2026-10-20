from django.http import Http404
from django.shortcuts import render

from db.database import fetch_all, fetch_one


def home(request):
    """Show the project summary and navigation."""
    # Общие показатели вычисляются в SQLite, а не подсчётом JSON в Python.
    context = {
        **dict(fetch_one("book_totals")),
        **dict(fetch_one("community_totals")),
        "recent_discussions": fetch_all("featured_discussions", (3, 0)),
    }
    return render(request, "homepage/index.html", context)


def member_list(request):
    """Show all book club members."""
    role = request.GET.get("role", "").strip()
    roles = {"owner": "Владелец", "moderator": "Модератор", "reader": "Читатель"}
    error = "Выберите роль из списка." if role and role not in roles else ""
    if error:
        members = []
    elif role:
        members = fetch_all("members_by_role", (role,))
    else:
        members = fetch_all("members")
    return render(
        request,
        "homepage/member_list.html",
        {"members": members, "role": role, "roles": roles, "error": error},
    )


def member_detail(request, member_id: int):
    """Show one member and their discussions."""
    if member_id > 9223372036854775807:
        raise Http404("Участник не найден")
    member = fetch_one("member", (member_id,))
    if member is None:
        raise Http404("Участник не найден")
    member_discussions = fetch_all("member_discussions", (member_id,))
    return render(
        request,
        "homepage/member_detail.html",
        {"member": member, "discussions": member_discussions},
    )
