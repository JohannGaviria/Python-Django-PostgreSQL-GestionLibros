from rest_framework import serializers
from .models import Author, Genre, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'full_name',
            'email'
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id',
            'genre'
        ]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'user',
            'title',
            'author',
            'genre',
            'publication_year'
        ]
    
    def create(self, validated_data):
        author_data = validated_data.pop('author')
        genres_data = validated_data.pop('genre')
        user = validated_data.pop('user')

        author, _ = Author.objects.get_or_create(**author_data)
        genres = [Genre.objects.get_or_create(**genre_data)[0] for genre_data in genres_data]

        book = Book.objects.create(author=author, user=user, **validated_data)
        book.genre.set(genres)

        return book
    
    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        genres_data = validated_data.pop('genre')
        user = validated_data.pop('user')

        instance.title = validated_data.get('title', instance.title)
        instance.publication_year = validated_data.get('publication_year', instance.publication_year)
        instance.user = user

        author, _ = Author.objects.get_or_create(**author_data)
        instance.author = author

        genres = [Genre.objects.get_or_create(**genre_data)[0] for genre_data in genres_data]
        instance.genre.set(genres)

        instance.save()

        return instance
