from django.urls import path

from . import views

app_name = "homepage"

urlpatterns = [
    path("", views.home, name="home"),
    path("members/", views.member_list, name="member_list"),
    path(
        "members/<int:member_id>/",
        views.member_detail,
        name="member_detail",
    ),
]
