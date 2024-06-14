from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('home/', views.home, name='home'),

    path('login/', views.login, name='login'),
    path('home/login/', views.login, name='login'),
    path('buscar/login/',views.login, name='login'),

    path('logout/', views.exit, name='login'),
    path('home/logout/', views.exit, name='login'), 
    path('buscar/logout/',views.exit, name='login'),
    path('favourites/logout',views.exit, name='login'),
 
    path('buscar/', views.search, name='buscar'),
    
    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
   
    #path('favourites/', views.deleteFavourite, name='borrar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),
    
    
    path('exit/', views.exit, name='exit'),
]
