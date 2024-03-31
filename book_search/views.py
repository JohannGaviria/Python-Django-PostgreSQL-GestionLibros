from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from books_management.models import Book


# Logica para buscar libros por titulo, autor o genero
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_books(request):
    # Obtener el parámetro de búsqueda de la solicitud
    query = request.GET.get('query')

    # Comprobar si no se proporciona ningún parámetro de búsqueda
    if not query:
        return Response({
            'message': 'incorrect search parameters'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Realizar la consulta para encontrar libros que coincidan con el título, autor o género
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__full_name__icontains=query) |
        Q(genre__genre__icontains=query)
    ).distinct()

    # Si el parametro de busqueda devuelve libros que no existe, devolver un mensaje de error
    if not books:
        return Response({
            'message': 'No books found matching your search'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Serializar los libros encontrados para prepararlos para la respuesta
    serialized_books = []
    for book in books:
        serialized_book = {
            'id': book.id,
            'title': book.title,
            'author': {
                'id': book.author.id,
                'full_name': book.author.full_name,
                'email': book.author.email
            },
            'genres': [{'id': genre.id, 'genre': genre.genre} for genre in book.genre.all()],
            'publication_year': book.publication_year
        }
        serialized_books.append(serialized_book)

    # Devolver los detalles de los libros junto con un mensaje de éxito
    return Response({
        'message': 'Correctly obtained books',
        'Books': serialized_books
    }, status=status.HTTP_200_OK)