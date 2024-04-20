import pandas as pd
import numpy as np

# Este codigo comprueba las distancias medias entre las vacas en un instante concreto
# Para tener en cuenta cuales estan muy alejadas de las demas guardamos el percentil-95%, es decir nos da el valor por el cual el 95% de los animales esta por debajo de este numero.
def haversine(lon1, lat1, lon2, lat2):
    """
    Calcula la distancia en kilómetros entre dos puntos en la superficie de la Tierra.
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371 # Radio de la Tierra en kilómetros
    return c * r

# Cargar datos
data = pd.read_csv('datos.csv')
data['fecha'] = pd.to_datetime(data['fecha'])
data['fecha_redondeada'] = data['fecha'].dt.floor('T')  # 'T' es un código de frecuencia para minutos

# Calcular la posición promedio de todo el ganado en cada instante
data['pos_promedio_lat'] = data.groupby('fecha_redondeada')['latitude'].transform('mean')
data['pos_promedio_lon'] = data.groupby('fecha_redondeada')['longitude'].transform('mean')

# Calcular la distancia de cada vaca a la posición promedio
data['distancia_a_promedio'] = data.apply(lambda row: haversine(row['longitude'], row['latitude'], 
                                                                 row['pos_promedio_lon'], row['pos_promedio_lat']), axis=1)

# Definir un umbral para considerar una vaca "muy alejada"
umbral_distancia = data['distancia_a_promedio'].quantile(0.95) #vamos a especificar que es raro si esta por encima del percentil 95%

# Identificar las instancias donde una vaca está muy alejada del resto
vacas_alejadas = data[data['distancia_a_promedio'] > umbral_distancia]

data.to_csv('distancias.csv',index=False)
    
print(vacas_alejadas)
