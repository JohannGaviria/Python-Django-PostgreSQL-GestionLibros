from django.urls import re_path
from . import views


# Definimos las URLs de la aplicación
urlpatterns = [
    re_path('signUp', views.signUp, name='signUp'),
    re_path('signIn', views.signIn, name='signIn'),
    re_path('signOut', views.signOut, name='signOut'),
]