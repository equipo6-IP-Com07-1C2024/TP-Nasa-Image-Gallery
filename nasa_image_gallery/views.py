# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail


# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, "index.html")


# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request, input=None):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)

    if input is None:
        images = services_nasa_image_gallery.getAllImages()
    else:
        images = services_nasa_image_gallery.getImagesBySearchInputLike(input)

        # si la busqueda no tiene resultados (images = []) asigno valores indicando que no se encontraron imagenes
        if not images:
            images = services_nasa_image_gallery.images_not_found()

    return images, favourite_list


# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    images = []
    favourite_list = []
    images, favourite_list = getAllImagesAndFavouriteList(request)
    return render(
        request, "home.html", {"images": images, "favourite_list": favourite_list}
    )


# función utilizada en el buscador.
def search(request):
    search_msg = request.POST.get("query", "")

    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    if search_msg:
        images, favourite_list = getAllImagesAndFavouriteList(request, search_msg)
    else:
        images, favourite_list = getAllImagesAndFavouriteList(request)

    return render(
        request,
        "home.html",
        {"images": images, "favourite_list": favourite_list, "search_msg": search_msg},
    )


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request) 

    return render(request, "favourites.html", {"favourite_list": favourite_list})


@login_required
def saveFavourite(request):
    services_nasa_image_gallery.saveFavourite(request)

    return search(request)


@login_required
def deleteFavourite(request):
    services_nasa_image_gallery.deleteFavourite(request)

    return redirect("favoritos")


@login_required
def exit(request):
    pass


def register(request):
    data = {"form": CustomUserCreationForm()}

    if request.method == "POST":
        formulario = CustomUserCreationForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()

            username = formulario.cleaned_data["username"]
            password = formulario.cleaned_data["password1"]
            user_email = formulario.cleaned_data["email"]

            user = authenticate(
                username=username,
                password=password,
            )

            # envío correo con las credenciales de inicio de sesión
            subject = "NASA Image Gallery - Registro exitoso"
            message = f"Gracias por registrarte\nTus datos de ingreso son:\nUsuario: {username}\nContaseña: {password}"
            recipient = user_email

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient],
                fail_silently=False,
            )
            messages.success(request, "¡Te has registrado exitosamente!")
            login(request, user)
            
            return redirect('home')
            
        data["form"] = formulario

    return render(request, "registration/signup.html", data)
