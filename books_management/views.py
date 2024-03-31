from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Book
from .serializers import BookSerializer


# Decorador personalizado para verificar si el usuario es propietario del libro
def check_book_owner(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            # Intenta obtener el libro basado en la clave primaria (pk) proporcionada en los argumentos de la solicitud
            book = Book.objects.get(pk=kwargs['pk'])
        except Book.DoesNotExist:
            # Si el libro no existe, devuelve una respuesta con el mensaje de error correspondiente
            return Response({
                'message': 'Book not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Comprueba si el usuario actual es propietario del libro
        if book.user != request.user:
            # Si el usuario no es el propietario, devuelve una respuesta de error de permiso
            return Response({
                'message': 'You are not allowed to access this book'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Si el usuario es propietario, llama a la función de vista original con los mismos argumentos
        return view_func(request, *args, **kwargs)
    
    return wrapper


# Vista para la creación de un nuevo libro
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_book(request):
    # Serializar los datos recibidos en la solicitud
    serializer = BookSerializer(data=request.data)

    # Verifica si los datos son válidos según las reglas definidas en el serializador
    if serializer.is_valid():
        # Guarda los datos serializados asociándolos al usuario actual
        serializer.save(user=request.user)

        # Devuelve una respuesta con un mensaje de éxito y los datos del libro creado
        return Response({
            'message': 'Successfully created book',
            'Book': serializer.data
        }, status=status.HTTP_201_CREATED)

    # Si los datos no son válidos, devuelve un mensaje de error y los errores de validación
    return Response({
        'message': 'Error when creating the book',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# Vista para obtener todos los libros asociados al usuario actual
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_books(request):
    # Filtra los libros pertenecientes al usuario actual
    books = Book.objects.filter(user=request.user)

    # Si no se encuentran libros, devuelve un mensaje de error
    if not books:
        return Response({
            'message': 'Books not found for the current user'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Serializa los libros encontrados y devuelve una respuesta con ellos
    serializer = BookSerializer(books, many=True)

    return Response({
        'message': 'Correctly obtained books for the current user',
        'Books': serializer.data
    }, status=status.HTTP_200_OK)


# Vista para obtener un libro específico por su clave primaria (pk)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_book_owner
def get_book_by_pk(request, pk):
    # Obtiene el libro por su clave primaria (pk)
    book = Book.objects.get(pk=pk)

    # Serializa el libro encontrado y devuelve una respuesta con él
    serializer = BookSerializer(book)

    return Response({
        'message': 'Correctly obtained book',
        'Book': serializer.data
    }, status=status.HTTP_200_OK)


# Vista para actualizar un libro existente
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_book_owner
def update_book(request, pk):
    # Obtiene el libro por su clave primaria (pk)
    book = Book.objects.get(pk=pk)

    # Serializa el libro con los datos proporcionados en la solicitud
    serializer = BookSerializer(book, data=request.data)

    # Si los datos son válidos, guarda el libro actualizado y devuelve una respuesta de éxito
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Book updated successfully',
            'Book': serializer.data
        }, status=status.HTTP_200_OK)
    
    # Si los datos no son válidos, devuelve un mensaje de error y los errores de validación
    return Response({
        'message': 'Error updating book',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# Vista para eliminar un libro existente
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_book_owner
def delete_book(request, pk):
    # Obtiene el libro por su clave primaria (pk)
    book = Book.objects.get(pk=pk)

    # Elimina el libro de la base de datos
    book.delete()

    # Devuelve una respuesta indicando que el libro ha sido eliminado con éxito
    return Response({
        'message': 'Book deleted successfully'
    }, status=status.HTTP_204_NO_CONTENT)
