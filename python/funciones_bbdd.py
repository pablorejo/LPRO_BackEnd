from conf import *
import pandas as pd
import numpy as np
import sys
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


def obtenerHeatmap(id_usuario: int, id_parcela: int= None, fecha_inicio: datetime = None, fecha_fin: datetime = None, numero_pendiente: int=0):
    
    # Crea el motor de SQLAlchemy

    query = f"""SELECT *
FROM coordenadas 
INNER JOIN parcela
ON coordenadas.id_parcela=parcela.id_parcela WHERE parcela.idusuario = {id_usuario}"""
    if (id_parcela):
        query += f" and parcela.id_parcela={id_parcela}"
        
    query += ";"
    df = pd.read_sql_query(query, engine,index_col='id_esquina')
    print(df.to_string())
    

def obtener_datos_vaca(numero_pendiente: int, id_usuario: int = 0):
    #Obtenemos los datos de la vaca
    query_vaca =  f"""SELECT Vaca.*, gps.* FROM Vaca INNER JOIN gps ON Vaca.Numero_pendiente = gps.Numero_pendiente WHERE Vaca.idusuario = {id_usuario} AND Vaca.Numero_pendiente = {numero_pendiente};"""
    df_vaca =  pd.read_sql_query(query_vaca, engine,index_col='Numero_pendiente')
    df_vaca['fecha'] = pd.to_datetime(df_vaca['fecha'])
    df_vaca = df_vaca.sort_values(by=['Numero pendiente', 'fecha'])
    
    #Obtenemos los datos de la madre
    query_vaca_madre =  f"""SELECT * FROM Vaca INNER JOIN gps ON Vaca.Numero_pendiente = gps.Numero_pendiente WHERE Vaca.idusuario = {id_usuario} AND Vaca.Numero_pendiente = {df_vaca['idNumeroPendienteMadre'][0]};"""
    df_vaca_madre =  pd.read_sql_query(query_vaca_madre, engine,index_col='Numero_pendiente')
    df_vaca_madre['fecha'] = pd.to_datetime(df_vaca_madre['fecha'])
    df_vaca_madre = df_vaca_madre.sort_values(by=['Numero pendiente', 'fecha'])
    
    #Obtenemos los datos de las hijas
    query_hijas = f"""SELECT * FROM Vaca INNER JOIN gps ON Vaca.Numero_pendiente = gps.Numero_pendiente  WHERE gps.idusuario = {id_usuario} AND idNumeroPendienteMadre = {df_vaca['Numero_pendiente'][0]};"""
    
    df_vaca_hijas = pd.read_sql_query(query_hijas, engine,index_col='Numero_pendiente')
    df_vaca_hijas['fecha'] = pd.to_datetime(df_vaca_hijas['fecha'])
    df_vaca_hijas = df_vaca_hijas.sort_values(by=['Numero pendiente', 'fecha'])
    
def obtener_tiempo_pasto_vaca(numero_pendiente: int, id_usuario: int = 0):
    query_vaca =  f"""SELECT * FROM gps WHERE idusuario = {id_usuario} AND Numero_pendiente = {numero_pendiente};"""
    df_vaca =  pd.read_sql_query(query_vaca, engine,index_col='Numero_pendiente')
    df_vaca['fecha'] = pd.to_datetime(df_vaca['fecha'])
    df_vaca = df_vaca.sort_values(by=['fecha'])
    

if __name__ == "__main__":
    print("ejecutando funciones " + len(sys.argv))
    for numero in sys.argv:
        print (numero)
        
    obtener_tiempo_pasto_vaca(numero_pendiente=1001,id_usuario=1)