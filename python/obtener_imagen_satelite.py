import requests
from PIL import Image
from io import BytesIO

# Tu clave API de Google Maps
api_key = "TU_CLAVE_API_AQUI"

# Coordenadas del centro de la imagen deseada
latitud = 42.222722
longitud = -7.748667

# Nivel de zoom
zoom = 17

# Tamaño de la imagen (max 640x640 para usuarios gratuitos)
tamaño = "640x640"

# Construir la URL para la API de Google Maps Static
url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitud},{longitud}&zoom={zoom}&size={tamaño}&maptype=satellite&key={api_key}"

# Realizar la solicitud a la API
respuesta = requests.get(url)

# Verificar si la solicitud fue exitosa
if respuesta.status_code == 200:
    # Abrir la imagen utilizando BytesIO
    img = Image.open(BytesIO(respuesta.content))
    # Mostrar la imagen
    img.show()
else:
    print("Error al obtener la imagen:", respuesta.status_code)
