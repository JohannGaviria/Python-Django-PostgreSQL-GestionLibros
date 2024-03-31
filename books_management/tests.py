from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Author, Book


# Tests para crear libros
class BookAPICreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
    
    # Prueba para crear libros correctamente
    def test_successful_create_book(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('create_book')
        data = {
            "title": "Test Title",
            "user": self.user.id,
            "author": {
                "full_name": "Test full name",
                "email": "test@example.com"
            },
            "genre": [
                {"genre": "Test Genre 1"},
                {"genre": "Test Genre 2"}
            ],
            "publication_year": 1999
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Prueba para crear libro con datos faltantes
    def test_create_book_missing_data(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('create_book')
        data = {
            "author": {
                "full_name": "Test full name",
                "email": "test@example.com"
            },
            "genre": [
                {"genre": "Test Genre 1"},
                {"genre": "Test Genre 2"}
            ],
            "publication_year": 1999
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Tests para obtener todos los libros
class GetAllBooksAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    # Prueba para obtener todos los libros no auntenticado
    def test_get_all_books_unauthenticated(self):
        url = reverse('get_all_books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Prueba para obtener todos los libros cuando no existen
    def test_get_all_books_no_books(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        Book.objects.all().delete()

        url = reverse('get_all_books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Books not found for the current user')


# Test para obtener libro por su PK
class GetBookByPkAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        author = Author.objects.create(full_name='Test Author', email='author@example.com')
        self.book = Book.objects.create(title='Test Title', author=author, publication_year=2000, user=self.user)

    # Prueba para obtener libro por su PK autenticado
    def test_get_book_by_pk_authenticated(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('get_book_by_pk', args=[self.book.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Book', response.data)
        self.assertEqual(response.data['Book']['id'], self.book.id)

    # Prueba para obtener libro por su PK no auntenticado
    def test_get_book_by_pk_unauthenticated(self):
        url = reverse('get_book_by_pk', args=[self.book.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Prueba para obtener un libro por su PK no existente
    def test_get_book_by_pk_nonexistent(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        nonexistent_pk = self.book.id + 1
        url = reverse('get_book_by_pk', args=[nonexistent_pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Book not found')


# Tests para actualizar libros
class UpdateBookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        author = Author.objects.create(full_name='Test Author', email='author@example.com')
        self.book = Book.objects.create(title='Test Title', author=author, publication_year=2000, user=self.user)


    # Prueba para actualizar libro autenticado
    def test_update_book_authenticated(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('update_book', args=[self.book.id])
        data = {
            "title": "Updated Title",
            "user": self.user.id,
            "author": {
                "full_name": "Test full name",
                "email": "test@example.com"
            },
            "genre": [
                {"genre": "Test Genre 1"},
                {"genre": "Test Genre 2"}
            ],
            "publication_year": 2020
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book updated successfully')
        self.assertEqual(response.data['Book']['title'], 'Updated Title')
        self.assertEqual(response.data['Book']['publication_year'], 2020)

    # Prueba para actualizar libro no auntenticado
    def test_update_book_unauthenticated(self):
        url = reverse('update_book', args=[self.book.id])
        data = {
            "title": "Test Title",
            "user": self.user.id,
            "author": {
                "full_name": "Test full name",
                "email": "test@example.com"
            },
            "genre": [
                {"genre": "Test Genre 1"},
                {"genre": "Test Genre 2"}
            ],
            "publication_year": 1999
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Prueba para actualizar libro no existente
    def test_update_book_nonexistent(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        nonexistent_pk = self.book.id + 1
        url = reverse('update_book', args=[nonexistent_pk])
        data = {
            "title": "Test Title",
            "user": self.user.id,
            "author": {
                "full_name": "Test full name",
                "email": "test@example.com"
            },
            "genre": [
                {"genre": "Test Genre 1"},
                {"genre": "Test Genre 2"}
            ],
            "publication_year": 1999
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Book not found')
    
    # Prueba para actualizar libro con datos faltantes
    def test_update_book_missing_data(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('create_book')
        data = {
            "author": {
                "full_name": "Test full name",
                "email": "test@example.com"
            },
            "genre": [
                {"genre": "Test Genre 1"},
                {"genre": "Test Genre 2"}
            ],
            "publication_year": 1999
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Tests para la eliminacion de libros
class DeleteBookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        author = Author.objects.create(full_name='Test Author', email='author@example.com')
        self.book = Book.objects.create(title='Test Title', author=author, publication_year=2000, user=self.user)

    # Prueba de eliminar libro autenticado
    def test_delete_book_authenticated(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('delete_book', args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    # Prueba de eliminar libro no autenticado
    def test_delete_book_unauthenticated(self):
        url = reverse('delete_book', args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertTrue(Book.objects.filter(id=self.book.id).exists())

    # Prueba de eliminar libro que no existe.
    def test_delete_book_not_found(self):
        
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('delete_book', args=[999])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Test para obtener libro por su PK cuando el usuario no es el propietario
class GetBookByPkUnauthorizedAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='password123')
        author = Author.objects.create(full_name='Test Author', email='author@example.com')
        self.book = Book.objects.create(title='Test Title', author=author, publication_year=2000, user=self.user1)

    # Prueba para obtener libro por su PK cuando el usuario no es el propietario
    def test_get_book_by_pk_unauthorized(self):
        token = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('get_book_by_pk', args=[self.book.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'You are not allowed to access this book')


# Test para actualizar libros cuando el usuario no es el propietario
class UpdateBookUnauthorizedAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='password123')
        author = Author.objects.create(full_name='Test Author', email='author@example.com')
        self.book = Book.objects.create(title='Test Title', author=author, publication_year=2000, user=self.user1)
    
    # Prueba para actualizar libro cuando el usuario no es el propietario
    def test_update_book_unauthorized(self):
        token = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('update_book', args=[self.book.id])
        data = {
            "title": "Updated Title",
            "user": self.user2.id,
            "author": {
                "full_name": "Test full name",
                "email": "test@example.com"
            },
            "genre": [
                {"genre": "Test Genre 1"},
                {"genre": "Test Genre 2"}
            ],
            "publication_year": 2020
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'You are not allowed to access this book')


# Test para eliminar libros cuando el usuario no es el propietario
class DeleteBookUnauthorizedAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='password123')
        author = Author.objects.create(full_name='Test Author', email='author@example.com')
        self.book = Book.objects.create(title='Test Title', author=author, publication_year=2000, user=self.user1)

    # Prueba de eliminar libro cuando el usuario no es el propietario
    def test_delete_book_unauthorized(self):
        token = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('delete_book', args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'You are not allowed to access this book')
