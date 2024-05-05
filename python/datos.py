import pandas as pd
import requests
from openai import OpenAI 
from conf import obtener_engine

def send_notification(title, message):
    # URL del servidor FCM:
    url_send = 'https://fcm.googleapis.com/fcm/send'

    # Token:
    notification_id = "APA91bGqLdpBmh0c5cbdlbR6VfSx93Ov17s5ZY6m8XViJIIZYbPPxiuMVqsvRN2HeXsNkITNfihvZJf0If4Uf_lZCZbMZnKcmGM8rJF-wf4Jkt19WMOVXDE"

    # Clave del servidor FCM
    server_key = 'AAAAvwb3TCE:APA91bH5ljrS5_Hzk1pvWpmpLMLYDaq1UPJ7ssnvtjHh5qZev7G2qc-5-H3cWZuxy2LYSuGRS_T_8M4dlHyawhzIXSbJQGkz3FZrp6ezhlrEv96qwotwd0pzU3mgDN9vgyIpG4c6W635'

    # Datos del mensaje:
    message_data = {
        'to': notification_id,
        'data': {
            'title': title,
            'message': message
        }
    }

    # Cabeceras de la petición HTTP
    headers = {
        'Authorization': 'key=' + server_key,
        'Content-Type': 'application/json'
    }

    # Realizar la petición HTTP
    response = requests.post(url_send, json=message_data, headers=headers)

    # Procesar la respuesta
    if response.status_code == 200:
        return 'Notificación enviada correctamente: ' + response.text
    else:
        return 'Error al enviar la notificación: ' + response.text
def asteriksCall(numero_Pendiente):
    # URL a la que deseas enviar la solicitud POST
    url = 'http://172.20.10.9/llamada'
    url = 'http://localhost/llamada'

    # Datos que deseas enviar en la solicitud POST (en formato de diccionario)
    datos = {
        'numeroPendiente': numero_Pendiente,
    }

    # Realizar la solicitud POST utilizando requests.post
    respuesta = requests.post(url, data=datos)


#source openai-env/bin/activate
client = OpenAI(api_key='sk-proj-Q56erkoH5sWNO8TkPDwkT3BlbkFJ19C4VEYyzPvunJVGcUs1')# defaults to getting the key using os.environ.get("OPENAI_API_KEY")

def chatCall(input):


    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    #response_format={ "type": "json_object" },
    #libertad del modelo
    temperature=0,
    max_tokens=100,
    #top_p=1,
    #frequency_penalty=0.5,
    #presence_penalty=0,
    messages=[
        
        {"role": "user", 
        "content":input}
    ]
    )
    return(response.choices[0].message.content)

# Cargar los datos desde el archivo CSV
query = """
SELECT * FROM gps
WHERE fecha >= NOW() - INTERVAL 1 MINUTE
"""

# query = """
# SELECT * FROM gps
# """
datos = pd.read_sql_query(query,obtener_engine())
#print(datos)
valores_unicos_pendiente = datos['Numero_pendiente'].unique()

selected_columns = datos[['Numero_pendiente', 'fecha','velocidad']]
#print(selected_columns)
#resultado = chatCall("datos donde el numero pendiente es el id de la vaca y y la velocidad es la velocidad en el momento fecha "+ selected_columns.to_string() +" hay alguna anomalia en la velocidad de las vacas y por que puede ser producida")
#print(resultado)


# Filtrar las filas donde la columna "fuera_del_recinto" sea verdadera
fuera_del_recinto = datos[datos['fuera_del_recinto'] == True]
# Obtener los ID de las vacas fuera del recinto
ids_fuera_del_recinto = fuera_del_recinto['Numero_pendiente'].unique()

# vacas_alejadas = datos[datos['vacas_alejadas'] == True]
# # Obtener los ID de las vacas fuera del recinto
# ids_vacas_alejadas = vacas_alejadas['Numero_pendiente'].unique()

# Calcular la velocidad media y la desviación estándar
velocidad_media = datos['velocidad'].mean()
desviacion_estandar = datos['velocidad'].std()

# Definir el umbral de desviación estándar (por ejemplo, 2)
umbral_desviacion = datos['velocidad'].quantile(0.95)

# Calcular los límites superior e inferior
limite_superior = velocidad_media + (umbral_desviacion * desviacion_estandar)
limite_inferior = velocidad_media - (umbral_desviacion * desviacion_estandar)
if limite_inferior < 0:
    limite_inferior = 0
# Filtrar los valores que están más allá de los límites superior e inferior
#valores_muy_alejados = datos[(datos['velocidad'] > limite_superior) | (datos['velocidad'] <= limite_inferior)]
print(limite_superior,umbral_desviacion,desviacion_estandar)
valores_altos =datos[(datos['velocidad'] > limite_superior)]
# Filtrar los valores que están más allá del límite inferior
valores_bajos =datos[(datos['velocidad'] <= limite_inferior)]

# Iterar sobre los valores altos
chat=chatCall("causas y medidas para una vaca que ha corrido")

# print(len(valores_altos))
# for index, fila in valores_altos.iterrows():
#     # Trabajar con la fila
#     send_notification("Vaca "+ str(fila['Numero_pendiente'])+" velocidade elevada", chat )
#     break 
    # Por ejemplo, acceder a un valor específico de la fila
    # valor_fecha = fila['fecha']
    # valor_velocidad = fila['velocidad']
    # Realizar más operaciones según tus necesidades

# # Iterar sobre los valores bajos
# chat2=chatCall("causas y medidas para una vaca no se mueva")
# print(chat2)
# for index, fila in valores_bajos.iterrows():
#     # Trabajar con la fila
#     send_notification("Vaca "+ str(fila['Numero_pendiente'])+" detectada anomalia","La Vaca "+ str(fila['Numero_pendiente'])+" esta parada a las "+str(fila['fecha'])+ chat2 )
#     # Realizar operaciones adicionales si es necesario

# Iterar sobre los IDs de vacas alejadas
# for id_vaca in ids_vacas_alejadas:
#     # Trabajar con el ID de la vaca
#     send_notification("Vaca "+str(id_vaca) +" muy alejada de las demás.","Vaca "+str(id_vaca) +" muy alejada de las demás.")
#     # Realizar operaciones adicionales si es necesario

# Iterar sobre los IDs de vacas fuera del recinto
# ids_fuera_del_recinto = [5]
for id_vaca in ids_fuera_del_recinto:
    # Trabajar con el ID de la vaca
    send_notification("Vaca "+str(id_vaca)+" fuera del recinto.","Vaca "+str(id_vaca)+" fuera del recinto.")
    asteriksCall(str(id_vaca))
    # Realizar operaciones adicionales si es necesario









