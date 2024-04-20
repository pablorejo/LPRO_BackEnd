# Vamos a procesar los datos obtenidos.
import pandas as pd
import numpy as np
from conf import *
from shapely.geometry import Point, Polygon

def haversine(lon1, lat1, lon2, lat2):
    """
    Calcula la distancia del círculo grande entre dos puntos en la Tierra.
    """
    # convertir grados decimales a radianes
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # fórmula haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371 # Radio de la Tierra en kilómetros. Usa 3956 para millas
    return c * r

anomalias = False

timer_15min_entrar = False
instancia_fecha_15min_entrar = None

timer_5h_estancia = False
instancia_fecha_5h_estancia = None

timer_15min_salir = False
instancia_fecha_15min_salir = None

anomalias = []

posibles_anomalias = []

poligonos = []

diccionario_vacas_fuera = {
    '1001': False,
    '1002': False,
    '1003': False,
    '1004': False,
    '1005': False,
    '1006': False,
    '1007': False,
    '1008': False,
    '1009': False
}




# Convertir el diccionario en una lista de parcelas, donde cada parcela es representada por su lista de coordenadas
parcelas = obtener_parcelas()

for parcela in parcelas:
    poligonos.append(Polygon(parcela))
    
df_anomalias = pd.DataFrame()

def guardar_anomalia(anomalia):
    """Se guarda la anomalia y se notifica al usuario"""
    df_anomalias = pd.concat([df_anomalias, anomalia], ignore_index=True)
    pass

def guardar_posibles_anomalias():
    for anomalia in posibles_anomalias:
        guardar_anomalia(anomalia)


def dato_fuera(poin):
    fuera_parcela = False
    for poligono in poligonos:
        if not poligono.contains(poin):
            fuera_parcela = True
    return fuera_parcela

def estan_todos_fuera():
    """
        Devuelve true en caso de que todos estean fuera y false en caso contrario
    """
    estan_fuera = True
    for numero_pendiente, fuera in diccionario_vacas_fuera.items():
        if (not fuera):
            estan_fuera = False
            break
            
    return estan_fuera

segundos_pastando = {}
segundos_descansando = {}
segundos_caminando = {}
def añadir_segundos_pastando(numero_pendiente):
    global segundos_pastando
    if not numero_pendiente in segundos_pastando:
        
        segundos_pastando[numero_pendiente] = 0
    
    segundos_pastando[numero_pendiente] += 10
    
def añadir_segundos_descansando(numero_pendiente):
    global segundos_descansando
    if not numero_pendiente in segundos_descansando:
        segundos_descansando[numero_pendiente] = 0
    
    segundos_descansando[numero_pendiente] += 10
    
def añadir_segundos_caminando(numero_pendiente):
    global segundos_caminando
    if not numero_pendiente in segundos_caminando:
        segundos_caminando[numero_pendiente] = 0
    
    segundos_caminando[numero_pendiente] += 10
    

puntos_30_anteriores = []
def analizar_dato(gps):
    if (len(puntos_30_anteriores) >= 1):
        puntos_30_anteriores.pop(0)
        
    # Vamos a analizar la velocidad media de la vaca durante 5 min
    puntos_30_anteriores.append(gps)
    
    # Calculamos velocidad media de estos puntos
    velocidad = 0
    for punto in puntos_30_anteriores:
        velocidad += punto['velocidad_en_m/s']
    velocidad = velocidad / len(puntos_30_anteriores)
    
    # Suponiendo que gps es un DataFrame y 'velocidad' es una variable previamente calculada
    
    
    numero_pendiente = gps['Numero_pendiente']
    if (velocidad <= 1/20 and velocidad >= 1/30):
        añadir_segundos_pastando(numero_pendiente)
    elif(velocidad > 1/20):
        añadir_segundos_caminando(numero_pendiente)
    elif velocidad < 1/30:
        añadir_segundos_descansando(numero_pendiente)
    
    return velocidad

velocidades_medias = []
def analizar_dato_gps(gps,gps_anterior):
    
    global anomalias 

    global timer_15min_entrar 
    global instancia_fecha_15min_entrar 

    global timer_5h_estancia 
    global instancia_fecha_5h_estancia 

    global timer_15min_salir 
    global instancia_fecha_15min_salir 

    global anomalias 

    global posibles_anomalias 

    global poligonos 

    global diccionario_vacas_fuera
    global velocidades_medias
    gps_point = Point(gps['latitude'],gps['longitude'])
    gps_anterior_point = Point(gps_anterior['latitude'],gps_anterior['longitude'])
    
    
    # Actualizamos en timer
    if (timer_15min_entrar):
        quince_minutos = timedelta(minutes=15)
        diferencia = gps['fecha'] - instancia_fecha_15min_entrar
        if diferencia > quince_minutos:
            timer_15min_entrar = False
            anomalias = False
            
    if(timer_15min_salir):
        if (estan_todos_fuera()):
            posibles_anomalias.clear()
            quince_minutos = timedelta(minutes=15)
            diferencia = gps['fecha'] - instancia_fecha_15min_salir
            if diferencia > quince_minutos:
                timer_15min_entrar = False
                anomalias = False
        else:
            guardar_posibles_anomalias()
            timer_15min_salir = False
            
    if(timer_5h_estancia):
        cinco_horas = timedelta(hours=5)
        diferencia = gps['fecha'] - instancia_fecha_5h_estancia
        if diferencia > cinco_horas:
            timer_5h_estancia = False
            anomalias = True
        
    # Si el punto actual esta fuera
    if dato_fuera(gps_point):
        # Si la deteccion de anomalias está habilitada
        if anomalias:
            guardar_anomalia(gps)
            velocidades_medias.append(analizar_dato(gps))
        # Si la deteccion de anomalias está deshabilitada
        else:
            if not dato_fuera(gps_anterior_point):
                if timer_15min_salir:
                    # Hay que guardar el punto en posibles anomalias y si al terminar el timer estan todas las vacas fuera pues se elimina sino se notifican las posibles anomalias
                    posibles_anomalias.append(gps)
                    pass 
                elif not timer_15min_entrar:
                    # por otra parte si no esta el timer encendido se enciende
                    timer_15min_salir = True
                    instancia_fecha_15min_salir = gps['fecha']
                else:
                    pass
            else:
                if timer_15min_salir:
                    posibles_anomalias.append(gps) 
            velocidades_medias.append(0)
            
        diccionario_vacas_fuera[gps['Numero_pendiente']] = True
        
    # Si el punto actual está dentro
    else: 
        if dato_fuera(gps_anterior_point):
            if timer_15min_entrar and not timer_15min_salir:
                pass
            elif not timer_15min_salir:
                timer_15min_entrar = True
                instancia_fecha_15min_entrar = gps['fecha']
            else:
                pass
        else:
            pass
        
        velocidades_medias.append(analizar_dato(gps))
        diccionario_vacas_fuera[gps['Numero_pendiente']] = False
    return gps_anterior
        
def redondear_fecha_hora(dt):
    # Redondea a la cantidad de segundos más cercana, múltiplo de 10
    segundos_para_sumar = (5 - dt.second % 5) % 5
    if segundos_para_sumar == 0 and dt.microsecond > 0:
        segundos_para_sumar = 5
    # Ajustar el microsegundo a cero para no tener en cuenta subsegundos
    return dt + timedelta(seconds=segundos_para_sumar) - timedelta(microseconds=dt.microsecond)


data = pd.read_csv('datos.csv')
data['fecha'] = pd.to_datetime(data['fecha'])
data['fecha'] = data['fecha'].apply(redondear_fecha_hora)          

data = data.sort_values(by=['Numero_pendiente', 'fecha'])

# Calcular la distancia y la velocidad
distancias = []
velocidades = []
fuera_de_parcela = []

for i in range(1, len(data)):
    row_prev = data.iloc[i-1]
    row = data.iloc[i]

    guardar = True
    
    try:
        guardar = row_prev['Numero_pendiente'] == row['Numero_pendiente'] 
    except: 
        guardar = False
    
    if (guardar):
        distancia = haversine(row_prev['longitude'], row_prev['latitude'], row['longitude'], row['latitude'])
        tiempo = ( row['fecha'] -row_prev['fecha']).total_seconds()  # Tiempo en horas
        velocidad = distancia * 1000 / tiempo if tiempo > 0 else 0
        distancias.append(distancia)
        velocidades.append(velocidad)
    else:
        velocidades.append(0)
        distancias.append(0)
    
    fuera_parcela = True
    for poligono in poligonos:
        fuera_parcela = not poligono.contains(Point(row_prev['latitude'],row_prev['longitude']))
    fuera_de_parcela.append(fuera_parcela)
    
    

# Añadir la distancia y velocidad calculada al DataFrame (asumiendo la primera velocidad y distancia como 0)
data['distancia_en_Km'] = [0] + distancias
data['velocidad_en_m/s'] = [0] + velocidades
    
# linea = data.iloc[len(data)-1]

# fuera_de_parcela.append(poligono_parcela.contains(Point(linea['latitude'],linea['longitude'])))

fuera_parcela = True
for poligono in poligonos:
    fuera_parcela = not poligono.contains(Point(row_prev['latitude'],row_prev['longitude']))
fuera_de_parcela.append(fuera_parcela)
    
data['fuera_del_recinto'] = fuera_de_parcela

# Calcular la distancia total recorrida
distancia_total = sum(distancias)


# Calcular la posición promedio de todo el ganado en cada instante
data['pos_promedio_lat'] = data.groupby('fecha')['latitude'].transform('mean')
data['pos_promedio_lon'] = data.groupby('fecha')['longitude'].transform('mean')

# Calcular la distancia de cada vaca a la posición promedio
data['distancia_a_promedio'] = data.apply(lambda row: haversine(row['longitude'], row['latitude'], 
                                                                 row['pos_promedio_lon'], row['pos_promedio_lat']), axis=1)

# Definir un umbral para considerar una vaca "muy alejada"
umbral_distancia = data['distancia_a_promedio'].quantile(0.95) #vamos a especificar que es raro si esta por encima del percentil 95%

# Identificar las instancias donde una vaca está muy alejada del resto
vacas_alejadas = data[data['distancia_a_promedio'] > umbral_distancia]
data.to_csv('distancias.csv',index=False)

columnas = ['Numero_pendiente','latitude','longitude','fecha','fuera_del_recinto','distancia_en_Km','velocidad_en_m/s','pos_promedio_lat','pos_promedio_lon','distancia_a_promedio','velocidad_media_30_anteriors']



for i in range(1, len(data)):
    row_prev = data.iloc[i-1]
    row = data.iloc[i]
    analizar_dato_gps(row,row_prev) 

data['velocidad_media_30_anteriors'] = [0] + velocidades_medias
# Opcional: Guardar los resultados en un nuevo archivo CSV
# data.to_csv('ruta_a_tu_archivo_con_resultados.csv', index=False)

data = data[columnas]
data.to_csv('datos_procesados.csv',index=False)
print(f"\nDistancia total recorrida: {distancia_total} km\n")

print("segundos_pastando: " + str(segundos_pastando) + "\n")
print("segundos_descansando: " + str(segundos_descansando) + "\n")
print("segundos_caminando: " + str(segundos_caminando) + "\n")
