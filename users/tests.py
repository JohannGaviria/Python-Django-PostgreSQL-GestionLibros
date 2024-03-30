from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# Tests para el registro
class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Prueba de registro existoso
    def test_successful_sign_up(self):
        url = reverse('signUp')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue('User' in response.data)

    def test_sign_up_with_existing_username(self):
        # Prueba registrar un usuario con un nombre de usuario que ya existe
        existing_user = User.objects.create_user(username='existinguser', password='testpassword', email='existing@example.com')
        url = reverse('signUp')
        data = {
            'username': 'existinguser',
            'password': 'testpassword',
            'email': 'new@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_missing_data(self):
        # Prueba de registro con datos faltantes
        url = reverse('signUp')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_invalid_email(self):
        # Prueba de registro con un correo electrónico inválido
        url = reverse('signUp')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'invalidemail'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Tests para el inicio de sesion
class SignInTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')

    # Prueba de inicio de sesion correctamente
    def test_successful_sign_in(self):
        url = reverse('signIn')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertTrue('User' in response.data)

    def test_sign_in_with_invalid_password(self):
        # Prueba iniciar sesión con una contraseña incorrecta
        url = reverse('signIn')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_with_missing_data(self):
        # Prueba de inicio de sesión con datos faltantes
        url = reverse('signIn')
        data = {
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Test para el cierre de sesion del usuario
class SignOutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    # Prueba de cierre de sesion
    def test_sign_out(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = '/api/user/signOut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)