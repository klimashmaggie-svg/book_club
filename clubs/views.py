from django.http import Http404
from django.shortcuts import render

from models import find_club_by_id, find_discussion_by_id
from storage import load_all


def club_list(request):
    """Show all book clubs."""
    clubs, _, _, _ = load_all()
    return render(request, "clubs/club_list.html", {"clubs": clubs})


def discussion_list(request):
    """Show all discussions."""
    _, _, _, discussions = load_all()
    return render(
        request,
        "clubs/discussion_list.html",
        {"discussions": discussions},
    )


def club_detail(request, club_id: int):
    """Show one club and its discussions."""
    clubs, _, _, _ = load_all()
    club = find_club_by_id(clubs, club_id)
    if club is None:
        raise Http404("Клуб не найден")
    return render(request, "clubs/club_detail.html", {"club": club})


def discussion_detail(request, discussion_id: int):
    """Show a member's review and its linked book."""
    _, _, _, discussions = load_all()
    discussion = find_discussion_by_id(discussions, discussion_id)
    if discussion is None:
        raise Http404("Обсуждение не найдено")
    return render(
        request,
        "clubs/discussion_detail.html",
        {"discussion": discussion},
    )
