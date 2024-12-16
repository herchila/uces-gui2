from django.contrib import admin
from django.urls import include, path

from . import views


app_name = "polls"
urlpatterns = [
    path("", views.index2, name="index"),
    path("<int:question_id>", views.edit, name="edit"),
    path("<int:question_id>/delete", views.delete, name="delete"),
]
