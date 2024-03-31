from django.urls import path
from . import views


# Definimos la URL de la aplicación
urlpatterns = [
    path('', views.search_books, name='search_books'),
]
