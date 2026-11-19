from django.urls import include, path

from . import views

app_name = 'users'
urlpatterns = [
    # Вход и выход: стандартные представления Django.
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]