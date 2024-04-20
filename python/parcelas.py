import bd as bd
from shapely.geometry import Polygon
import mysql.connector


# Definir los parámetros de conexión
hostname = 'localhost'
database = 'muundoGando'
username = 'root'
password = 'LPRO_2024'

# Parametros para los datos de la BD
idUsuario = 1
idParcela = 1

minuto_metroCuadrado = 7.5  #min./m^2
BOCADOS_MIN = 60            #bocados/min.
VOLUMEN_BOCADO = 0.4        #g_pasto/bocado

# Conectar a la base de datos
try:
    connection = mysql.connector.connect(
        host=hostname,
        database=database,
        user=username,
        password=password
    )
    if connection.is_connected():
        print('Conexión exitosa a la base de datos')

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        numVacas = bd.getVacas(cursor, idUsuario)

        resultados = bd.getCoordenadasParcela(cursor, idUsuario, idParcela)

        # Crear listas vacías para almacenar las latitudes y longitudes
        latitudes_parcela = []
        longitudes_parcela = []

        # Iterar sobre los resultados y almacenar en las listas correspondientes
        for fila in resultados:
            latitud_parcela.append(fila[0])
            longitud_parcela.append(fila[1])

        areaParcela = calcular_area(longitudes_parcela,latitudes_parcela)

        print("Área del polígono:", areaParcela)
        
        volumenPastoVacaHora = 60 * BOCADOS_MIN * VOLUMEN_BOCADO

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()
        print('Conexión cerrada')
        
except mysql.connector.Error as error:
    print('Error al conectar a la base de datos:', error)




def calcular_area(longitudes, latitudes):
    # Crear una lista de coordenadas (longitud, latitud)
    coords = [(longitud, latitud) for longitud, latitud in zip(longitudes, latitudes)]
    
    # Agregar el primer punto al final para cerrar el polígono
    coords.append(coords[0])
    
    # Crear un objeto Polygon
    poligono = Polygon(coords)
    
    # Calcular el área del polígono
    area = poligono.area
    
    return area
