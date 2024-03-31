from django.contrib import admin
from django.urls import path, include


# Definimos las URLs globales
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user', include('users.urls')),
    path('api/books/', include('books_management.urls')),
    path('api/books/searchs/', include('book_search.urls'))
]
