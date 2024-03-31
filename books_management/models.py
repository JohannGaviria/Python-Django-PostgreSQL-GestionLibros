from django.contrib.auth.models import User
from django.db import models


# Modelo para los autores de los libros
class Author(models.Model):
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.full_name


# Modelo para el genero de los libors
class Genre(models.Model):
    genre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.genre


# Modelo para los libros
class Book(models.Model):
    title = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    publication_year = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.title