from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
from json import dumps

fecha_inicial = datetime.now() - timedelta(days=30)

PORCENTAJE_DE_TIEMPO_CAMINANDO = 0.2
SIGMA_CAMINANDO = 0.00005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_CAMINANDO = 1/2


PORCENTAJE_DE_TIEMPO_PASTANDO = 0.2
SIGMA_PASTANDO = 0.005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_PASTANDO = 1/25

PORCENTAJE_DE_TIEMPO_DESCANSANDO = 1 - PORCENTAJE_DE_TIEMPO_CAMINANDO -PORCENTAJE_DE_TIEMPO_PASTANDO
SIGMA_DESCANSANDO = 0.005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_DESCANSANDO = 1/50


minutos = 0.1 # El tiempo que se tarda en obtener un dato y otro
rango = 1000 # El numero de puntos por vaca y por parcela
probabilidad_anomalia = 0.001 # Probabilidad con la que una vaca va a tener una anomalia
sigma_anomalia = 0.0001 # El nivel de movimiento de la anomalia
numero_de_vacas = 10 # Número de vacas que se van a crear
PARA_SQL =  False # Si se quiere guardar en un fichero para pasarlo a sql.

engine = None


def obtener_engine():
    global engine
    if engine is None:
        usuario = 'root'
        contraseña = 'LPRO_2024'
        host = 'localhost'
        base_de_datos = 'muundoGando'
        url_conexion = f"mysql+pymysql://{usuario}:{contraseña}@{host}/{base_de_datos}"
        engine = create_engine(url_conexion, pool_recycle=3600, pool_pre_ping=True)
    return engine

def pd_to_array(query: str, to_array: bool):
    if to_array:
        return list(pd.read_sql_query(query, engine).itertuples(index=False, name=None)) 
    else:
        return pd.read_sql_query(query, engine)
    
    
def obtener_coordenadas_parcela(id_parcela,to_array = False):
    obtener_engine()
    query = f"SELECT latitude, longitude from coordenadas WHERE id_parcela = {id_parcela}"
    return pd_to_array(query, to_array)

def obtener_parcelas():
    obtener_engine()
    query = f"SELECT id_parcela, latitude, longitude from coordenadas"
    df_parcelas = pd.read_sql_query(query, engine)
    # Organizar el DataFrame en una lista de listas de coordenadas por cada parcela
    parcelas_dict = df_parcelas.groupby('id_parcela').apply(
        lambda x: list(zip(x.latitude, x.longitude))
    ).to_dict()

    # Convertir el diccionario en una lista de parcelas, donde cada parcela es representada por su lista de coordenadas
    parcelas = list(parcelas_dict.values())
    return parcelas

def obtener_coordenadas_sector(id_parcela,to_array = False):
    obtener_engine()
    query = f"SELECT latitude, longitude from coordenadas_sector WHERE id_parcela = {id_parcela}"
    return pd_to_array(query, to_array)
    
# Función para coger las vacas de la BD:
def obtenerVacas(idUsuario,to_array = False):
    # Ejecutar una consulta SQL
    obtener_engine()
    query = f"SELECT * FROM Vaca WHERE IdUsuario = {str(idUsuario)}"
    return pd_to_array(query, to_array)

def getMinPastoVacas(idUsuario):
    query = "SELECT minPastoVaca \
                FROM Vaca \
                WHERE IdUsuario =" + str(idUsuario)

    data = pd.DataFrame(pd_to_array(query, False))
    return data['minPastoVaca'].sum()

def mensaje(mensaje: str):
    # Crear el diccionario
    data = {
        "mensaje": mensaje
    }
    # Convertir el diccionario a JSON
    json_data = dumps(data)
    print(json_data)

