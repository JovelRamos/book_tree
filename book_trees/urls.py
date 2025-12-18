"""Defines URL patterns for book_trees."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.epub_list, name='epub_list'),

    path('upload/', views.upload_epub, name='upload_epub'),

    path('delete/<int:pk>/', views.delete_epub, name='delete_epub'),

    path('epub/<int:pk>/', views.epub_detail, name='epub_detail'),


]
