# mapper: se refiere a un componente o conjunto de funciones que se utiliza para convertir o "mapear" datos de un formato o estructura a otro. Esta conversión se realiza típicamente cuando se trabaja con diferentes capas de una aplicación, como por ejemplo, entre la capa de datos y la capa de presentación, o entre dos modelos de datos diferentes, mejorando la coherencia y eficiencia.

from nasa_image_gallery.layers.generic.nasa_card import NASACard

# usado cuando la info. viene de la API de la nasa, para transformarlo en una NASACard.
# 
def fromRequestIntoNASACard(object):
    data = object.get('data', [])
    links = object.get('links', [])

    # Verificamos que 'data' no esté vacío y contenga 'title' y 'date_created'
    if data and isinstance(data, list) and len(data) > 0:
        title = data[0].get('title', 'Título no disponible')
        description = data[0].get('description', 'Descripción no disponible')
        date = data[0].get('date_created', '')[:10]  # Tomamos solo los primeros 10 caracteres
    else:
        title = 'Título no disponible'
        description = 'Descripción no disponible'
        date = ''

    # Verificamos que 'links' tenga al menos un elemento y contenga 'href'
    image_url = links[0].get('href', '') if links and isinstance(links, list) and len(links) > 0 else ''

    return NASACard(
        title=title,
        description=description,
        image_url=image_url,
        date=date
    )




# usado cuando la info. viene del template, para transformarlo en una NASACard antes de guardarlo en la base de datos.
def fromTemplateIntoNASACard(templ): 
    nasa_card = NASACard(
                        title=templ.POST.get("title"),
                        description=templ.POST.get("description"),
                        image_url=templ.POST.get("image_url"),
                        date=templ.POST.get("date")
                )
    return nasa_card


# cuando la info. viene de la base de datos, para transformarlo en una NASACard antes de mostrarlo.
def fromRepositoryIntoNASACard(repo_dict):
    nasa_card = NASACard(
                        id=repo_dict['id'],
                        title=repo_dict['title'],
                        description=repo_dict['description'],
                        image_url=repo_dict['image_url'],
                        date=repo_dict['date'],
                )
    return nasa_card