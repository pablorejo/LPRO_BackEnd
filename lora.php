<?php
include 'conexion.php';

function analizar_datos($IdUsuario)
{
    $comando = escapeshellcmd("python3 python/procesar_datos.py '$IdUsuario'");
    $comando = str_replace(PHP_EOL, '', $comando); // Elimina saltos de línea del comando

    exec($comando, $salida,$codigo_retorno);
}

// Abrir el puerto serie USB (reemplazar '/dev/ttyUSB0' con el puerto correcto)
$serial_port = fopen('/dev/ttyUSB0', 'r');

$IdUsuario = 1;


$intervalo = 5 * 60; // Ejecutar cada 5 minutos
$proximaEjecucion = time() + $intervalo; // Calcula el momento de la próxima ejecución

// Bucle infinito para leer datos continuamente
while (true) {
    // Leer datos del puerto serie USB
    $data = fgets($serial_port);
    // echo $data;

    // Parsear los datos (suponiendo que los datos están separados por comas)
    $datos = explode(",", $data);
    if (count($datos) >= 3) {
            // echo "Datos recibidos: " . $data;
        // Obtener latitud y longitud de los datos recibidos
        $latitud = $datos[0];
        $longitud = $datos[1];
        $rssi = $datos[2];
        $idUsuario =$IdUsuario;
        $Numero_pendiente="1001";
        // Preparar la consulta SQL para insertar los datos
        $sql = "INSERT INTO gps (Numero_pendiente,IdUsuario,latitud, longitud, rssi) VALUES (?,?,?,?,?)";

        // Preparar la declaración
        $stmt = $conexion->prepare($sql);

        // Vincular parámetros
        $stmt->bind_param("iiddd",$Numero_pendiente,$idUsuario,$latitud, $longitud,$rssi);

        // Ejecutar la consulta
        $stmt->execute();
        echo $latitud;
        echo $longitud; 
        echo $rssi;
        echo $idUsuario;
        echo  $Numero_pendiente;
    } 
    // Comprobar si es hora de ejecutar analizar_datos()
    if (time() >= $proximaEjecucion) {
        analizar_datos($IdUsuario);
        $proximaEjecucion = time() + $intervalo; // Reestablece el tiempo para la próxima ejecución
    }


    // Una pequeña pausa para no sobrecargar el CPU
    usleep(20000); // 100 milisegundos
}

$conexion->close();
?>


