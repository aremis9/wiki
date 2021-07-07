from unicodedata import name
from django.urls import path
import re
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.wiki, name="wiki"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random/", views.random, name="random"),
    path("new/", views.new, name="new"),
    path("search/", views.search, name="search")
]
