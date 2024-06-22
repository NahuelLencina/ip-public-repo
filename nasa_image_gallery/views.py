# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con 
# services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 

#============================================================
# Se implementan las herramientas necesarias para manejar 
# la autenticación
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse


from django.contrib import messages
from django.contrib.auth.models import User
#============================================================
from googletrans import Translator

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los 
# favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
#======================================================================================    
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
#======================================================================================
    return images, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un 
    # listado vacío [].
   #===================================================================================
    images, favourite_list = getAllImagesAndFavouriteList(request)
   #===================================================================================
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get('query', '')
    
    if not search_msg:
        search_msg = 'space'
    
    else:
        traduccion = Translator()
        traduccion = traduccion.translate(search_msg, src='es', dest='en')
        search_msg = traduccion.text
    
       # traduccion = traduccion.detect(search_msg).lang # Detectar el idioma
       # translation_result = traduccion.translate(search_msg,traduccion = traduccion.detect(search_msg).lang , dest='en')
       # search_msg = translation_result.text

    images= services_nasa_image_gallery.getImagesBySearchInputLike(search_msg)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )

    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, 
    # debe filtrar aquellas imágenes que posean el texto de búsqueda.
    

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirige a la función home después de un login exitoso
        else: # acá se desarrolla la logica para mostrar el usuario/contraseña incorrecto
            error = 'Usuario/Contraseña, Incorrecto' # Se carga en error la frase a mostrar
            return render(request, 'registration/login.html', {'error': error}) # se renderiza a la pagina Login
    return render(request, 'registration/login.html')
     
    
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        if password1 != password2:
            error = 'Las contraseñas son distintas.'
            return render(request, 'registration/register.html', {'error': error})
        
        if User.objects.filter(username=username).exists():
            error = 'Username is already taken.'
            return render(request, 'registration/login.html', {'error': error})
        
        if User.objects.filter(email=email).exists():
            error = 'Email address is already registered.'
            return render(request, 'registration/login.html', {'error': error})
        
        # Crear el usuario si todas las validaciones pasan
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        # Autenticar al usuario y redirigir a la página de inicio
        user = authenticate(username=username, password=password1)
        login(request, user)
        
        messages.success(request, f'Account created for {username}!')
        return redirect('home')  # Redirigir a la página de inicio o donde prefieras
    else:
        # Si es GET, mostrar el formulario vacío
        return render(request, 'registration/register.html')


  

# las siguientes funciones se utilizan para implementar la sección de favoritos: 
# traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request): 
        favourite_list = services_nasa_image_gallery.saveFavourite(request)
        return redirect(request.META.get('HTTP_REFERER', '/'))
      
@login_required
def deleteFavourite(request):
    favourite_list = services_nasa_image_gallery.deleteFavourite(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def exit(request):
    logout(request) 
    return redirect('home')  # Redirige a la página de inicio después de cerrar sesión