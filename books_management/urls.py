from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_book, name='create_book'),
    path('all', views.get_all_books, name='get_all_books'),
    path('<int:pk>', views.get_book_by_pk, name='get_book_by_pk'),
    path('update/<int:pk>', views.update_book, name='update_book'),
    path('delete/<int:pk>', views.delete_book, name='delete_book'),
]
