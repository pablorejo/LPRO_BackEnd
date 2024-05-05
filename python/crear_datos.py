from random import uniform, gauss, random, choices,randint
from datetime import datetime, timedelta
from shapely.geometry import Point, Polygon
from conf import *
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
import numpy as np
from os import path
def next_date():
    global fecha_inicial
    global MINUTOS
    fecha_inicial = fecha_inicial + timedelta(minutes=MINUTOS)
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
    distancia = velocidad * MINUTOS * 60  # en metros
    
    # Generar un ángulo aleatorio en radianes
    angulo = np.random.uniform(0, 2 * np.pi)
    
    # Convertir distancia en metros a cambios en grados
    delta_lat = distancia / 111000  # 111,000 metros es aproximadamente un grado de latitud
    delta_lon = distancia / (111000 * np.cos(np.radians(punto_anterior[1])))  # Ajuste por coseno de la latitud para longitud

    # Calcular el desplazamiento en grados
    delta_x = delta_lon * np.cos(angulo)
    delta_y = delta_lat * np.sin(angulo)
    
    
    # Nuevo punto
    nuevo_punto_x = punto_anterior[0] + choices([delta_x, -delta_x])
    nuevo_punto_y = punto_anterior[1] + choices([delta_y, -delta_y])
    
    return Point(nuevo_punto_x[0], nuevo_punto_y[0])

def generar_punto_aleatorio_en_parcela(anomalia: bool,poligono_parcela,punto_inicial, punto_anterior:tuple=(0,0)):
    min_x, min_y, max_x, max_y = poligono_parcela.bounds

    if (punto_anterior == (0,0)):
        while True:
            random_point = Point(uniform(min_x, max_x), uniform(min_y, max_y))  # Generar un punto aleatorio
            if poligono_parcela.contains(random_point):  # Verificar si el polígono contiene el punto
                return (random_point.x, random_point.y)
            
    elif (anomalia):
        punto_aleatorio = Point(gauss(punto_anterior[0],SIGMA_ANOMALIA), gauss(punto_anterior[1],SIGMA_ANOMALIA))
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
                
                
def crear_parcelas(numero_parcelas: int):
    vertices = []
    for i in range(numero_parcelas):
        numero_vertices = randint(5,10)
        for k in range(numero_vertices):
            latitud = 0
            longitud = 0
            vertice = (latitud,longitud)
            vertices.append(vertice)
            #Crear los vertices
            pass
    return vertices


def generar_datos_vacas(n):
    np.random.seed(0)  # Para reproducibilidad
    
    # Crear número pendiente y ID de usuario
    numeros_pendientes = np.random.randint(1000, 10000, size=n)
    # Asignar todos los IdUsuario a 1
    id_usuarios = np.ones(n, dtype=int)
    
    # Generar fechas de nacimiento entre dos fechas
    start_date = datetime.strptime('2000-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2010-12-31', '%Y-%m-%d')
    dias_entre_fechas = (end_date - start_date).days
    fechas_nacimiento = [start_date + timedelta(days=np.random.randint(dias_entre_fechas)) for _ in range(n)]
    
    # Potencialmente asignar madres (con un 30% de tener madre asignada)
    tiene_madre = np.random.choice([None, 1], size=n, p=[0.7, 0.3])
    id_numero_pendiente_madre = [np.random.randint(1000, 10000) if madre else None for madre in tiene_madre]
    id_usuario_madre = [1 if madre else 0 for madre in tiene_madre]
    
    # Notas y minPastoVaca
    notas = np.random.choice(['Vaca líder', 'Salud excelente', 'Requiere atención', None], size=n, p=[0.25, 0.25, 0.25, 0.25])
    
    # Crear DataFrame
    df = pd.DataFrame({
        'Numero_pendiente': numeros_pendientes,
        'IdUsuario': id_usuarios,
        'Fecha_nacimiento': fechas_nacimiento,
        'idNumeroPendienteMadre': id_numero_pendiente_madre,
        'idUsuarioMadre': id_usuario_madre,
        'nota': notas
    })
    
    return df

def generar_datos_enfermedades(n,id_vacas):
    np.random.seed(0)  # Para reproducibilidad
    
    # Números pendientes y ID de usuario
    id_usuarios = np.ones(n, dtype=int)  # Asumiendo que todos los ID de usuario son 1 por simplicidad
    numeros_pendientes = np.random.choice(id_vacas,n)
    # Medicamentos y enfermedades
    medicamentos = np.random.choice(['Paracetamol', 'Ibuprofeno', 'Amoxicilina'], size=n)
    enfermedades = np.random.choice(['Gripe', 'Mastitis', 'Cólico'], size=n)
    
    # Fechas de inicio y fin
    start_dates = [datetime.today() - timedelta(days=np.random.randint(1, 100)) for _ in range(n)]
    end_dates = [start + timedelta(days=np.random.randint(5, 30)) for start in start_dates]
    
    # Periodicidad en días
    periodicidades = np.random.randint(1, 10, size=n)  # Periodicidad entre 1 y 9 días
    
    # Notas
    notas = np.random.choice(['Inicio leve, se observa mejoría con el tratamiento.', 
                              'Mantener en observación por posibles recaídas.', 
                              'La vaca muestra buen apetito, signo positivo.',
                              'Tratamiento en curso, seguir protocolo.',
                              None], size=n)
    
    # Crear DataFrame
    df_enfermedades = pd.DataFrame({
        'Numero_pendiente': numeros_pendientes,
        'IdUsuario': id_usuarios,
        'Medicamento': medicamentos,
        'Enfermedad': enfermedades,
        'fecha_inicio': [date.strftime('%Y-%m-%d') for date in start_dates],
        'fecha_fin': [date.strftime('%Y-%m-%d') for date in end_dates],
        'periocidad_en_dias': periodicidades,
        'nota': notas
    })
    
    return df_enfermedades

def generar_datos_partos(n,id_vacas):
    np.random.seed(0)  # Para reproducibilidad
    
    # Números pendientes y ID de usuario
    numeros_pendientes = np.random.choice(id_vacas, size=n)
    id_usuarios = np.ones(n, dtype=int)  # Asumiendo que todos los ID de usuario son 1 por simplicidad
    
    # Fechas de parto
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-12-31', '%Y-%m-%d')
    dias_entre_fechas = (end_date - start_date).days
    fechas_parto = [start_date + timedelta(days=np.random.randint(dias_entre_fechas)) for _ in range(n)]
    
    # Notas sobre los partos
    notas = np.random.choice([
        'Parto sin complicaciones. La madre y el ternero están en buen estado.',
        'Parto asistido. Se observará la recuperación de la madre durante los próximos días.',
        'Parto natural. Se recomienda supervisión continua del ternero.',
        'Parto prematuro. El ternero requiere cuidados intensivos.',
        'Parto con complicaciones menores. Ambos se recuperan satisfactoriamente.',
        'Parto gemelar exitoso. Se monitoreará el desarrollo de ambos terneros.',
        'Parto natural bajo observación. Sin incidencias.',
        'Se necesitó intervención veterinaria para completar el parto. Recuperación en curso.',
        'Parto rápido y sin asistencia. Ternero vigoroso y saludable.',
        ''], size=n, p=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    
    # Crear DataFrame
    df_partos = pd.DataFrame({
        'Numero_pendiente': numeros_pendientes,
        'IdUsuario': id_usuarios,
        'fecha_parto': [date.strftime('%Y-%m-%d') for date in fechas_parto],
        'nota': notas
    })
    
    return df_partos

def es_valido(poligono, otros_poligonos):
    for otro in otros_poligonos:
        if poligono.intersects(otro):
            return False
    return True

def generar_puntos_poligono_convexo(centro, num_puntos, radio_max):
    angulos = np.linspace(0, 2 * np.pi, num_puntos, endpoint=False)
    radios = np.random.uniform(0, radio_max, num_puntos)
    puntos = [(centro[0] + r * np.cos(a), centro[1] + r * np.sin(a)) for r, a in zip(radios, angulos)]
    poligono = Polygon(puntos)
    return poligono

def generar_datos_parcelas(n_parcelas, espacio_disponible):
    poligonos = []
    datos_parcelas = []

    for _ in range(n_parcelas):
        valido = False
        while not valido:
            centro = (
                np.random.uniform(espacio_disponible['min_lat'], espacio_disponible['max_lat']),
                np.random.uniform(espacio_disponible['min_lon'], espacio_disponible['max_lon'])
            )
            poligono = generar_puntos_poligono_convexo(centro, num_puntos=np.random.randint(4, 10), radio_max=0.01)
            
            if es_valido(poligono, poligonos):
                poligonos.append(poligono)
                datos_parcelas.extend([{'id_parcela': len(poligonos), 'latitude': p[1], 'longitude': p[0]} for p in poligono.exterior.coords])
                valido = True
    
    return pd.DataFrame(datos_parcelas)


def generar_coordenadas_gps(vacas_id,parcelas):
    columnas = ['Numero_pendiente', 'latitude', 'longitude', 'fecha', 'anomalia','id_parcela']
    df = pd.DataFrame(columns=columnas)  # Define las columnas de tu DataFrame

    id = 1
    for parcela in  tqdm(parcelas, desc="Procesando parcelas"):
        poligono_parcela = Polygon(parcela)
        min_x, min_y, max_x, max_y = poligono_parcela.bounds
        poligono_parcela
        punto_inicial = Point(uniform(min_x, max_x),uniform(min_y, max_y))
             
        for numero_pendiente in tqdm(vacas_id, desc="Numero_pendiente", leave=False):
            fecha_inicial = datetime.now() - timedelta(days=30)
            punto_anterior = (0,0)
            for num in tqdm(range(1, RANGO), desc="Generando puntos", leave=False):
            
                # Generar 5 puntos aleatorios dentro de la parcela
                anomalia = False
                if PROBABILIDAD_ANOMALIA > random():
                    anomalia = True
                
                puntos_aleatorios = generar_punto_aleatorio_en_parcela(anomalia,poligono_parcela,punto_inicial,punto_anterior=punto_anterior) 
                if (not anomalia):
                    punto_anterior = puntos_aleatorios
                
                if (PONER_ANOMALIAS):
                    new_row = {
                                columnas[0]: int(numero_pendiente),
                                columnas[1]: puntos_aleatorios[0],
                                columnas[2]: puntos_aleatorios[1],
                                columnas[3]: next_date(),
                                columnas[4]: anomalia,
                                columnas[5]: id
                            }
                else:
                    new_row = {
                                columnas[0]: int(numero_pendiente),
                                columnas[1]: puntos_aleatorios[0],
                                columnas[2]: puntos_aleatorios[1],
                                columnas[3]: next_date(),
                                columnas[5]: id
                            }
                df = pd.concat([df, pd.DataFrame([new_row], dtype="object")], ignore_index=True)
        id += 1
    return df[columnas]

def guardar_datos_gps_para_sql(df_gps):
    global PARA_SQL
    if(PARA_SQL):
        fichero = path.join(CARPETA_DATOS_CSV,'datos.sql')
        with open(fichero,'w') as file:
            file.write("""USE muundoGando
INSERT INTO gps (Numero_pendiente,IdUsuario,latitud, longitud,fecha,id_parcela)
VALUES 
""")
            
            for indice_fila in range(0,len(df_gps)):
                fila = df_gps.iloc[indice_fila]
                fecha = f"'{str(fila['fecha']).split('.')[0]}'"
                id_parcela = int(fila['id_parcela'])
                nuermo_pendiente = int(fila['Numero_pendiente'])
                if (indice_fila == len(df_gps)-1):
                    file.write(f"({nuermo_pendiente},1,{fila['latitude']},{fila['longitude']},{fecha},{id_parcela});\n")
                else:
                    file.write(f"({nuermo_pendiente},1,{fila['latitude']},{fila['longitude']},{fecha},{id_parcela}),\n")


if __name__ == "__main__":
    # Generamos las parcelas
    espacio_disponible = {
    'min_lat': 42.208709,
    'max_lat': 8.568751,
    'min_lon': -1.0,
    'max_lon': -1.0
    }
    
    if VERBOSE:
        print("Creando parcelas")
        
    if (parcelas == None):
        df_parcelas = generar_datos_parcelas(NUMERO_PARCELAS, espacio_disponible)
        df_parcelas.to_csv(path.join(CARPETA_DATOS_CSV,'parcelas.csv'),index=False)
        # Organizar el DataFrame en una lista de listas de coordenadas por cada parcela
        parcelas_dict = df_parcelas.groupby('id_parcela').apply(
            lambda x: list(zip(x.latitude, x.longitude))
        ).to_dict()

        # Convertir el diccionario en una lista de parcelas, donde cada parcela es representada por su lista de coordenadas
        parcelas = list(parcelas_dict.values())
    

    if VERBOSE:
        print("Creando vacas")
    # Generamos las vacas
    df_vacas = generar_datos_vacas(NUMERO_DE_VACAS)
    df_vacas.to_csv(path.join(CARPETA_DATOS_CSV,'vacas.csv'),index=False)   
    vacas_id = list(df_vacas['Numero_pendiente'].to_numpy())


    if VERBOSE:
        print("Creando enfermedades")
    df_enfermedades = generar_datos_enfermedades(1000,vacas_id)
    df_enfermedades.to_csv(path.join(CARPETA_DATOS_CSV,'enfermedades.csv'),index=False)


    if VERBOSE:
        print("Creando partos")
    # Generar 100 registros de partos
    df_partos = generar_datos_partos(100,vacas_id)
    df_partos.to_csv(path.join(CARPETA_DATOS_CSV,'partos.csv'),index=False)


    if VERBOSE:
        print("Creando datos gps")
    # Generamos las coordenadas de las vacas
    df_gps = generar_coordenadas_gps(vacas_id,parcelas)
    df_gps.to_csv(path.join(CARPETA_DATOS_CSV,'datos.csv'),index=False)

    # guardamos los datos en fichero sql
    guardar_datos_gps_para_sql(df_gps)

