from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from books_management.models import Book, Author, Genre

class SearchBooksAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.author = Author.objects.create(full_name='Test Author', email='author@example.com')
        self.genre1 = Genre.objects.create(genre='Test Genre 1')
        self.genre2 = Genre.objects.create(genre='Test Genre 2')
        self.book1 = Book.objects.create(title='Book Title 1', author=self.author, publication_year=2000)
        self.book1.genre.add(self.genre1)
        self.book2 = Book.objects.create(title='Book Title 2', author=self.author, publication_year=2005)
        self.book2.genre.add(self.genre2)

    def test_search_books_authenticated(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('search_books') + '?query=Test'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Books', response.data)
        self.assertNotEqual(len(response.data['Books']), 0)

    def test_search_books_unauthenticated(self):
        url = reverse('search_books') + '?query=Test'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_books_no_query_parameter(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('search_books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'incorrect search parameters')

    def test_search_books_not_found(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('search_books') + '?query=NonExistent'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'No books found matching your search')
