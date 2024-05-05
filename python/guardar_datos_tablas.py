import pandas as pd
from conf import *
from sqlalchemy.exc import SQLAlchemyError


def guardar_tabla(df,nombre_tabla):
    try:
        df.to_sql(nombre_tabla, con=obtener_engine(), if_exists='append', index=False)
        print("Datos insertados correctamente.")
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    df = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_VACAS))
    guardar_tabla(df,'Vaca')
    
    df = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_PARTOS))
    guardar_tabla(df,'Partos')
    
    df = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_ENFERMEDADES))
    guardar_tabla(df,'Enfermedades')
    
    df = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_ENFERMEDADES))
    guardar_tabla(df,'Enfermedades')
    
    df = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_DATOS_PROCESADOS))
    if 'IdUsuario' not in df.columns:
        # Si no existe, la creamos e inicializamos todas las filas de esa columna a 1
        df['IdUsuario'] = 1
    columnas = ['Numero_pendiente','IdUsuario','latitude','longitude','fecha','id_parcela','fuera_del_recinto','velocidad','tipo']
    df = df[columnas]
    guardar_tabla(df,'gps')