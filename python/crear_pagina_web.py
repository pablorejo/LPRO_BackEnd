from random import randint
import pandas as pd
import folium
from folium.plugins import HeatMap
from conf import *

def crar_figura_mapa(mapa: folium.Map,parcela: list):
    
    # Asegurándonos de que 'parcela' es una lista de tuplas (lat, lon)
    # y usamos folium.Polygon para parcelas de terreno con múltiples esquinas
    folium.Polygon(
        locations=parcela,  # Lista de puntos que definen la parcela
        color='#ff7800',
        fill=True,
        fill_color='#ffff00',
        fill_opacity=0.2
    ).add_to(mapa)
  

df = pd.read_csv('datos.csv')
def generar_color_aleatorio():
    # "#3388ff"
    randint(1, 16777215)
    color = '#' + str(hex(randint(1, 16777215))).split('x')[1]
    return color

print ("Datos guardados")


# Crea un mapa centrado en las coordenadas medias
mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)


crar_figura_mapa(mapa,parcelas[0])
# Agrupa el DataFrame por 'Numero_pendiente'
colores = ['red', 'blue']
i = 0
for _, group in df.groupby('Numero pendiente'):
    puntos = group[['latitude', 'longitude']].values
    # Añade los puntos al mapa
    folium.PolyLine(puntos, color=generar_color_aleatorio(), weight=2.5, opacity=1).add_to(mapa)
    for punto in puntos:
        folium.CircleMarker(location=punto, radius=3, color='blue', fill=True).add_to(mapa)
    i +=1


# Mostrar el mapa
mapa.save('mapa_de_posicion.html')

mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)
crar_figura_mapa(mapa,parcelas[0])
# Crear el mapa de calor
HeatMap(data=df[['latitude', 'longitude']].values, radius=15).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save('mapa_de_calor.html')