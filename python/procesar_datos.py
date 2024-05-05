# Vamos a procesar los datos obtenidos.
import pandas as pd
import numpy as np
from conf import *
from shapely.geometry import Point, Polygon
from os import path
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

def guardar_anomalia(anomalia):
    """Se guarda la anomalia y se notifica al usuario"""
    global anomalias_verdaderas
    anomalias_verdaderas.append(anomalia)

def guardar_posibles_anomalias():
    for anomalia in posibles_anomalias:
        guardar_anomalia(anomalia)


def dato_fuera(poin):
    global parcelas_dict
    fuera_parcela = True
    id = None
    for id_parcela, puntos in parcelas_dict.items():
        poligono = Polygon(puntos)
        if poligono.contains(poin):
            fuera_parcela = False
            id = id_parcela
            break
        else:
            id = None
    return fuera_parcela,id

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


def añadir_segundos_pastando(numero_pendiente):
    global segundos_pastando
    if not numero_pendiente in segundos_pastando:
        
        segundos_pastando[numero_pendiente] = 0
    
    segundos_pastando[numero_pendiente] += MINUTOS * 60
    
def añadir_segundos_descansando(numero_pendiente):
    global segundos_descansando
    if not numero_pendiente in segundos_descansando:
        segundos_descansando[numero_pendiente] = 0
    
    segundos_descansando[numero_pendiente] += MINUTOS * 60
    
def añadir_segundos_caminando(numero_pendiente):
    global segundos_caminando
    if not numero_pendiente in segundos_caminando:
        segundos_caminando[numero_pendiente] = 0
    
    segundos_caminando[numero_pendiente] += MINUTOS * 60
    

def analizar_dato(gps):
    if (len(puntos_30_anteriores) >= 3):
        puntos_30_anteriores.pop(0)
        
    # Vamos a analizar la velocidad media de la vaca durante 5 min
    puntos_30_anteriores.append(gps)
    # Calculamos velocidad media de estos puntos
    velocidad = 0
    for punto in puntos_30_anteriores:
        velocidad += punto['velocidad']
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

def analizar_dato_gps(gps,gps_anterior,indices_parcela):
    
    global timer_15min_entrar 
    global instancia_fecha_15min_entrar 

    global timer_5h_estancia 
    global instancia_fecha_5h_estancia 

    global timer_15min_salir 
    global instancia_fecha_15min_salir 

    global anomalias_bool 

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
            anomalias_bool = False
            
    if(timer_15min_salir):
        if (estan_todos_fuera()):
            posibles_anomalias.clear()
            quince_minutos = timedelta(minutes=15)
            diferencia = gps['fecha'] - instancia_fecha_15min_salir
            if diferencia > quince_minutos:
                timer_15min_entrar = False
                anomalias_bool = False
        else:
            guardar_posibles_anomalias()
            timer_15min_salir = False
            
    if(timer_5h_estancia):
        cinco_horas = timedelta(hours=5)
        diferencia = gps['fecha'] - instancia_fecha_5h_estancia
        if diferencia > cinco_horas:
            timer_5h_estancia = False
            anomalias_bool = True
    
    # Si el punto actual esta fuera
    dato_actual_fuera , id_parcela_dato_actual = dato_fuera(gps_point)
    dato_anerior_fuera, id_parcela_dato_anterior = dato_fuera(gps_anterior_point)
    if dato_actual_fuera:
        # Si la deteccion de anomalias está habilitada
        if anomalias_bool:
            guardar_anomalia(gps)
            velocidades_medias.append(analizar_dato(gps))
        # Si la deteccion de anomalias está deshabilitada
        else:
            if not dato_anerior_fuera:
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
        indices_parcela.append(id_parcela_dato_anterior)
        diccionario_vacas_fuera[gps['Numero_pendiente']] = True
        
    # Si el punto actual está dentro
    else: 
        if dato_anerior_fuera:
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
        indices_parcela.append(id_parcela_dato_actual)
        diccionario_vacas_fuera[gps['Numero_pendiente']] = False
    return gps_anterior,velocidades_medias
        
def redondear_fecha_hora(dt):
    # Redondea a la cantidad de segundos más cercana, múltiplo de 10
    segundos_para_sumar = (5 - dt.second % 5) % 5
    if segundos_para_sumar == 0 and dt.microsecond > 0:
        segundos_para_sumar = 5
    # Ajustar el microsegundo a cero para no tener en cuenta subsegundos
    return dt + timedelta(seconds=segundos_para_sumar) - timedelta(microseconds=dt.microsecond)

def obtener_primer_procesado(df_datos_gps):
    # Calcular la distancia y la velocidad
    distancias = []
    velocidades = []
    fuera_de_parcela = []

    for i in range(1, len(df_datos_gps)):
        row_prev = df_datos_gps.iloc[i-1]
        row = df_datos_gps.iloc[i]
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
    df_datos_gps['distancia_en_Km'] = [0] + distancias
    df_datos_gps['velocidad'] = [0] + velocidades
    
    fuera_parcela = True
    for poligono in poligonos:
        fuera_parcela = not poligono.contains(Point(row_prev['latitude'],row_prev['longitude']))
    fuera_de_parcela.append(fuera_parcela)
        
    df_datos_gps['fuera_del_recinto'] = fuera_de_parcela

    # Calcular la distancia total recorrida
    return sum(distancias)
    
def calcular_velocidades_medias(df_datos_gps):
    # Calcular la posición promedio de todo el ganado en cada instante
    df_datos_gps['pos_promedio_lat'] = df_datos_gps.groupby('fecha')['latitude'].transform('mean')
    df_datos_gps['pos_promedio_lon'] = df_datos_gps.groupby('fecha')['longitude'].transform('mean')

    # Calcular la distancia de cada vaca a la posición promedio
    df_datos_gps['distancia_a_promedio'] = df_datos_gps.apply(lambda row: haversine(row['longitude'], row['latitude'], 
                                                                    row['pos_promedio_lon'], row['pos_promedio_lat']), axis=1)

    # Definir un umbral para considerar una vaca "muy alejada"
    umbral_distancia = df_datos_gps['distancia_a_promedio'].quantile(0.95) #vamos a especificar que es raro si esta por encima del percentil 95%

    # Identificar las instancias donde una vaca está muy alejada del resto
    df_datos_gps['vacas_alejadas'] = df_datos_gps['distancia_a_promedio'] > umbral_distancia

    # data.to_csv('distancias.csv',index=False)

    
    
if __name__ == "__main__":
    anomalias_bool = False

    timer_15min_entrar = False
    instancia_fecha_15min_entrar = None

    timer_5h_estancia = False
    instancia_fecha_5h_estancia = None

    timer_15min_salir = False
    instancia_fecha_15min_salir = None

    anomalias_verdaderas = []

    posibles_anomalias = []

    poligonos = []

    # Obtenemos los id de las vacas
    df_vacas = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_VACAS))
    df_vacas.to_csv(path.join(CARPETA_DATOS_CSV,'vacas.csv'),index=False)   
    vacas_id = list(df_vacas['Numero_pendiente'].to_numpy())
    
    #Diccionario con los datos de si la vaca se encuentra fuera o dentro
    diccionario_vacas_fuera = {str(numero): False for numero in vacas_id}


    # Obtenemos las parcelas
    if (parcelas == None):
        df_parcelas = pd.read_csv(path.join(CARPETA_DATOS_CSV,'parcelas.csv'))
        parcelas_dict = df_parcelas.groupby('id_parcela').apply(
                lambda x: list(zip(x.latitude, x.longitude))
            ).to_dict()
        parcelas = list(parcelas_dict.values())
    else:
        parcelas_dict = {}
        for k in range(len(parcelas)):
            parcelas_dict[k] = parcelas[k]

    # Creamos los poligonos
    for parcela in parcelas:
        poligonos.append(Polygon(parcela))
        
        
    df_anomalias = pd.DataFrame()


    segundos_pastando = {} # Diccionario donde se guarda el id de la vaca y los segundos que esta esta pastando
    segundos_descansando = {} # Diccionario donde se guarda el id de la vaca y los segundos que esta esta descansando
    segundos_caminando = {} # Diccionario donde se guarda el id de la vaca y los segundos que esta esta caminando
    puntos_30_anteriores = [] # Diccionario donde se guarda el id de la vaca y los ultimos 30 puntos anteriores


    # Obtenemso los datos gps sin procesar
    df_datos_gps = pd.read_csv(path.join(CARPETA_DATOS_CSV,'datos.csv'))
    df_datos_gps['fecha'] = pd.to_datetime(df_datos_gps['fecha']) 
    df_datos_gps['fecha'] = df_datos_gps['fecha'].apply(redondear_fecha_hora)           
    df_datos_gps = df_datos_gps.sort_values(by=['Numero_pendiente', 'fecha']) # Los agrupamos por id y fecha
    
    
    # linea = data.iloc[len(data)-1]
    distancia_total = obtener_primer_procesado(df_datos_gps)
    
    # Añadimos al df las velocidades medias
    calcular_velocidades_medias(df_datos_gps)

    
    # Ahora vamos a procesar dato a datos para encontrar anomalias y otras cosas
    velocidades_medias = [] 
    indices_parcela = []
    for i in range(1, len(df_datos_gps)):
        row_prev = df_datos_gps.iloc[i-1]
        row = df_datos_gps.iloc[i]
        analizar_dato_gps(row,row_prev,indices_parcela) 

    df_datos_gps['velocidad_media_30_anteriors'] = [0] + velocidades_medias
    df_datos_gps['id_parcela'] = [0] + indices_parcela

    columnas = ['Numero_pendiente','latitude','longitude','fecha','id_parcela','fuera_del_recinto','distancia_en_Km','velocidad','pos_promedio_lat','pos_promedio_lon','distancia_a_promedio','vacas_alejadas','velocidad_media_30_anteriors']
    df_datos_gps = df_datos_gps[columnas]
    df_datos_gps.to_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_DATOS_PROCESADOS),index=False)
    df_anomalias.to_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_ANOMALIAS))
    
    df_vacas = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_VACAS))
    # Establece 'Numero_pendiente' como el índice del DataFrame para alinearlo con las claves de tus diccionarios
    df_vacas.set_index('Numero_pendiente', inplace=True)

    # Añade los diccionarios como nuevas columnas
    df_vacas['segundos_pastando'] = df_vacas.index.map(segundos_pastando)
    df_vacas['segundos_descansando'] = df_vacas.index.map(segundos_descansando)
    df_vacas['segundos_caminando'] = df_vacas.index.map(segundos_caminando)
    
    df_vacas.to_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_VACAS))
    
    if VERBOSE: 
        print(f"\nDistancia total recorrida: {distancia_total} km\n")
        print(f"segundos_pastando: {segundos_pastando}\n")
        print(f"segundos_descansando: {segundos_descansando}\n")
        print(f"segundos_caminando: {segundos_caminando}\n")
