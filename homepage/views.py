from django.http import Http404
from django.shortcuts import render

from models import find_member_by_id
from storage import load_all


def home(request):
    """Show the project summary and navigation."""
    clubs, members, books, discussions = load_all()
    context = {
        "clubs_count": len(clubs),
        "members_count": len(members),
        "books_count": len(books),
        "discussions_count": len(discussions),
        "recent_discussions": discussions[:3],
    }
    return render(request, "homepage/index.html", context)


def member_list(request):
    """Show all book club members."""
    _, members, _, _ = load_all()
    return render(
        request,
        "homepage/member_list.html",
        {"members": members},
    )


def member_detail(request, member_id: int):
    """Show one member and their discussions."""
    _, members, _, discussions = load_all()
    member = find_member_by_id(members, member_id)
    if member is None:
        raise Http404("Участник не найден")
    member_discussions = [
        item for item in discussions if item.member.id == member_id
    ]
    return render(
        request,
        "homepage/member_detail.html",
        {"member": member, "discussions": member_discussions},
    )
