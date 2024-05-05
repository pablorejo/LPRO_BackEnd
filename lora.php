<?php
include 'conexion.php';


// Abrir el puerto serie USB (reemplazar '/dev/ttyUSB0' con el puerto correcto)
$serial_port = fopen('/dev/ttyUSB0', 'r');
$IdUsuario = 1;

$intervalo = 5 ; // Ejecutar cada 5 minutos
$proximaEjecucion = time() + $intervalo; // Calcula el momento de la próxima ejecución

$id_parcela = null;
$id_fecha = time();

$fecha =  date('Y-m-d h:m:s');

$diccionario = [];
$diccionario = obtenerDiccionario($conexion,$diccionario);
// Datos de procesacmiento
$velocidadAnterior = 0;


$dato_anterior = [];
$dato_actual = []; // Se guarda un => con los datos del gps actual

$posibles_anomalias = []; // Aquí se guardaran las posibles anomalias


// Temporizadores e instancias del inicio de estos para analizar los datos comprobando si son anomalias o no.
$timer_15min_entrar = false;
$instancia_fecha_15min_entrar = date('Y-m-d h:m:s');
$timer_5h_estancia = false;
$instancia_fecha_5h_estancia = date('Y-m-d h:m:s');
$timer_15min_salir = false;
$instancia_fecha_15min_salir = date('Y-m-d h:m:s');
$anomalias_bool = false;

$inicio = true;

$archivo = fopen("pruebas_jesus.txt", 'w');
// // Bucle infinito para leer datos continuamente


while (true) {
    // Leer datos del puerto serie USB
    echo "---";
    $data = fgets($serial_port); // Archivo lora
    // $data = fgets($archivo); // Archivo de pruebas
    
    // Parsear los datos (suponiendo que los datos están separados por comas)
    $datos = explode(",", $data);
    if (count($datos) >= 3) {
        fwrite($archivo,$data);
        $latitud = $datos[0];
        $longitud = $datos[1];
        $rssi = $datos[2];
        $idUsuario =$IdUsuario;


        // Esto se usa para la demostración. Ya que si una vaca sale y entra y solo hay una en esa parcela pues se considera que no entró.
        // if ($inicio){
        //     $Numero_pendiente="1002";
        //     $inicio = false;
        // }else{
        //     $Numero_pendiente="1001";
        // }
        $Numero_pendiente="1001";
        

        // Obtenemos los datos de velocidad y tipo 
        $fecha =  date('Y-m-d H:m:s');
        if (isset($diccionario[$Numero_pendiente])){
            $datos_velocidad = obtenerVelocidad($diccionario[$Numero_pendiente],$latitud,$longitud,$fecha);
            $velocidad = $datos_velocidad[0];
            $tipo = $datos_velocidad[1];
        }else{
            $velocidad = 0;
            $tipo = "Nada";
        }
        

        // Obtenemos los datos de si esta fuera y si está dentro en que parcela está.
        $datos_fuera_del_recinto = fueraDeLaParcela($latitud,$longitud);
        echo $datos_fuera_del_recinto[0];
        $bool_fuera = (strtolower($datos_fuera_del_recinto[0]) == "true")? 1 : 0 ;
        $id_parcela = $datos_fuera_del_recinto[1];

        // Actualizamos los datos anteriores y el actual
        if(isset($dato_actual[$Numero_pendiente])){
            $dato_anterior[$Numero_pendiente] = $dato_actual[$Numero_pendiente];
        }else{
            $dato_anterior[$Numero_pendiente] = [
                'Numero_pendiente' => $Numero_pendiente,
                'latitude' => $latitud,
                'longitude' => $longitud,
                'velocidad' => $velocidad,
                'fuera' => $bool_fuera,
                'anomalia' => false,
                'id_parcela' => $id_parcela,
                'fecha' => $fecha,
                'tipo' => $tipo,
                'rssi' => $rssi
            ];
        }

        $dato_actual[$Numero_pendiente] = [
            'Numero_pendiente' => $Numero_pendiente,
            'latitude' => $latitud,
            'longitude' => $longitud,
            'velocidad' => $velocidad,
            'fuera' => $bool_fuera,
            'anomalia' => false,
            'id_parcela' => $id_parcela,
            'fecha' => $fecha,
            'tipo' => $tipo,
            'rssi' => $rssi
        ];

        // Analizamos el dato para saber si es una anomalia o si hay que guardar las anteriores porque se acabo el timer
        $datos_analizados = analizarDato($dato_actual[$Numero_pendiente], $dato_anterior[$Numero_pendiente]);
        $anomalia = $datos_analizados[0]; 
        $guardar_anomalias = $datos_analizados[1]; // -1 no se guardan, 1 se guardan, 0 no hace nada.

        echo "\n\nDatos: \n-> anomalia: '$anomalia' guardar_anomalias: '$guardar_anomalias' \n";
        echo "-> bool_fuera: '$bool_fuera' id_parcela: '$id_parcela' \n";
        echo "-> velocidad: '$velocidad' tipo: '$tipo' \n";
        echo "-> latitude: '$latitud,$longitud' \n";
        echo "-> rssi: '$rssi' \n";
        echo "-> fecha: '$fecha' \n";

        // En caso de que haya que guardar las anteriores
        if ($guardar_anomalias == 1){ 
            foreach ($posibles_anomalias as $numero => $datos){
                $sql = "INSERT INTO gps (Numero_pendiente ,IdUsuario, latitude, longitude, id_parcela,fecha,velocidad,fuera_del_recinto,anomalia, rssi,tipo) VALUES (?,?,?,?,?,?,?,?,?,?)";
                // Preparar la declaración
                $stmt = $conexion->prepare($sql);
                // Vincular parámetros
                $stmt->bind_param(
                    "iiddisdssis",
                    $datos['Numero_pendiente'],
                    $idUsuario, // Asegúrate de que esta variable está definida y tiene el valor correcto antes del bucle
                    $datos['latitude'],
                    $datos['longitude'],
                    $datos['id_parcela'],
                    $datos['fecha'],
                    $datos['velocidad'],
                    $datos['fuera'],
                    $bool_anomalia = $datos['anomalia'] ? '1' : '0', // Convertir booleano a '1' o '0' para SQL
                    $rssi, // Asumiendo que $rssi está definido correctamente antes del bucle
                    $datos['tipo']
                );

                
                $stmt->bind_param("iiddisdssis",$Numero_pendiente,$idUsuario,$latitud, $longitud,$id_parcela,$fecha,$velocidad,$bool_fuera,$bool_anomalia,$rssi,$tipo);
                
                switch ($tipo) {
                    case 'caminando':
                        $sql = "INSERT INTO gps (Numero_pendiente ,IdUsuario, latitude, longitude, id_parcela,fecha,velocidad,fuera_del_recinto,anomalia, rssi,tipo) VALUES (?,?,?,?,?,?,?,?,?,?)";
                        $stmt = $conexion->prepare($sql);
                        $stmt = $conexion->prepare($sql);
                        # code...
                        break;
                    
                    default:
                        # code...
                        break;
                }
            }
            $posibles_anomalias = []; 
        // En caso de que no haya que guardar las anteriores se descartan
        }elseif($guardar_anomalias == -1){ // -1 indica que no se guarda
            $posibles_anomalias = []; // Eliminamos estos datos.
        }

        // Si anomalias esta a 0 se guarda comoposibles anomaliaas
        if ($anomalia == 0){
            $bool_anomalia = (strtolower($anomalia[0]) === "-1") ? 1 : 0;
            $dato_actual[$Numero_pendiente] = [
                'Numero_pendiente' => $Numero_pendiente,
                'latitude' => $latitud,
                'longitude' => $longitud,
                'velocidad' => $velocidad,
                'fuera' => $bool_fuera,
                'anomalia' => $bool_anomalia,
                'id_parcela' => $id_parcela,
                'fecha' => $fecha,
                'tipo' => $tipo,
                'rssi' => $rssi
            ];

            $posibles_anomalias[] = $dato_actual[$Numero_pendiente];
        }else{
            
            // si esta fuera y se considera anomalia se guarda, si no es anomalia y no está dentro se guarda en otro caso no se guarda
            // if ($bool_fuera == 1 && $anomalia == -1 || ($anomalia == 1 && $bool_fuera == 0)){ // se guarda en caso de que se considere que si esta fuera es una anomalia o no.
                $bool_anomalia = (strtolower($anomalia) === "-1") ? 1 : 0;
                // Preparar la consulta SQL para insertar los datos
                // $sql = "INSERT INTO gps (Numero_pendiente ,IdUsuario, latitude, longitude, id_parcela,fecha,velocidad,fuera_del_recinto,anomalia, rssi,tipo) VALUES (?,?,?,?,?,?,?,?,?,?,?)";
                $sql = "INSERT INTO gps (Numero_pendiente ,IdUsuario, latitude, longitude, id_parcela,velocidad,fuera_del_recinto,anomalia, rssi,tipo) VALUES (?,?,?,?,?,?,?,?,?,?)";

                // Preparar la declaración
                $stmt = $conexion->prepare($sql);
                // Vincular parámetros
                echo $bool_anomalia;
                $stmt->bind_param("iiddidiiis", $Numero_pendiente, $idUsuario, $latitud, $longitud, $id_parcela, $velocidad, $bool_fuera, $bool_anomalia, $rssi, $tipo);
                $stmt->execute();

                // Actualizamos los segundos de la tabla de vacas
                $segundos = 5;
                actualizarVaca($idUsuario,$Numero_pendiente,$tipo,$segundos);

                
                if ($bool_fuera == 1){
                    echo "Llamando.";
                    exec("python3 python/datos.py");
                    $proximaEjecucion = time() + $intervalo; // Reestablece el tiempo para la próxima ejecución
                    echo $salida[0];
                }
            // }
            // Estos datos estan en la granja
           
            // Ejecutar la consulta
            
        }
        $diccionario[$Numero_pendiente] = [$latitud,$longitud,$fecha]; # Guardamos la ultima posicion para saber su velocidad
        echo $diccionario[$Numero_pendiente][2];
        $diccionario = obtenerDiccionario($conexion, $diccionario); #En caso de que se añadan vacas es importante actualizar el diccionario
        echo ' '. $diccionario[$Numero_pendiente][2] ;
    } 

    // Comprobar si es hora de ejecutar analizar_datos()
    // if (time() >= $proximaEjecucion) {

        
    // }


    // Una pequeña pausa para no sobrecargar el CPU
    usleep(20000); // 100 milisegundos
}

/**
 * Funcion para actualizar los segundos de estas pastando segun los segundos
 */
function actualizarVaca($idUsuario,$Numero_pendiente,$tipo,$segundos){
    global $conexion;
    switch ($tipo) {
        case 'caminando':
            $sql = "UPDATE Vaca SET segundos_caminando = segundos_caminando + ? WHERE IdUsuario = ? AND Numero_pendiente = ?";
            $stmt = $conexion->prepare($sql);
            $stmt->bind_param("dii",$segundos,$idUsuario,$Numero_pendiente);
            break;

        case 'pastando':
            $sql = "UPDATE Vaca SET segundos_pastando = segundos_pastando + ? WHERE IdUsuario = ? AND Numero_pendiente = ?";
            $stmt = $conexion->prepare($sql);
            $stmt->bind_param("dii",$segundos,$idUsuario,$Numero_pendiente);
            break;

        case 'descansando':
            $sql = "UPDATE Vaca SET segundos_descansando = segundos_descansando + ? WHERE IdUsuario = ? AND Numero_pendiente = ?";
            $stmt = $conexion->prepare($sql);
            $stmt->bind_param("dii",$segundos,$idUsuario,$Numero_pendiente);
            break;
        
        default:
            # code...
            break;
    }
}

/**
 * Esta funcion obtiene el diccionario de Numero_pendientes y los inicializa con [0,0,""] es decir latitude longitude fecha. 
 */
function obtenerDiccionario($conexion, $diccionario2){

    // Preparar la consulta para obtener los IDs
    $sql = "SELECT Numero_pendiente FROM Vaca where IdUsuario = 1";
    $stmt = $conexion->prepare($sql);

    // Verificar si la preparación fue exitosa
    if ($stmt === false) {
        die("Error en la preparación de la consulta: " . $conexion->error);
    }

    // Ejecutar la consulta
    $stmt->execute();

    // Vincular el resultado a variables
    $id = 1;
    $stmt->bind_result($id);

    // Crear el diccionario con todos los IDs inicializados a 0
    // $diccionario = [];
    while ($stmt->fetch()) {
        if (isset($diccionario2[$id])){
            $diccionario[$id] = $diccionario2[$id];
        }else{
            $diccionario[$id] = [0,0,""];
        }
    }

    // Cerrar el statement
    $stmt->close();
    return $diccionario;
}

/**
 * Obtiene la velocidad mediante un código de python
 */
function obtenerVelocidad($dato_anterior,$latitude,$longitud,$fecha){
    if ($dato_anterior[0] != 0 && $dato_anterior[1] != 0 && $dato_anterior[2] != ""){
        $comando = escapeshellcmd("python3 python/procesar_datos_funciones.py 'velocidad' '$dato_anterior[0]' '$dato_anterior[1]' '$latitude' '$longitud' '$dato_anterior[2]' '$fecha'");
        $comando = str_replace(PHP_EOL, '', $comando); // Elimina saltos de línea del comando
        $fecha = date('Y-m-d h:m:s');
        exec($comando, $velocidad,$codigo_retorno);
        $resultados = explode(',', $velocidad[0]);
    }else{
        $resultados = [0,"Nada"];
    }
    return $resultados;
}

/**
 * Comprueba si está fuera del recinto mediante un codigo de pyhton.
 * Devuelve [boleano si está fuera del recinto, id_parcela en caso de que este dentro de alguno]
 */
function fueraDeLaParcela($latitude,$longitud){
    
    $comando = escapeshellcmd("python3 python/procesar_datos_funciones.py 'fuera_del_recinto' '$latitude' '$longitud'");
    $comando = str_replace(PHP_EOL, '', $comando); // Elimina saltos de línea del comando
    exec($comando, $fuera,$codigo_retorno);
    $resultados = explode(',', $fuera[0]);
    return $resultados;
}

/**
 * Analia el dato para saber si al estar fuera es una anomalia o no.
 * anomalia: -1 si es anomalia, 1 si no lo es, 0 es posible que sea.
 * guardar anomalia: -1 no se guardan, 1 se guardan, 0 no hace nada
 */
function analizarDato($dato_actual, $dato_anterior) {
    global $timer_15min_entrar, $instancia_fecha_15min_entrar;
    global $timer_5h_estancia, $instancia_fecha_5h_estancia;
    global $timer_15min_salir, $instancia_fecha_15min_salir;
    global $anomalias_bool;
    $guardar_anomalias = 0;
    // Actualizamos en timer
    if ($timer_15min_entrar) {
        $quince_minutos = 900;  // 15 minutos en segundos
        $quince_minutos = 60; // Para pruebas
        $diferencia = strtotime($dato_actual['fecha']) - strtotime($instancia_fecha_15min_entrar);
        if ($diferencia > $quince_minutos) {
            echo "Apagando timer_15min_entrar";
            $timer_15min_entrar = false;
            $instancia_fecha_5h_estancia = $dato_actual['fecha'];
            $anomalias_bool = true;
            $guardar_anomalias = 1;
        }
    }

    if ($timer_15min_salir) {
        $quince_minutos = 900;  // 15 minutos en segundos
        $quince_minutos = 60;  // 15 minutos en segundos
        $diferencia = strtotime($dato_actual['fecha']) - strtotime($instancia_fecha_15min_salir);
        if ($diferencia > $quince_minutos) {
            echo "Apagando timer_15min_salir";
            $timer_15min_salir = false;
            $anomalias_bool = false;
        }

        if (estan_todos_fuera($dato_actual['id_parcela'])) {
            $guardar_anomalias = -1;
        } else {
            $guardar_anomalias = 1;
        }
    }

    if ($timer_5h_estancia) {
        $cinco_horas = 18000;  // 5 horas en segundos
        $cinco_horas = 120;  // para preubas 5 horas en segundos
        $diferencia = strtotime($dato_actual['fecha']) - strtotime($instancia_fecha_5h_estancia);
        if ($diferencia > $cinco_horas) {
            echo "Apagando timer_5h_estancia";
            $timer_5h_estancia = false;
            $anomalias_bool = false;
        }
    }


    $anomalia = 1; // a priori decimos que no hay

    // Si el punto actual está fuera
    if ($dato_actual['fuera']) {
        if ($anomalias_bool) {
            $anomalia = -1;
        } else {
            if (!$dato_anterior['fuera']) {
                if ($timer_15min_salir) {
                    $anomalia = 0;
                } elseif (!$timer_15min_entrar) {
                    $timer_15min_salir = true;
                    $instancia_fecha_15min_salir = $dato_actual['fecha'];
                }
            } else {
                if ($timer_15min_salir) {
                    $anomalia = 0;
                }
            }
        }
    } else {
        if ($dato_anterior['fuera']) {
            if (!$timer_15min_salir) {
                $timer_15min_entrar = true;
                $instancia_fecha_15min_entrar = $dato_actual['fecha'];
            }
            $anomalia = 1;
        }
    }

    // anomalia contine un -1 si es anomalia un 0 si no se sabe y un 1 si no lo es.
    // guardar_anomalias un -1 si no la hay que guardar un 1 si la hay que guardar un 0 si no hay que hacer
    return [$anomalia,$guardar_anomalias];
}


function estan_todos_fuera($id_parcela){
    $comando = escapeshellcmd("python3 python/procesar_datos_funciones.py 'estan_todos_fuera' '$id_parcela'");
    $comando = str_replace(PHP_EOL, '', $comando); // Elimina saltos de línea del comando
    exec($comando, $fuera,$codigo_retorno);
    $bool_fuera = (strtolower($fuera[0]) === "true");
    return $bool_fuera;
}


$conexion->close();

?>

