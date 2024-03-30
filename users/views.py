from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .serializers import UserSerializer
from datetime import datetime


# Logica para el registro del usuario
@api_view(['POST'])
def signUp(request):
    # Serializa los datos recibidos en la solicitud
    serializer = UserSerializer(data=request.data)

    # Verifica si los datos son válidos según las reglas definidas en el serializador
    if serializer.is_valid():
        # Obtiene los campos validados del serializador
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        # Verifica si los campos requeridos no están vacíos
        if not username or not email or not password:
            return Response({
                'error': 'Username, email and password are required fields'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verifica si el nombre de usuario ya existe en la base de datos
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Crea un nuevo usuario en la base de datos
        user = User.objects.create_user(username=username, email=email, password=password)

        # Crea un token de autenticación para el usuario
        token = Token.objects.create(user=user)

        # Devuelve una respuesta con el token y los datos del usuario creado
        return Response({
            'token': token.key,
            'User': serializer.data
        }, status=status.HTTP_201_CREATED)

    # Si los datos no son válidos, devuelve los errores de validación
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# Logica para el inicio de sesion del usuario
@api_view(['POST'])
def signIn(request):
    # Obtiene el nombre de usuario y la contraseña de la solicitud
    username = request.data.get('username', '')
    password = request.data.get('password', '')

    # Verifica si el nombre de usuario y la contraseña no están vacíos
    if not username or not password:
        return Response({
            'error': 'Username and password are required fields'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Busca el usuario en la base de datos por el nombre de usuario
    user = get_object_or_404(User, username=username)

    # Verifica si la contraseña proporcionada coincide con la contraseña almacenada
    if not user.check_password(password):
        return Response({
            'error': 'Invalid password'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Modificar el campo de 'is_active'
    user.is_active = True
    user.save()

    # Obtiene o crea un token de autenticación para el usuario
    token, created = Token.objects.get_or_create(user=user)

    # Serializa los datos del usuario para la respuesta
    serializer = UserSerializer(instance=user)

    # Devuelve una respuesta con el token y los datos del usuario
    return Response({
        'token': token.key,
        'User': {
            'user_id': serializer.data['id'],
            'username': serializer.data['username'],
            'email': serializer.data['email'],
        }
    }, status=status.HTTP_200_OK)



# Logica para desconectar al usuario
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def signOut(request):
    # Obtener el usuario actual
    user = request.user

    # Actualizar los campos
    user.last_login = timezone.now()
    # user.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user.is_active = False

    # Guardar el usuario
    user.save()

    return Response({
        'message': 'User signed out successfully'
    }, status=status.HTTP_200_OK)
