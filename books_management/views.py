from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer


# Logica para la creacion de libros
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_book(request):
    # Serializar los datos recibidos en la solicitud
    serializer = BookSerializer(data=request.data)

    # Verifica si los datos son válidos según las reglas definidas en el serializador
    if serializer.is_valid():
        # Guardar los datos del serializador
        serializer.save()

        # Devuelve una respuesta con un mensaje y los datos del libro creado
        return Response({
            'message': 'Successfully created book',
            'Book': serializer.data
        }, status=status.HTTP_201_CREATED)

    # Si los datos no son válidos, devuelve un mensaje y los errores de validación
    return Response({
        'message': 'error when creating the book',
        'erros': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# Logica para obtener todos los libros
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_books(request):
    # Obtener todos los libros de la base de datos
    books = Book.objects.all()

    # Verificar si hay libros
    if not books:
        return Response({
            'message': 'Books not found'
        }, status=status.HTTP_404_NOT_FOUND)

    # Serializar los detalles de todos los libros obtenidos
    serializer = BookSerializer(books, many=True)

    # Devolver los detalles de todos los libros junto con un mensaje de éxito
    return Response({
        'message': 'Correctly obtained books',
        'Books': serializer.data
    }, status=status.HTTP_200_OK)


# Logica para obtener un libro por su ID
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_book_by_pk(request, pk):
    try:
        # Intentar obtener el libro con el ID proporcionado
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({
            'message': 'Book not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Serializar los detalles del libro obtenido
    serializer = BookSerializer(book)
    
    # Devolver los detalles del libro junto con un mensaje de éxito
    return Response({
        'message': 'Correctly obtained book',
        'Book': serializer.data
    }, status=status.HTTP_200_OK)


# Logica para actualizar un libro
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_book(request, pk):
    try:
        # Intentar encontrar el libro con el ID proporcionado
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        # Si el libro no existe, devolver un mensaje de error con un estado 404
        return Response({
            'message': 'Book not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Crear un serializador para el libro con los datos proporcionados en la solicitud
    serializer = BookSerializer(book, data=request.data)
    
    # Verificar si los datos proporcionados son válidos
    if serializer.is_valid():
        # Si los datos son válidos, guardar el libro actualizado en la base de datos
        serializer.save()

        # Devolver un mensaje de éxito junto con los datos actualizados del libro
        return Response({
            'message': 'Book updated successfully',
            'Book': serializer.data
        }, status=status.HTTP_200_OK)
    
    # Si los datos no son válidos, devuelve un mensaje de error junto con los errores de validación
    return Response({
        'message': 'Error updating book',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# Logica para eliminar un libro
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_book(request, pk):
    try:
        # Intentar encontrar el libro con el ID proporcionado
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        # Si el libro no existe, devolver un mensaje de error
        return Response({
            'message': 'Book not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Si se encuentra el libro, eliminarlo de la base de datos
    book.delete()

    # Devolver un mensaje de éxito
    return Response({
        'message': 'Book deleted successfully'
    }, status=status.HTTP_204_NO_CONTENT)
