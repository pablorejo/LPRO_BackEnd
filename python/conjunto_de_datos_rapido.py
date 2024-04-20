import sys
import json
import pandas as pd
import random
from conf import obtener_engine, obtener_coordenadas_parcela

from shapely.geometry import Polygon, Point
def verificar_argumentos():
    if len(sys.argv) < 6:
        print(json.dumps({"mensaje": "Algo ha salido mal"}))
        sys.exit(-1)
    return sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5].split(",")

def consultar_datos_gps(engine, id_usuario, fecha_inicio, fecha_fin, numeros_pendiente):
    numeros_in = ','.join(f"'{num.strip()}'" for num in numeros_pendiente if num.strip())
    where_clauses = [f"idusuario = '{id_usuario}'"]
    if numeros_in:
        where_clauses.append(f"Numero_pendiente IN ({numeros_in})")
    if fecha_inicio != "None":
        where_clauses.append(f"fecha >= '{fecha_inicio}'")
    if fecha_fin != "None":
        where_clauses.append(f"fecha <= '{fecha_fin}'")
    query_filtro = f"SELECT latitud, longitud, Numero_pendiente FROM gps WHERE {' AND '.join(where_clauses)};"
    return pd.read_sql_query(query_filtro, engine, index_col='Numero_pendiente')

def random_subsampling(points, sample_size):
    points_list = list(map(tuple, points))  # Convertir array de NumPy a lista de tuplas
    return random.sample(points_list, min(sample_size, len(points_list)))

def filtrar_datos_dentro_parcela(id_usuario, id_parcela,engine,data_df: pd.DataFrame):
    coordenadas_parcela = pd.DataFrame(obtener_coordenadas_parcela(id_parcela,engine)).to_numpy()
    poligono_parcela = Polygon(coordenadas_parcela)
    data_in_parcela = []
    for k in range(len(data_df)):
        fila = data_df.iloc[k]
        tupla = (fila['latitud'],fila['longitud'])
        punto = Point(tupla)
        if poligono_parcela.contains(punto):
            data_in_parcela.append(tupla)
    return data_in_parcela
    
def main():
    id_usuario, id_parcela, fecha_inicio, fecha_fin, numeros_pendiente = verificar_argumentos()
    engine = obtener_engine() # Obtenemos el motor
    data_df = consultar_datos_gps(engine, id_usuario, fecha_inicio, fecha_fin, numeros_pendiente) # Obtenemos el conjunto de datos gps
    points = filtrar_datos_dentro_parcela(id_usuario,id_parcela,engine,data_df) # Obtenemos los puntos que estan dentro de la parcela
    points_reduce = random_subsampling(points, 300) # reducimos los datos de manera aleatoria a 300
    
    # Los combertimso en json
    reduced_df = pd.DataFrame(points_reduce, columns=['latitude', 'longitude'])
    clusters_json = reduced_df.to_dict(orient='records')
    json_output = json.dumps(clusters_json, indent=4)
    print(json_output)

if __name__ == "__main__":
    main()
