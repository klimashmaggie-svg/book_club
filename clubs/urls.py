from django.urls import path

from . import views

app_name = "clubs"

urlpatterns = [
    path("", views.club_list, name="club_list"),
    path("discussions/", views.discussion_list, name="discussion_list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:club_id>/", views.club_detail, name="club_detail"),
    path(
        "discussions/<int:discussion_id>/",
        views.discussion_detail,
        name="discussion_detail",
    ),
]
