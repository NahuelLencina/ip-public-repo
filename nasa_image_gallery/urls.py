from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('home/', views.home, name='home'),

    # Rutas de inicio de sesión
    path('login/', views.login, name='login'),
    path('home/login/', views.login, name='login'),
    path('buscar/login/', views.login, name='login'),

    # Rutas de cierre de sesión
    path('logout/', views.exit, name='logout'),
    path('home/logout/', views.exit, name='logout'),
    path('buscar/logout/', views.exit, name='logout'),
    path('favourites/logout/', views.exit, name='logout'),

    # Ruta de búsqueda
    path('buscar/', views.search, name='buscar'),

    # Rutas de favoritos
    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    # Rutas de registro
    path('register/', views.register, name='register'),
    path('login/register/', views.register, name='register'),
    path('home/register/', views.register, name='register'),
    path('register/home', views.register, name='register'),
    # Ruta de salida
    path('exit/', views.exit, name='exit'),
]
