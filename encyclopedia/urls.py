from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create", views.create_new_page, name="create_new_page"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path("random", views.random_page, name="random_page")
]
