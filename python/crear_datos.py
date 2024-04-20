from random import uniform, gauss, random, choices
from datetime import datetime, timedelta
from shapely.geometry import Point, Polygon
from conf import *
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
import numpy as np

def next_date():
    global fecha_inicial
    global minutos
    fecha_inicial = fecha_inicial + timedelta(minutes=minutos)
    return fecha_inicial


def parsear_cordenadas(cordenadas: str):
    longitud, latitud = cordenadas.split(' ')
    return pasar_a_grados(longitud), pasar_a_grados(latitud)

def pasar_a_grados(dms):
    # Recordamos Latitud Norte, Sur: Norte +, Sur -
    # Recordamos Longitu Este, Oeste: Este +, Oeste -
    partes = dms.replace('°', ' ').replace('\'', ' ').replace('"', ' ').split()
    grados = float(partes[0]) + float(partes[1])/60 + float(partes[2])/3600
    if partes[3] in ['S', 'W']:
        grados *= -1
    return grados

def generar_punto_con_velocidad(punto_anterior, velocidad):
    # Calcular la distancia basada en la velocidad y el intervalo de tiempo
    distancia = velocidad * minutos * 60  # en metros
    
    # Generar un ángulo aleatorio en radianes
    angulo = np.random.uniform(0, 2 * np.pi)
    
    # Convertir distancia en metros a cambios en grados
    delta_lat = distancia / 111000  # 111,000 metros es aproximadamente un grado de latitud
    delta_lon = distancia / (111000 * np.cos(np.radians(punto_anterior[1])))  # Ajuste por coseno de la latitud para longitud

    # Calcular el desplazamiento en grados
    delta_x = delta_lon * np.cos(angulo)
    delta_y = delta_lat * np.sin(angulo)
    
    
    # Nuevo punto
    nuevo_punto_x = punto_anterior[0] + delta_x
    nuevo_punto_y = punto_anterior[1] + delta_y
    
    return Point(nuevo_punto_x, nuevo_punto_y)

def generar_punto_aleatorio_en_parcela(anomalia: bool,poligono_parcela, punto_anterior:tuple=(0,0)):
    
        if (punto_anterior == (0,0)):
            while True:
                punto_aleatorio = Point(uniform(min_x, max_x),uniform(min_y, max_y))
                if poligono_parcela.contains(punto_aleatorio):
                    return (punto_aleatorio.x, punto_aleatorio.y)
            
        elif (anomalia):
            punto_aleatorio = Point(gauss(punto_anterior[0],sigma_anomalia), gauss(punto_anterior[1],sigma_anomalia))
            return (punto_aleatorio.x, punto_aleatorio.y)
        else:
            probabilidades = [PORCENTAJE_DE_TIEMPO_CAMINANDO,PORCENTAJE_DE_TIEMPO_PASTANDO,PORCENTAJE_DE_TIEMPO_DESCANSANDO]
            actividad = choices(["caminando", "pastando", "descansando"], probabilidades)[0]
            sigma = SIGMA_DESCANSANDO  # Valor por defecto para 'descansando'
            velocidad = VELOCIDAD_DESCANSANDO
            if actividad == "caminando":
                sigma = SIGMA_CAMINANDO
                velocidad = VELOCIDAD_CAMINANDO
            elif actividad == "pastando":
                sigma = SIGMA_PASTANDO
                velocidad = VELOCIDAD_PASTANDO
            while True:
                
                punto_aleatorio = generar_punto_con_velocidad(punto_anterior, gauss(velocidad,sigma))
                    
                if poligono_parcela.contains(punto_aleatorio):
                    return (punto_aleatorio.x, punto_aleatorio.y)
                
            
columnas = ['Numero_pendiente', 'latitude', 'longitude', 'fecha', 'anomalia']
df = pd.DataFrame(columns=columnas)  # Define las columnas de tu DataFrame

for parcela in  tqdm(parcelas, desc="Procesando parcelas"):
    poligono_parcela = Polygon(parcela)
    # Calcular el bounding box de la parcela
    min_x, min_y, max_x, max_y = poligono_parcela.bounds

    for numero_pendiente in tqdm(range(1, numero_de_vacas), desc="Numero_pendiente", leave=False):
        fecha_inicial = datetime.now() - timedelta(days=30)
        punto_anterior = (0,0)
        for num in tqdm(range(1, rango), desc="Generando puntos", leave=False):
        
            # Generar 5 puntos aleatorios dentro de la parcela
            anomalia = False
            if probabilidad_anomalia > random():
                anomalia = True
            
            puntos_aleatorios = generar_punto_aleatorio_en_parcela(anomalia,poligono_parcela,punto_anterior=punto_anterior) 
            
            if (not anomalia):
                punto_anterior = puntos_aleatorios
            
           
            new_row = {
                        columnas[0]: int(numero_pendiente) + 1000,
                        columnas[1]: puntos_aleatorios[0],
                        columnas[2]: puntos_aleatorios[1],
                        columnas[3]: next_date()
                    }
            
            df = pd.concat([df, pd.DataFrame([new_row], dtype="object")], ignore_index=True)
            
df = df[columnas]
df.to_csv('datos.csv',index=False)

if(PARA_SQL):
    with open('datos.sql','w') as file:
        file.write("""USE muundoGando
INSERT INTO gps (Numero_pendiente,IdUsuario,latitud, longitud,fecha)
VALUES 
""")
        
        for indice_fila in range(0,len(df)):
            fila = df.iloc[indice_fila]
            fecha = f"'{str(fila['fecha']).split('.')[0]}'"
            nuermo_pendiente = int(fila['Numero_pendiente'])
            if (indice_fila == len(df)-1):
                file.write(f"({nuermo_pendiente},1,{fila['latitude']},{fila['longitude']},{fecha});\n")
            else:
                file.write(f"({nuermo_pendiente},1,{fila['latitude']},{fila['longitude']},{fecha}),\n")