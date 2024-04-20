from shapely.geometry import Polygon
import pandas as pd
import gmplot

# ******************************************************************* #
# ***************************** FUNCIONES *************************** # 
# ******************************************************************* #

# Función para el calculo del area de 
# parcelas y sectores a traves de coordenadas:
def calcular_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[i][1] * vertices[j][0]
    return abs(area) / 2

def calculoAreaSector(tiempoPastado, minPasto_m2):
    areaSector = tiempoPastado * (1/minPasto_m2)
    print("Área del Sector: ", areaSector, "m2")
    return areaSector


def conexionBD(host, database, user, password):
    # Construir la cadena de conexión
    conexion = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    # Verificar si la conexión se realizó con éxito
    if conexion.is_connected():
        print("Conexión exitosa")
        return conexion


# Función para coger las vacas de la BD:
def getVacas(cursor, idUsuario):
    # Ejecutar una consulta SQL
    consulta = f"SELECT COUNT(Numero_pendiente) FROM Vaca WHERE IdUsuario = {str(idUsuario)}"
    cursor.execute(consulta)
    pd.read_sql_query()
    # Obtener los resultados de la consulta
    numeroVacas = cursor.fetchall()

    return numeroVacas[0][0]

# Función para coger las coordenadas de la parcela de la BD:
def getCoordenadasParcela(cursor, idUsuario, idParcela):
    # Ejecutar una consulta SQL
    consulta = "SELECT c.latitude, c.longitude \
                FROM coordenadas c \
                JOIN parcela p ON c.id_parcela = p.id_parcela \
                WHERE p.id_parcela=" + str(idParcela) + " AND p.IdUsuario=" + str(idUsuario) 
    cursor.execute(consulta)
    
    

    # Obtener los resultados de la consulta
    latitud_longitud = cursor.fetchall()

    return latitud_longitud

def getMinPastoVacas(cursor, idUsuario):
    consulta = "SELECT minPastoVaca \
                FROM Vaca \
                WHERE IdUsuario =" + str(idUsuario)

    cursor.execute(consulta)

    # Obtener los resultados de la consulta
    minPastoConsulta = cursor.fetchall()

    minPastoVaca = [tupla[0] for tupla in minPastoConsulta]

    minPasto = sum(minPastoVaca)
    return minPasto

    


# ******************************************************************* #
# ******************************* MAIN ****************************** # 
# ******************************************************************* #
# Definir los parámetros de conexión
hostname = 'localhost'
database = 'muundoGando'
username = 'root'
password = 'LPRO_2024'

# Definir los parámetros para realizar consultas:
idUsuario = 1
idParcela = 1

# Constantes calculo área pastada:
minMetroCuadradoPastoMedio = 7.5	#min/m2
minMetroCuadradoPastoPeorCaso = 5	#min/m2

conexion = conexionBD(hostname, database, username, password)
cursor = conexion.cursor()

numVacas = getVacas(cursor, idUsuario)
#print(numVacas)

coordenadas = getCoordenadasParcela(cursor, idUsuario, idParcela)
print(coordenadas)

areaParcela = calcular_area(coordenadas)
areaParcela = 10**10*areaParcela

print("El área del polígono es:", areaParcela, "m2")
#print("El área del polígono es:", area1, "m2")

# Crear un objeto de polígono Shapely para la extensión de tierra
extencion_poligono = Polygon(coordenadas)

# Calcular el centroide del polígono
centroide = extencion_poligono.centroid

# Calculo del área deseada para pastar:
minPasto = getMinPastoVacas(cursor, idUsuario)
areaSector = calculoAreaSector(minPasto, minMetroCuadradoPastoPeorCaso)

# ************************************************** #
# EXTRA: Calculo del area Pastada:
areaPastada = calculoAreaSector(minPasto, minMetroCuadradoPastoMedio)
areaParcelaRestante = areaParcela - (areaSector)
print("Área restante de la Parcela: ", areaParcelaRestante, "m2")
# ************************************************** #

# # Calcular el radio necesario para el área deseada
# radio = (areaSector / extencion_poligono.area) ** 0.5

# # Crear un círculo centrado en el centroide con el radio calculado
# circulo = centroide.buffer(radio)

# # Intersectar el círculo con la extensión de tierra para obtener la división
# sector = extencion_poligono.intersection(circulo)

# coordenadasSector = sector.exterior.coords[:]
# # Imprimir las coordenadas de la división
# #print(coordenadasSector)

# # Extraer latitudes y longitudes
# lats, lons = zip(*coordenadasSector)

# # Inicializar el objeto gmplot
# gmap = gmplot.GoogleMapPlotter(lats[0], lons[0], 18)

# # Dibujar el polígono
# gmap.plot(lats, lons, 'cornflowerblue', edge_width=5)

# # Guardar el mapa como HTML
# gmap.draw("mapaSector.html")

# print("Mapa generado. Abre el archivo 'mapaSector.html' en tu navegador web para ver el mapa.")

# # Extraer latitudes y longitudes
# lats, lons = zip(*coordenadas)

# # Inicializar el objeto gmplot
# gmap = gmplot.GoogleMapPlotter(lats[0], lons[0], 18)

# # Dibujar el polígono
# gmap.plot(lats, lons, 'cornflowerblue', edge_width=5)

# # Guardar el mapa como HTML
# gmap.draw("mapa.html")

# print("Mapa generado. Abre el archivo 'mapa.html' en tu navegador web para ver el mapa.")





