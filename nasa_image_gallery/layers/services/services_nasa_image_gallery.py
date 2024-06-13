# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user




def getAllImages(input=None):
    # obtiene un listado de imágenes desde transport.py y lo guarda en un json_collection.
    # ¡OJO! el parámetro 'input' indica si se debe buscar por un valor introducido en el buscador.

    json_collection = transport.getAllImages(input)  # Si input es necesario, pásalo a la función de transporte

    images = []
#=========================================================================
    # recorre el listado de objetos JSON, lo transforma en una NASACard y 
    # lo agrega en el listado de images. Ayuda: ver mapper.py.
    for json in json_collection:
        nasa_card = mapper.fromRequestIntoNASACard(json)
        images.append(nasa_card)
#=========================================================================
    return images


def getImagesBySearchInputLike(input):
    return getAllImages(input)


# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
#========================================================================
        favourite_Usuario = repositories.getAllFavouritesByUser(user)     # buscamos desde el repositorio TODOS los favoritos del usuario 
                                                       #(variable 'user').
        list_favourites = []

        for favourite in favourite_Usuario:
            nasa_card = mapper.fromRepositoryIntoNASACard(favourite) # transformamos cada favorito en una NASACard, y lo almacenamos en nasa_card.
            list_favourites.append(nasa_card)
#========================================================================
        return list_favourites

#================================================================
# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = mapper.fromTemplateIntoNASACard(request) # transformamos un request del template en una NASACard.
    fav.user = request.user  # le seteamos el usuario correspondiente.
    return repositories.saveFavourite(fav) # lo guardamos en la base.


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.
    