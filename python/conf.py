from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
from json import dumps
from os import path,mkdir
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

fecha_inicial = datetime.now() - timedelta(days=30)

VERBOSE = True

PORCENTAJE_DE_TIEMPO_CAMINANDO = 0.2
SIGMA_CAMINANDO = 0.00005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_CAMINANDO = 1/2


PORCENTAJE_DE_TIEMPO_PASTANDO = 0.4
SIGMA_PASTANDO = 0.005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_PASTANDO = 1/25

PORCENTAJE_DE_TIEMPO_DESCANSANDO = 1 - PORCENTAJE_DE_TIEMPO_CAMINANDO -PORCENTAJE_DE_TIEMPO_PASTANDO
SIGMA_DESCANSANDO = 0.005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_DESCANSANDO = 1/50


MINUTOS = 2 # El tiempo que se tarda en obtener un dato y otro
RANGO = 1000 # El numero de puntos por vaca y por parcela
PROBABILIDAD_ANOMALIA = 0.001 # Probabilidad con la que una vaca va a tener una anomalia
SIGMA_ANOMALIA = 0.0001 # El nivel de movimiento de la anomalia
NUMERO_DE_VACAS = 10 # Número de vacas que se van a crear
NUMERO_PARCELAS = 1 # Número de parcelas a crear
PARA_SQL =  True # Si se quiere guardar en un fichero para pasarlo a sql.
# Aquí vamos a definir las esquinas de las parcelas.

CARPETA_DATOS_CSV = 'datos_csv'

if (not path.exists(CARPETA_DATOS_CSV)):
    mkdir = CARPETA_DATOS_CSV

FICHERO_DATOS_PARCELA = 'parcelas.csv'
FICHERO_DATOS_ENFERMEDADES = 'enfermedades.csv'
FICHERO_DATOS_PARTOS = 'partos.csv'
FICHERO_DATOS_VACAS = 'vacas.csv'
FICHERO_DATOS_DATOS = 'datos.csv'
FICHERO_DATOS_DATOS_PROCESADOS = 'datos_procesados.csv'
FICHERO_DATOS_ANOMALIAS = 'anomalias.csv'

parcelas = None

# parcelas = [
#     [
#         (42.1708749220415 ,  -8.684778213500977),
#         (42.17088784344455 ,  -8.683796525001526),
#         (42.171329902931646 ,  -8.683318421244621),
#         (42.171783638124204 ,   -8.68295531719923),
#         (42.17215164330223 ,  -8.682750463485718),
#         (42.17232210277389 ,  -8.683327473700047),
#         (42.17273135272034 ,  -8.684871755540371),
#         (42.17178438357912 ,   -8.68525430560112)
#     ]
# ]
PONER_ANOMALIAS = False



engine = None

# connection = mysql.connector.connect(
#         user = 'root',
#         password = 'LPRO_2024',
#         host = 'localhost',
#         database = 'muundoGando'
#         )



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
    return parcelas, parcelas_dict

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

def obtenerNumerosPendiente(idUsuario):
    obtener_engine()
    query = f"SELECT Numero_pendiente FROM Vaca WHERE IdUsuario = {str(idUsuario)}"
    data = pd.DataFrame(pd_to_array(query, False))
    return data['Numero_pendiente'].astype(str)

def obtenerCoordsVaca(id_parcela, tipo, to_array = False):
    obtener_engine()
    query = f"SELECT latitude, longitude FROM gps WHERE id_parcela = {id_parcela} AND tipo={tipo}"
    if to_array:
        return pd_to_array(query,to_array)
    else:
        data = pd.DataFrame(pd_to_array(query, False))
        return data['latitude'].astype(str), data['longitude'].astype(str)


def obtener_coords_parcela(id_parcela,to_array = False):
    obtener_engine()
    query = f"SELECT latitude, longitude from coordenadas WHERE id_parcela = {id_parcela}"
    if to_array:
        
        return pd_to_array(query,to_array )
    else:
        data = pd.DataFrame(pd_to_array(query, False))
        return data['latitude'].astype(str), data['longitude'].astype(str)

def getSegundosPastando(idUsuario):
    query = "SELECT segundos_pastando \
                FROM Vaca \
                WHERE IdUsuario =" + str(idUsuario)

    data = pd.DataFrame(pd_to_array(query, False))
    return data['segundos_pastando'].sum()

def mensaje(mensaje: str):
    # Crear el diccionario
    data = {
        "mensaje": mensaje
    }
    # Convertir el diccionario a JSON
    json_data = dumps(data)
    print(json_data)
    
Session = sessionmaker(bind=engine)
def actualizar_actividades(numero_pendiente, id_usuario, adicion_pastando, adicion_caminando, adicion_descansando):
    session = Session()
    try:
        # Buscar la vaca específica
        vaca = session.query(Vaca).filter_by(Numero_pendiente=numero_pendiente, IdUsuario=id_usuario).one_or_none()
        if vaca:
            # Actualizar los valores
            vaca.segundos_pastando += adicion_pastando
            vaca.segundos_caminando += adicion_caminando
            vaca.segundos_descansando += adicion_descansando
            session.commit()

    except Exception as e:
        session.rollback()  # Revertir cambios en caso de error
    finally:
        session.close()
        
if __name__ == "__main__":
    print(obtenerVacas(1))


Base = declarative_base()

class Vaca(Base):
    __tablename__ = 'Vaca'
    
    Numero_pendiente = Column(Integer, primary_key=True)
    IdUsuario = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    Fecha_nacimiento = Column(Date, nullable=False)
    idNumeroPendienteMadre = Column(Integer, nullable=True)
    idUsuarioMadre = Column(Integer, nullable=True)
    nota = Column(Text, nullable=True)
    segundos_pastando = Column(Integer, default=0)
    segundos_descansando = Column(Integer, default=0)
    segundos_caminando = Column(Integer, default=0)

    usuario = relationship("Usuario")  # Suponiendo que existe una clase Usuario

# Crear todas las tablas en la base de datos (si no existen)
Base.metadata.create_all(obtener_engine())