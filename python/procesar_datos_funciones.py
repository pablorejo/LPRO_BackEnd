# Vamos a procesar los datos obtenidos.
import pandas as pd
import numpy as np
from conf import *
from shapely.geometry import Point, Polygon
from os import path
import sys
from datetime import datetime
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

def dato_fuera(poin):
    parcelas,parcelas_dict = obtener_parcelas()
    fuera_parcela = True
    id = None
    global id_sector
    for id_parcela, puntos in parcelas_dict.items():
        poligono = Polygon(puntos)
        if poligono.contains(poin):
            fuera_parcela = False
            id = id_parcela
            id_sector = id_parcela
            break
        else:
            id = None
    
    return fuera_parcela,id


def estan_todos_fuera(id_parcela):
    """
        Devuelve true en caso de que todos estean fuera y false en caso contrario
    """
    
    query = """SELECT gps.latitude, gps.longitude
FROM gps
LEFT JOIN gps as gps2 
ON gps.Numero_pendiente = gps2.Numero_pendiente AND gps.IdUsuario = gps2.IdUsuario
AND (gps.fecha < gps2.fecha OR (gps.fecha = gps2.fecha AND gps.id_vaca_gps < gps2.id_vaca_gps))
WHERE gps2.id_vaca_gps IS NULL AND gps.IdUsuario = 1;"""

    df_datos_gps = pd.read_sql_query(query,obtener_engine())
    list_of_tuples = list(zip(df_datos_gps['latitude'], df_datos_gps['longitude']))
    
    estan_fuera = True
    for latitude,longitude in list_of_tuples:
        coords_parcela = obtener_coords_parcela(id_parcela,True)
        poligono_parcela = Polygon(coords_parcela)
        if (poligono_parcela.contains(Point(latitude,longitude))):
            estan_fuera = False
            break
            
    return estan_fuera

if __name__ == "__main__":
    opcion = sys.argv[1]
    if opcion == 'velocidad':
        distancia = haversine(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
        
        fecha1 = datetime.strptime(sys.argv[6], '%Y-%m-%d %H:%M:%S')
        fecha2 = datetime.strptime(sys.argv[7], '%Y-%m-%d %H:%M:%S')

        tiempo = (fecha2 - fecha1).total_seconds()  # Tiempo en horas
        velocidad = distancia * 1000 / tiempo if tiempo > 0 else 0
        tipo = ""
        if (velocidad <= 1/20 and velocidad >= 1/30):
            tipo = "pastando"
        elif(velocidad > 1/20):
            tipo = "caminando"
        elif velocidad < 1/30:
            tipo = "descansando"
        print (f'{velocidad},{tipo}')
        
        
    elif opcion == 'fuera_del_recinto':
        fuera_parcela,id  = dato_fuera(Point(float(sys.argv[2]), float(sys.argv[3])))
        print(f'{fuera_parcela},{id}')
        
    elif opcion == 'estan_todos_fuera':
        print(estan_todos_fuera(int(sys.argv[2])))
        
