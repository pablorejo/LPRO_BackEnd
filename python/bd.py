import mysql.connector

def getVacas(cursor, idUsuario):
    # Ejecutar una consulta SQL
    consulta = "SELECT COUNT(Numero_pendiente) FROM Vaca WHERE IdUsuario = {idUsuario}"
    cursor.execute(consulta)

    # Obtener los resultados de la consulta
    numeroVacas = cursor.fetchall()

    return numeroVacas


def getCoordenadasParcela(cursor, idUsuario, idParcela):
    # Ejecutar una consulta SQL
    consulta = "SELECT c.latitude, c.longitude \
                FROM coordenadas c \
                JOIN parcela p ON c.id_parcela = p.id_parcela \
                WHERE p.id_parcela = {idParcela} AND p.IdUsuario = {idUsuario}"
    cursor.execute(consulta)

    # Obtener los resultados de la consulta
    latitud_longitud = cursor.fetchall()

    return latitud_longitud


