from sentinelhub import SHConfig, SentinelHubRequest, DataCollection, MimeType, CRS, BBox, bbox_to_dimensions, DownloadRequest
from datetime import datetime
import numpy as np
from PIL import Image
import os

config = SHConfig()
config.sh_client_id = '44d5e92c-2c53-4320-8eb9-0be3fcf27a90'
config.sh_client_secret = '3SylUmrJFlD5LU9b5jOv1TopqjkhAStp'

if not config.sh_client_id or not config.sh_client_secret:
    print("Advertencia: 'sh_client_id' y 'sh_client_secret' no están configurados.")


# Define las coordenadas de la zona de interés (BBox)
coords = [[ -7.749786,42.222365], [ -7.748090,42.221778]]  # longitud, latitud de dos esquinas opuestas
zona_interes = BBox(bbox=coords, crs=CRS.WGS84)
dimensiones = bbox_to_dimensions(zona_interes, resolution=0.1)
print(dimensiones)

# Define el rango de fechas
fecha_inicio = '2024-01-01'
fecha_fin = datetime.now().strftime('%Y-%m-%d')  # Usa la fecha actual

# Crea el Evalscript
evalscript = """
//VERSION=3
function setup() {
    return {
        input: ["B04", "B03", "B02"],
        output: { bands: 3 }
    };
}

function evaluatePixel(sample) {
    return [sample.B04, sample.B03, sample.B02];
}
"""

output = {
    'width': 1024,
    'height': 1024,
    'responses': [
        {
            'identifier': 'default',
            'format': {
                'type': 'image/png'
            }
        }
    ]
}

# Crea la petición
request = SentinelHubRequest(
    
    data_folder='imagenes',
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=(fecha_inicio, fecha_fin),
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    bbox=zona_interes,
    size=dimensiones,
    config=config
)

# Carpeta para guardar la imagen
folder_name = 'imagenes'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Obtener datos y guardar imagen
data = request.get_data(save_data=True)

# # Si data es None o está vacío, no intentes guardar la imagen
# if data:
#     # Convertir la imagen en un objeto de Image de PIL para poder guardarla
#     # Suponiendo que 'image' es el arreglo NumPy que obtuviste
#     image_np = np.array(data[0])

#     # Convertir el arreglo NumPy en una imagen
#     img = Image.fromarray(image_np)

#     # Especificar el nombre del archivo y la ruta completa
#     file_path = os.path.join(folder_name, 'imagen_satelital.png')

#     # Guardar la imagen
#     img.save(file_path)
#     print(f"Imagen guardada en {file_path}")
# else:
#     print("No se recibieron datos de la imagen.")

