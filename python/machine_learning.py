import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # para visualización bonita



def distancia(lon1, lat1, lon2, lat2):
    # Radio de la Tierra en kilómetros
    R = 6371.0
    
    # Convertir coordenadas de grados a radianes
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    
    # Diferencia de coordenadas
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # Fórmula de Haversine
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c
    
    return distance
# Carga de datos
df = pd.read_csv('datos.csv')
df['distancia_km'] = np.concatenate([[0], distancia(df['longitud'][:-1].values, df['latitud'][:-1].values, df['longitud'][1:].values, df['latitud'][1:].values)])
df['velocidad_kmh'] = df['distancia_km'] / 0.25 # como es cada 15 min es cada 0.25 (1/4)horas 

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

latitud_max, longitud_max = parsear_cordenadas("43°18'47.4\"N 8°25'10.4\"W")
latitud_min, longitud_min = parsear_cordenadas("43°18'37.6\"N 8°24'56.2\"W")

# Convertir la columna 'fecha' a datetime si aún no lo es

# corregir min y max
if (latitud_max < latitud_min):
    temporal = latitud_min
    latitud_min = latitud_max
    latitud_max = temporal

if (longitud_max < longitud_min):
    temporal = longitud_min
    longitud_min = longitud_max
    longitud_max = temporal
    
# Determinar si las coordenadas están fuera del recinto
df['fuera_del_recinto'] = ~df.apply(lambda x: latitud_min <= x['latitud'] <= latitud_max and longitud_min <= x['longitud'] <= longitud_max, axis=1)


from sklearn.ensemble import IsolationForest
from datetime import datetime

def fecha_hora_a_entero(fecha_hora_str):
    """
    Convierte una fecha y hora en formato string a un número entero.
    
    Parámetros:
    - fecha_hora_str (str): La fecha y hora en formato string, esperado en el formato "AAAA-MM-DD HH:MM:SS.ssssss".
    
    Retorna:
    - int: Un número entero que representa la fecha y hora.
    """
    # Convertir la cadena de fecha y hora a un objeto datetime
    fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M:%S.%f")
    
    # Convertir la fecha y hora a un número entero (formato AAAAMMDDHHMMSS)
    fecha_hora_entero = int(fecha_hora.strftime("%Y%m%d%H%M%S"))
    
    return fecha_hora_entero

df['fecha'] = df['fecha'].apply(fecha_hora_a_entero)
# Asumiendo que 'longitud' y 'latitud' son tus características
X = df[['Numero_pendiente','longitud', 'latitud','fecha','anomalia','distancia_km','velocidad_kmh','fuera_del_recinto']]
X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

# Instanciar y entrenar el modelo
model = IsolationForest(n_estimators=10000, contamination='auto')

model.fit(X)

# Realizar las predicciones con Isolation Forest
df['anomalia_prediccion'] = model.predict(X)

# Convertir las predicciones: -1 se convierte en True (anomalía), 1 se convierte en False (normal)
df['anomalia_prediccion'] = df['anomalia_prediccion'] == -1



# Filtrar los datos anómalos
anomalias = df[df['anomalia_prediccion'] == -1]

df.to_csv('datos_velocidad.csv')

# Contar y imprimir el número de anomalías
n_anomalias = np.sum(anomalias)
print(f'Número total de anomalías detectadas: {n_anomalias}')

# Calcular la matriz de confusión
matriz_conf = confusion_matrix(df['anomalia'], df['anomalia_prediccion'])

# Visualizar la matriz de confusión
plt.figure(figsize=(10,7))
sns.heatmap(matriz_conf, annot=True, fmt='d',
            xticklabels=['No anomalia', 'anomalia'],
            yticklabels=['No anomalia', 'anomalia'])
plt.ylabel('Valores de prediccion')
plt.xlabel('Valores reales')
plt.show()


