from shapely.geometry import Polygon,Point
from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic
import math
import json
from conf import *
import sys
from numpy import log2
import pandas as pd

def haversine(punto1, punto2):
    """
    Calcula la distancia entre el punto 1 y el 2
    """
    R = 6371.0
    lat1, lon1 = punto1
    lat2, lon2 = punto2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calcular_area_esferica(coords):
    if len(coords) < 3:
        return 0
    # Comprobamos si el primer y último punto son diferentes, comparando cada elemento
    coords = coords + [coords[0]] if not all(c1 == c2 for c1, c2 in zip(coords[0], coords[-1])) else coords
    area = 0
    for i in range(len(coords) - 1):
        p1, p2 = coords[i], coords[i + 1]
        lat1, lon1 = map(math.radians, p1)
        lat2, lon2 = map(math.radians, p2)
        area += (lon2 - lon1) * (2 + math.sin(lat1) + math.sin(lat2))
    return abs(area) * (6371000 ** 2) / 2

def mover_punto(punto_inicio: tuple, punto_destino: tuple, distancia_metros: tuple):
    geod = Geodesic.WGS84.Inverse(*punto_inicio, *punto_destino)
    rumbo_inicial = geod['azi1']
    nuevo_punto = Geodesic.WGS84.Direct(punto_inicio[0], punto_inicio[1], rumbo_inicial, distancia_metros)
    return (nuevo_punto['lat2'], nuevo_punto['lon2'])

def esta_en_el_limite(punto, poligono):
    return Point(punto).touches(Polygon(poligono))

def punto_en_linea(punto: tuple, linea_punto1: tuple, linea_punto2: tuple, tolerancia=0.1):
    total_distancia = geodesic(linea_punto1, linea_punto2).meters
    dist_p1 = geodesic(punto, linea_punto1).meters
    dist_p2 = geodesic(punto, linea_punto2).meters
    return abs((dist_p1 + dist_p2) - total_distancia) <= tolerancia



def coordenadas_toca_parcela(coords_parcela: list,coords_subespacio: list):
    poligono_parcela = Polygon(coords_parcela)
    coords_subespacio_touch_parcela = {}

    for k in range(len(coords_subespacio)):
        if esta_en_el_limite(coords_subespacio[k],poligono_parcela):
            coords_subespacio_touch_parcela[k] = coords_subespacio[k]
    return coords_subespacio_touch_parcela



def seleccionar_coordenadas_desplazables(coords_subespacio_touch_parcela, coords_parcela):
    
    poligono_subespacio = Polygon(list(coords_subespacio_touch_parcela.values()))
    
    coordenadas_elegidas = {}
    # Precomputar límites para todas las coordenadas de la parcela
    en_limite = [esta_en_el_limite(coord, poligono_subespacio) for coord in coords_parcela]
    
    for i in range(len(coords_parcela)):
        actual = i
        previo = i - 1
        siguiente = previo if (en_limite[actual] and not en_limite[previo]) else actual
        anterior = actual if siguiente == previo else previo
        
        if en_limite[previo] != en_limite[actual]:
            coordenadas_posibles = {}
            for key, value in coords_subespacio_touch_parcela.items():
                if punto_en_linea(value, coords_parcela[anterior], coords_parcela[siguiente], 0):
                    coordenadas_posibles[key] = value
            
            menor_distancia = float('inf')
            index_elegido, coordenada_elegida = None, None
            for index, coordenada in coordenadas_posibles.items():
                dist = haversine(coordenada, coords_parcela[siguiente])
                if dist < menor_distancia:
                    menor_distancia = dist
                    coordenada_elegida = coordenada
                    index_elegido = index
            
            if index_elegido is not None:
                coordenadas_elegidas[index_elegido] = (coordenada_elegida, siguiente, anterior)
    
    return coordenadas_elegidas




def añadir_coordenadas_nuevas(coords_subespacio_touch_parcela: dict,coordeenadas_elegidas: dict):
    # Ajustar las coordenadas según las elecciones, modificando el índice si es necesario.
    for index, coordenada_tuple in coordeenadas_elegidas.items():
        siguiente, anterior = coordenada_tuple[1], coordenada_tuple[2]
        nuevo_index = index + 0.5 if siguiente < anterior else index - 0.5
        coords_subespacio_touch_parcela[nuevo_index] = coordenada_tuple[0]
    
    # Ordenar el diccionario por clave para asegurar consistencia.
    # Esto es importante si el orden de los índices afecta a la lógica de procesamiento posterior.
    coords_subespacio_touch_parcela = dict(sorted(coords_subespacio_touch_parcela.items()))

    return coords_subespacio_touch_parcela

    
def expandir_area(metros_cuadrados_expandir: int, area_original: int, coords_parcela: list, coords_a_expandir: dict,coordeenadas_elegidas: dict, add_metros=5, num_maximo_bucle= 200):
    ADD_AREA = metros_cuadrados_expandir
    
    
    diferencia_area = 0
    coords_subespacio_sugerido = coords_a_expandir.copy()
    
    bucle = 0 
    while diferencia_area < ADD_AREA:
        for index, coordenada_tuple in coordeenadas_elegidas.items():
            siguiente = coordenada_tuple[1]
            anterior = coordenada_tuple[2]
            punto_bueno = True
            if not punto_en_linea(coords_subespacio_sugerido[index], coords_parcela[anterior], coords_parcela[siguiente], 1):
                if siguiente < anterior:
                    siguiente, anterior = max(0, siguiente - 1), siguiente
                else:
                    siguiente, anterior = min(len(coords_parcela) - 1, siguiente + 1), siguiente
                
                coords_subespacio_sugerido[index] = coords_parcela[siguiente]
                punto_bueno = False
                coordeenadas_elegidas[index] = coords_subespacio_sugerido[index], siguiente, anterior
                add_metros = 1

            if punto_bueno:
                coords_subespacio_sugerido[index] = mover_punto(coordenada_tuple[0], coords_parcela[siguiente], add_metros)
                
            nueva_area = calcular_area_esferica(list(coords_subespacio_sugerido.values()))
            diferencia_area = nueva_area - area_original
            
            if bucle > num_maximo_bucle:
                exit(ERROR_BUCLE_INFINITO)
            bucle += 1
            
            if diferencia_area - ADD_AREA >= 0:
                break
            else:
                add_metros += (ajustar_add_metros(diferencia_area, ADD_AREA))/2
       

    return coords_subespacio_sugerido

def ajustar_add_metros(diferencia_area, metros_cuadrados_expandir):
    if  diferencia_area > metros_cuadrados_expandir -50:
        return 3
    elif  diferencia_area > metros_cuadrados_expandir -300:
        return log2( metros_cuadrados_expandir - diferencia_area  + 1)/2
    else:
        return log2( metros_cuadrados_expandir - diferencia_area  + 1)

def verificar_argumentos():
    if len(sys.argv) < 3:
        print(json.dumps({"mensaje": "Algo ha salido mal"}))
        sys.exit(-1)
    return sys.argv[1], sys.argv[2]

def find_vertices(points):
    """Encuentra los vértices en una lista de puntos."""
    vertices = []
    n = len(points)
    for i in range(n):
        p1 = points[i - 1]  # punto anterior
        p2 = points[i]      # punto actual
        p3 = points[(i + 1) % n]  # punto siguiente, usando módulo para conectar el final con el principio
        
        if not punto_en_linea(p2, p1, p3):  # atol es la tolerancia, ajustar según la precisión deseada
            vertices.append(p2)
    
    return vertices

def ajustar_vertices_subespacio(coords_subespacio, coords_parcela):
    # Crear polígonos usando las listas de coordenadas
    poligono_subespacio = Polygon(coords_subespacio)
    poligono_parcela = Polygon(coords_parcela)
    
    # Lista para guardar los puntos más cercanos
    puntos_cercanos = []
    
    # Iterar sobre cada punto en el polígono de la parcela
    for punto in poligono_parcela.exterior.coords:
        # Convertir el punto actual a un objeto Point
        punto_actual = Point(punto)
        
        # Encontrar la distancia mínima entre el punto actual y el polígono del subespacio
        distancia_minima = poligono_subespacio.exterior.distance(punto_actual)
        
        # Guardar el punto y la distancia mínima
        puntos_cercanos.append((punto, distancia_minima))
    
    # Filtrar para obtener solo los puntos con la distancia mínima
    if puntos_cercanos:
        min_distancia = min(puntos_cercanos, key=lambda x: x[1])[1]
        puntos_cercanos = [p for p, d in puntos_cercanos if d == min_distancia]
    
    return puntos_cercanos
    
    
    
ERROR_NO_HAY_COORDENADAS_SUB_ESPACIO = -128
ERROR_BUCLE_INFINITO = -129


def obtener_recomendacion_sector(expansion_metros_cuadrados, coords_parcela ,coords_subespacio ,porcentaje_de_error=0.1):
    
    # Reducimos quitando los puntos que estan en la linea que se une
    coords_parcela = find_vertices(coords_parcela)
    coords_subespacio = find_vertices(coords_subespacio)
    
    if len(coords_subespacio) == 0:
        exit(ERROR_NO_HAY_COORDENADAS_SUB_ESPACIO)
    
    ## Obtencion de las coordenadas
    coords_subespacio_touch_parcela = coordenadas_toca_parcela(coords_parcela,coords_subespacio) # Obtenemos las coordenadas del subespacio que toca la parcela
    
    
    coordeenadas_elegidas = seleccionar_coordenadas_desplazables(coords_subespacio_touch_parcela,coords_parcela) # Obtenemos las coordenadas que podemos desplazar
    coords_subespacio_touch_parcela_new = añadir_coordenadas_nuevas(coords_subespacio_touch_parcela,coordeenadas_elegidas) # Las añadimos a las coordenadas del subespacio a recomendar
    
    area_sector = calcular_area_esferica(coords_subespacio) 
    area_parcela = calcular_area_esferica(coords_parcela)
    expandir = expansion_metros_cuadrados - area_parcela * porcentaje_de_error
    coords_sugeridas = None
    
    expandir = area_parcela + 10000
    # Comprobamos que el area a expadir es menor que el area total de la parcela
    if (expandir <= area_parcela):
        mensaje("Es recomendable cambiar de parcela")
    else:
        if (expandir < area_parcela - calcular_area_esferica(coords_subespacio)):
            coords_sugeridas = coords_parcela
            mensaje("La parcela se está quedando pequeña")
        else:
            if len(coords_subespacio_touch_parcela) < 3:
                coords_subespacio_ajustadas = ajustar_vertices_subespacio(coords_subespacio, coords_parcela)
                area_sector_calculada = calcular_area_esferica(coords_subespacio_ajustadas)
                if (area_sector_calculada-area_sector >= expandir):
                    coords_subespacio_sugerido = coords_subespacio_ajustadas
                else:
                    coords_subespacio_sugerido = expandir_area(expansion_metros_cuadrados,area_sector,coords_parcela,coords_subespacio_ajustadas,coordeenadas_elegidas)
            else:
                coords_subespacio_sugerido = expandir_area(expansion_metros_cuadrados,area_sector,coords_parcela,coords_subespacio_touch_parcela_new,coordeenadas_elegidas)
        
        coords_sugeridas = find_vertices(list(coords_subespacio_sugerido.values()))
        lista_de_diccionarios = [{'latitude': lat, 'longitude': lon} for lat, lon in coords_sugeridas]
        json_resultado = json.dumps(lista_de_diccionarios, indent=4)
        print(json_resultado)



def calculoAreaSector(tiempoPastado, minPasto_m2):
    areaSector = (tiempoPastado/60) /minPasto_m2
    return areaSector



# Función para coger las vacas de la BD:
def getVacas(cursor, idUsuario):
    # Ejecutar una consulta SQL
    consulta = f"SELECT COUNT(Numero_pendiente) FROM Vaca WHERE IdUsuario = {str(idUsuario)}"
    cursor.execute(consulta)
    pd.read_sql_query()
    # Obtener los resultados de la consulta
    numeroVacas = cursor.fetchall()

    return numeroVacas[0][0]


if __name__ == "__main__":
    IdUsuario,id_parcela = verificar_argumentos() # obtenemos los parametros 
    # Constantes calculo área pastada:
    minMetroCuadradoPastoMedio = 7.5	#min/m2
    minMetroCuadradoPastoPeorCaso = 5	#min/m2

    id_usuario = 1
    numVacas = obtenerVacas(id_usuario,to_array= True)

    coords_parcela = obtener_coordenadas_parcela(id_parcela, True) 
    areaParcela = calcular_area_esferica(coords_parcela)

    # Crear un objeto de polígono Shapely para la extensión de tierra
    extencion_poligono = Polygon(coords_parcela)

    # Calcular el centroide del polígono
    centroide = extencion_poligono.centroid

    # Calculo del área deseada para pastar:
    segundos_pastando = getSegundosPastando(IdUsuario)
    areaPastada = calculoAreaSector(segundos_pastando, minMetroCuadradoPastoPeorCaso)
    
    # ************************************************** #
    coordenadas_sector = obtener_coordenadas_sector(id_parcela,True)
    area_sector = calcular_area_esferica(coordenadas_sector)
    expansion = 2*areaPastada - ((area_sector)*1.1) # Lo multiplicamos por 1.1 para asegurarnos de al menos expandirla un 10%
    expansion = 5000
    if (expansion > 0):
        obtener_recomendacion_sector(expansion,coords_parcela=coords_parcela,coords_subespacio=coordenadas_sector)
    else:
        mensaje("No es necesaria la expansion, el area actual es suficiente para el ganado")
    # ************************************************** #
