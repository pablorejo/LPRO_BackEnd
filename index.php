<?php
include 'conexion.php';
session_start();
header("Content-Type: application/json");
$requestMethod = $_SERVER["REQUEST_METHOD"];
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$uri = explode( '/', $uri );
// Obtener el JSON recibido
// Decodificar el JSON a un array asociativo
$IdUsuario= $_SESSION['user_id'];
$ficheros = file_get_contents("php://input");

$data = json_decode($ficheros);

switch ($requestMethod) {
    case 'GET':
        if($uri[1] =='parcelas'){
                        
            // Las contraseñas coinciden
            $sentencia = $conexion->prepare("SELECT c.latitude, c.longitude FROM coordenadas c JOIN parcela p ON c.id_parcela = p.id_parcela WHERE p.IdUsuario = ?");
            $sentencia->bind_param('i',$IdUsuario);

            // Ejecutar la sentencia
            $sentencia->execute();

            // Obtener el resultado
            $resultado = $sentencia->get_result();

            $COORDENADAS = [];    
            // Recorrer los resultados
            while ($fila = $resultado->fetch_assoc()) {
                $COORDENADAS[]= $fila; // Añadir cada fila al array de vacas
            }


            if (count($COORDENADAS) > 0) {
                echo json_encode($COORDENADAS);
            } else {
                echo json_encode(["mensaje" => "No hay parcelas asociadas con el usuario " . $IdUsuario]);
            }
            break;

        }elseif($uri[1] =='vacas'){
            if(isset($uri[2])&&isset($uri[3])){
                switch ($uri[3]) {
                    case 'enfermedades':
                        $id_vaca = (int)$uri[2];
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("SELECT * FROM Enfermedades
                        WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        $sentencia->bind_param('ii',$id_vaca,$IdUsuario);
    
                        // Ejecutar la sentencia
                        $sentencia->execute();
    
                        // Obtener el resultado
                        $resultado = $sentencia->get_result();

                        $enferemedades = [];    
                        // Recorrer los resultados
                        while ($fila = $resultado->fetch_assoc()) {
                            $enferemedades[] = $fila; // Añadir cada fila al array de vacas
                        }


                        if (count($enferemedades) > 0) {
                            echo json_encode($enferemedades);
                        } else {
                            echo json_encode(["mensaje" => "No hay enfermedades asociadas con el usuario " . $IdUsuario]);
                        }
                        break;
                        
                    case 'fechas_parto':
                        $id_vaca = (int)$uri[2];
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("SELECT * FROM Partos
                        WHERE Numero_pendiente = ? AND IdUsuario = ?");

                        $sentencia->bind_param('ii',$id_vaca, $IdUsuario);
    
                        // Ejecutar la sentencia
                        $sentencia->execute();
    
                        // Obtener el resultado
                        $resultado = $sentencia->get_result();
                        $partos = [];    
                        // Recorrer los resultados
                        while ($fila = $resultado->fetch_assoc()) {
                            $partos[] = $fila; // Añadir cada fila al array de vacas
                        }


                        if (count($partos) > 0) {
                            echo json_encode($partos);
                        }  else {
                            echo json_encode(["mensaje" => "fechas_parto no encontrado"]);
                        }
                        break;
                        
                    case 'volumen_leche':
                        $id_vaca = (int)$uri[2];
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("SELECT * FROM Leite
                        WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        $sentencia->bind_param('ii',$id_vaca,$IdUsuario);
    
                        // Ejecutar la sentencia
                        $sentencia->execute();
    
                        // Obtener el resultado
                        $resultado = $sentencia->get_result();
                        $leite = [];    
                        // Recorrer los resultados
                        while ($fila = $resultado->fetch_assoc()) {
                            $leite[] = $fila; // Añadir cada fila al array de vacas
                        }


                        if (count($leite) > 0) {
                            echo json_encode($leite);
                        } else {
                            echo json_encode(["mensaje" => "volumen_leche no encontrado"]);
                        }
                        break;
                        
                    case 'dias_pasto':
                        $id_vaca = (int)$uri[2];
                        
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("SELECT * FROM Pasto
                        WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        $sentencia->bind_param('ii',$id_vaca,  $IdUsuario);
    
                        // Ejecutar la sentencia
                        $sentencia->execute();
    
                        // Obtener el resultado
                        $resultado = $sentencia->get_result();
                        $pastos = [];    
                        // Recorrer los resultados
                        while ($fila = $resultado->fetch_assoc()) {
                            $pastos[] = $fila; // Añadir cada fila al array de vacas
                        }


                        if (count($pastos) > 0) {
                            echo json_encode($pastos);
                        } else {
                            echo json_encode(["mensaje" => "dias_pasto no encontrado"]);
                        }
                        break;
                  
                    case 'gps':
                        $id_vaca = (int)$uri[2];
                        
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("SELECT * FROM gps
                        WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        $sentencia->bind_param('ii',$id_vaca,  $IdUsuario);
    
                        // Ejecutar la sentencia
                        $sentencia->execute();
    
                        // Obtener el resultado
                        $resultado = $sentencia->get_result();
                        $pastos = [];    
                        // Recorrer los resultados
                        while ($fila = $resultado->fetch_assoc()) {
                            $pastos[] = $fila; // Añadir cada fila al array de vacas
                        }


                        if (count($pastos) > 0) {
                            echo json_encode($pastos);
                        } else {
                            echo json_encode(["mensaje" => "dias_pasto no encontrado"]);
                        }
                        break;

                    default:
                        header("HTTP/1.1 404 Not Found");
                        exit();
                }

            }elseif(isset($uri[2])&& $uri='puerta'){
                                                
                // Las contraseñas coinciden
                $sentencia = $conexion->prepare("SELECT * FROM puerta
                WHERE IdUsuario = ?");
                $sentencia->bind_param('i',$IdUsuario);

                // Ejecutar la sentencia
                $sentencia->execute();

                // Obtener el resultado
                $resultado = $sentencia->get_result();
                $usuario = $resultado->fetch_assoc();

                if ($usuario) {
                    echo json_encode($usuario);
                } else {
                    echo json_encode(["mensaje" => "puerta no encontrada"]);
                }

            
            }elseif(isset($uri[2])&& $uri='gps'){
                                                
                // Las contraseñas coinciden
                $sentencia = $conexion->prepare("SELECT * FROM gps
                WHERE IdUsuario = ?");
                $sentencia->bind_param('i',$IdUsuario);

                // Ejecutar la sentencia
                $sentencia->execute();
                
                // Obtener el resultado
                $resultado = $sentencia->get_result();
                $usuario = $resultado->fetch_assoc();

                if ($usuario) {
                    echo json_encode($usuario);
                } else {
                    echo json_encode(["mensaje" => "gps no encontrado"]);
                }

            
            }elseif(isset($uri[2])){
                //cogemos una vaca con el id
                $id_vaca = (int)$uri[2];
                                                
                // Las contraseñas coinciden
                $sentencia = $conexion->prepare("SELECT * FROM Vaca
                WHERE Numero_pendiente = ?  AND IdUsuario = ?");
                $sentencia->bind_param('ii', $id_vaca,$IdUsuario);

                // Ejecutar la sentencia
                $sentencia->execute();

                // Obtener el resultado
                $resultado = $sentencia->get_result();
                $usuario = $resultado->fetch_assoc();

                if ($usuario) {
                    echo json_encode($usuario);
                } else {
                    echo json_encode(["mensaje" => "Vaca no encontrada"]);
                }

            }else{
                //todas las vacas
                $sentencia = $conexion->prepare("SELECT * FROM Vaca WHERE IdUsuario = ?");
                $sentencia->bind_param('i', $IdUsuario);

                // Ejecutar la sentencia
                $sentencia->execute();

                // Obtener el resultado
                $resultado = $sentencia->get_result();
                
                $vacas = [];    
                // Recorrer los resultados
                while ($fila = $resultado->fetch_assoc()) {
                    $vacas[] = $fila; // Añadir cada fila al array de vacas
                }

                if (count($vacas) > 0) {
                    echo json_encode($vacas);
                } else {
                    echo json_encode(["mensaje" => "No existen vacas para el usuario " . $IdUsuario]);
                }
            }
        }
        break;

    case 'PUT':

        if($uri[1] =='parcelas'){
            // Obtener los datos de la parcela
            $id_parcela = $data->id_parcela;
            $nombreParcela = $data->nombre_parcela;

            // Iniciar una transacción para garantizar la consistencia de los datos
            $conexion->begin_transaction();
            
            // Actualizar la información de la parcela en la tabla 'parcela'
            $sentenciaParcela = $conexion->prepare("UPDATE parcela SET nombre_parcela = ?, IdUsuario = ? WHERE id_parcela = ?");
            $sentenciaParcela->bind_param("sii", $nombreParcela, $IdUsuario, $id_parcela);
            $sentenciaParcela->execute();

            // Verificar si la actualización de la parcela fue exitosa
            $actualizoAlgunaCoordenada = false;
            // Insertar las nuevas coordenadas en la tabla 'coordenadas'
            $coordenadas = $data->coordenadas;
            
            foreach ($coordenadas as $coordenada) {
                $latitude = $coordenada->latitude;
                $longitude = $coordenada->longitude;
                $id_esquina = $coordenada->id_esquina;
                
                $sentenciaActualizarCoordenadas = $conexion->prepare("UPDATE coordenadas SET latitude = ?, longitude = ? WHERE id_esquina = ? and id_parcela = ?");
                $sentenciaActualizarCoordenadas->bind_param("ddii",  $latitude, $longitude, $id_esquina , $id_parcela);
                $sentenciaActualizarCoordenadas->execute();

                if ($sentenciaActualizarCoordenadas->affected_rows > 0) {
                    $actualizoAlgunaCoordenada = true;
                }
            }

            if ($sentenciaParcela->affected_rows > 0 or $actualizoAlgunaCoordenada){
                $conexion->commit();
                echo json_encode(["mensaje" => "Parcela actualizada correctamente"]);
            }else{
                echo json_encode(["mensaje" => "La parcela no tiene cambios"]);
            }
                        
        }elseif($uri[1] =='usuarios'){
                                                
            $nuevoCorreo = $data->correo;
                $nuevaContraseña =$data->usu_password;
                $nuevoNombre = $data->nombre;
                $nuevosApellidos = $data->apellidos;
            
                // Las contraseñas coinciden
                $sentencia = $conexion->prepare("UPDATE usuario SET correo = ?, usu_password = ?, nombre = ?, apellidos = ? WHERE id = ?");
                $sentencia->bind_param("ssssi", $nuevoCorreo, $nuevaContraseña, $nuevoNombre, $nuevosApellidos, $IdUsuario);
                
                // Ejecutar la sentencia
                $sentencia->execute();

                // Verificar si la actualización fue exitosa
                if ($sentencia->affected_rows > 0) {
                    echo json_encode(["mensaje" => "Usuario actualizado correctamente"]);
                } else {
                    echo json_encode(["mensaje" => "No se pudo encontrar el usuario para actualizar"]);
                }

        }elseif($uri[1] =='vacas'){
            if(isset($uri[2])){
                switch ($uri[2]) {
                    case 'enfermedades':
                        $id_enfermedad_vaca =$data->id_enfermedad_vaca;
                        $Numero_pendiente = $data->Numero_pendiente;
                        $Enfermedad =  $data->Enfermedad;
                        $fecha_inicio =  $data->fecha_inicio;
                        $fecha_fin =  $data->fecha_fin;
                        $Medicamento= $data->Medicamento;
                        $periocidad_en_dias = $data->periocidad_en_dias;
                        $nota = $data->nota;
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("UPDATE Enfermedades SET nota = ?, Medicamento = ?, Enfermedad = ?, fecha_inicio = ?, fecha_fin = ?, periocidad_en_dias = ? WHERE id_enfermedad_vaca = ? AND Numero_pendiente = ?");
                        $sentencia->bind_param("sssssiii", $nota, $Medicamento, $Enfermedad, $fecha_inicio,$fecha_fin,$periocidad_en_dias, $id_enfermedad_vaca, $Numero_pendiente);
                        
                        
                        // Ejecutar la sentencia
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0) {
                                echo json_encode(["mensaje" => "Enfermedad actualizada correctamente"]);
                            } else {
                                echo json_encode(["mensaje" => "No se actualizó"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error ejecutando la actualización: " . $sentencia->error]);
                        }
                        break;
                      
                        
                    case 'fechas_parto':
                        $Numero_pendiente = $data->Numero_pendiente;
                        $fecha_parto = $data->fecha_parto;
                        $id_vaca_parto= $data->id_vaca_parto;
                        $nota = $data->nota;
                    
                    
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("UPDATE Partos SET Numero_pendiente = ?, fecha_parto = ?, nota = ? WHERE id_vaca_parto = ?");
                        $sentencia->bind_param("issi", $Numero_pendiente,$fecha_parto,$nota, $id_vaca_parto);
                        
        
                        // Ejecutar la sentencia
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0) {
                                echo json_encode(["mensaje" => "Parto actualizado correctamente"]);
                            } else {
                                echo json_encode(["mensaje" => "No se actualizó"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error ejecutando la actualización: " . $sentencia->error]);
                        }
                        break;

                    case 'volumen_leche':
                        $Numero_pendiente = $data->Numero_pendiente;
                        $litros = $data->litros;
                        $fecha_recogida = $data->fecha_recogida;
                        $id_vaca_leite= $data->id_vaca_leite;
                    
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("UPDATE Leite SET Numero_pendiente = ?, litros = ?, fecha_recogida = ? WHERE id_vaca_leite = ?");
                        $sentencia->bind_param("idsi", $Numero_pendiente,$litros,$fecha_recogida, $id_vaca_leite);
                        
        
                        // Ejecutar la sentencia
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0) {
                                echo json_encode(["mensaje" => "Leche actualizada correctamente"]);
                            } else {
                                echo json_encode(["mensaje" => "No se actualizó"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error ejecutando la actualización: " . $sentencia->error]);
                        }
                        break;

                    case 'dias_pasto':
                        $id_vaca_pasto = $data->id_vaca_pasto;
                        $Numero_pendiente = $data->Numero_pendiente;
                        $dias_de_pasto = $data->dias_de_pasto;
                        $mes_de_pastore = $data->mes_de_pastore;
                        
                    
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("UPDATE Pasto SET Numero_pendiente = ?, dias_de_pasto = ?, mes_de_pastore = ? WHERE id_vaca_pasto = ?");
                        $sentencia->bind_param("iisi", $Numero_pendiente,$dias_de_pasto,$mes_de_pastore, $id_vaca_pasto);
                        
        
                        // Ejecutar la sentencia
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0) {
                                echo json_encode(["mensaje" => "Pasto actualizado correctamente"]);
                            } else {
                                echo json_encode(["mensaje" => "No se actualizó"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error ejecutando la actualización: " . $sentencia->error]);
                        }

                        break;
                    case 'puerta':
                        $id_puerta = $data->id_puerta;
                        $hora_apertura = $data->hora_apertura;
                        $hora_cierre = $data->hora_cierre;
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("UPDATE puerta SET hora_apertura = ?, hora_cierre = ? WHERE id_puerta = ?");
                        $sentencia->bind_param("ssi",$hora_apertura,$hora_cierre, $id_puerta);
                        
        
                        // Ejecutar la sentencia
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0) {
                                echo json_encode(["mensaje" => "Puerta actualizada correctamente"]);
                            } else {
                                echo json_encode(["mensaje" => "No se actualizó"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error ejecutando la actualización: " . $sentencia->error]);
                        }
                        break;

                    case 'gps':
                        $id_vaca_gps = $data->id_vaca_gps;
                        $Numero_pendiente = $data->Numero_pendiente;
                        $longitud = $data->longitud;
                        $latitud = $data->latitud;
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("UPDATE Pasto SET Numero_pendiente = ?, longitud = ?, latitud = ? WHERE id_vaca_gps = ?");
                        $sentencia->bind_param("iddi", $Numero_pendiente,$longitud,$latitud, $id_vaca_gps);
                        
                        // Ejecutar la sentencia
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0) {
                                echo json_encode(["mensaje" => "GPS actualizad correctamente"]);
                            } else {
                                echo json_encode(["mensaje" => "No se actualizó"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error ejecutando la actualización: " . $sentencia->error]);
                        }
                        break;
                     
                    default:
                        header("HTTP/1.1 404 Not Found");
                        exit();
                }

            }else{
                $datosCrudos = file_get_contents("php://input");
                $datos = json_decode($datosCrudos, true);
                $Numero_pendiente = $data->Numero_pendiente;
                $Fecha_nacimiento = $data->Fecha_nacimiento;
                $nota = $data->nota;

                $idNumeroPendienteMadre = isset($data->idNumeroPendienteMadre) ? $data->idNumeroPendienteMadre : null;
                // $idUsuarioMadre = isset($data->idUsuarioMadre) ? $data->idUsuarioMadre : null;
                // Preparar la sentencia SQL para actualizar la tabla
                
                $sentencia = $conexion->prepare("UPDATE Vaca SET idNumeroPendienteMadre = ?, idUsuarioMadre = ?, nota = ?, Fecha_nacimiento = ? WHERE Numero_pendiente = ? AND IdUsuario = ?");

                // Vincular los parámetros a la sentencia preparada
                $sentencia->bind_param("iissii",$idNumeroPendienteMadre, $IdUsuario , $nota, $Fecha_nacimiento, $Numero_pendiente, $IdUsuario);
                if ($sentencia->execute()) {
                    if ($sentencia->affected_rows > 0) {
                        echo json_encode(["mensaje" => "Vaca actualizada correctamente"]);
                    } else {
                        echo json_encode(["mensaje" => "No se actualizó"]);
                    }
                } else {
                    echo json_encode(["mensaje" => "Error ejecutando la actualización: " . $sentencia->error]);
                }
            }
        }
        break;

    case 'POST':
        if($uri[1]=='parcelas'){
            $nombreParcela = $data->nombre_parcela;
            // Insertar la información de la parcela en la tabla 'parcela'
            $sentencia = $conexion->prepare("INSERT INTO parcela (IdUsuario,nombre_parcela) VALUES (?, ?)");
            $sentencia->bind_param("is", $IdUsuario,$nombreParcela);
            $sentencia->execute();
            
            // Obtener el id_parcela recién insertado
            echo $nombreParcela;
            $idParcela = $sentencia->insert_id;
            
            // Insertar las coordenadas en la tabla 'coordenadas'
            $coordenadas = $data->coordenadas;
            
            foreach ($coordenadas as $coordenada) {
                $latitud = $coordenada->latitude;
                $longitud = $coordenada->longitude;
                
                $sentenciaCoordenadas = $conexion->prepare("INSERT INTO coordenadas (id_parcela, latitude, longitude) VALUES (?,?,?)");
                $sentenciaCoordenadas->bind_param("idd", $idParcela, $latitud, $longitud);
                $sentenciaCoordenadas->execute();
            }
            
            // Verificar si la inserción fue exitosa
            if ($sentencia->affected_rows > 0) {
                echo json_encode(["mensaje" => "Parcela y coordenadas insertadas correctamente"]);
            } else {
                echo json_encode(["mensaje" => "Error al insertar parcela y coordenadas"]);
            }
            
        }elseif($uri[1] == 'login'){
            include 'user_login.php';
            
        }elseif($uri[1] =='usuarios'){
            $nuevoCorreo = $data->correo;
            $nuevaContraseña = $data->usu_password;
            $nuevoNombre = $data->nombre; 
            $nuevosApellidos = $data->apellidos;
            
            // Las contraseñas coinciden
            $sentencia = $conexion->prepare("INSERT INTO usuario (correo,usu_password, nombre, apellidos) VALUES (?,?,?,?)");
            $sentencia->bind_param("ssss", $nuevoCorreo, $nuevaContraseña, $nuevoNombre, $nuevosApellidos);
            
            // Ejecutar la sentencia
            $sentencia->execute();
            
            // Después de ejecutar la sentencia
            if ($conexion->affected_rows > 0) {
                $idNuevoUsuario = $conexion->insert_id; // Obtener el ID del nuevo usuario
                echo json_encode([
                    "mensaje" => "Usuario creado con éxito",
                    "id" => $idNuevoUsuario,
                    "sesion_id" => session_id()]);
            } else {
                echo json_encode(["mensaje" => "Error al insertar usuario"]);
            }

        }elseif($uri[1] =='vacas'){
            if(isset($uri[2])){
                switch ($uri[2]) {
                    case 'enfermedades':
                        // Asumiendo que ya has validado y saneado las entradas antes de este punto
                        $Numero_pendiente = $data->Numero_pendiente;
                        $Medicamento = $data->Medicamento;
                        $Enfermedad = $data->Enfermedad;
                        $fecha_inicio = $data->fecha_inicio;
                        $fecha_fin = $data->fecha_fin;
                        $PeriocidadEnDias = $data->periocidad_en_dias;
                        $nota = $data->nota;

                        // Preparar la sentencia SQL
                        $sentencia = $conexion->prepare("INSERT INTO Enfermedades (Numero_pendiente, IdUsuario, Medicamento, Enfermedad, fecha_inicio, fecha_fin, nota, periocidad_en_dias) VALUES (?, ?, ?, ?, ?, ?, ?,?)");
                        $sentencia->bind_param("iisssssi", $Numero_pendiente, $IdUsuario, $Medicamento, $Enfermedad, $fecha_inicio, $fecha_fin, $nota, $PeriocidadEnDias);

                        // Ejecutar la sentencia
                        if ($sentencia->execute()) {
                            // Verificar si se insertó la enfermedad
                            if ($sentencia->affected_rows > 0) {
                                
                                $resultadoEnfermedades = $sentencia->get_result();
                                
                                $jsonEnfermedad = [];

                                $idNuevaEnfermedad = $conexion->insert_id; // Obtener el ID del nuevo parto
                                $consulta = $conexion->prepare("SELECT * FROM Enfermedades WHERE id_enfermedad_vaca = ?");
                                $consulta->bind_param("i", $idNuevaEnfermedad);
                                $consulta->execute();
                                $resultado = $consulta->get_result();
                                $enfermedad = []; // Corregido: Inicializar el array correctamente
                                if ($fila = $resultado->fetch_assoc()) {
                                    // Devolver los datos como JSON
                                    $enfermedad = $fila;
                                }
                                $enfermedad["mensaje"] = "Enfermedad insertada con éxito";
                                echo json_encode($enfermedad);

                            } else {
                                echo json_encode(["mensaje" => "No se pudo insertar la enfermedad"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error al ejecutar la sentencia"]);
                        }
                        $sentencia->close();
                        break;
                    
                        
                    case 'fechas_parto':
                        
                        $Numero_pendiente = $data->Numero_pendiente;
                        $fecha_parto = $data->fecha_parto;
                        $nota = $data->nota;
                    
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("INSERT INTO Partos(Numero_pendiente,IdUsuario, fecha_parto, nota) VALUES(?,?,?,?)");
                        $sentencia->bind_param("iiss", $Numero_pendiente,$IdUsuario,$fecha_parto, $nota);
                        
                        // Ejecutar la sentencia
                        $sentencia->execute();
        
                        // Después de ejecutar la sentencia
                        if ($conexion->affected_rows > 0) {
                            $idNuevoParto = $conexion->insert_id; // Obtener el ID del nuevo parto
        
                            // Realizar una nueva consulta para obtener la fila completa basada en el ID insertado
                            $consulta = $conexion->prepare("SELECT * FROM Partos WHERE id_vaca_parto = ?");
                            $consulta->bind_param("i", $idNuevoParto);
                            $consulta->execute();
                            $resultado = $consulta->get_result();
                            
                            $parto = []; // Corregido: Inicializar el array correctamente
                            if ($fila = $resultado->fetch_assoc()) {
                                // Devolver los datos como JSON
                                $parto = $fila;
                            }
                            $parto['mensaje'] = "Parto añadido con éxito";
                            echo json_encode($parto);
                        } else{
                            echo json_encode(["mensaje" => "No se pudo insertar el parto"]);
                        }
                        break;
                        
                    case 'volumen_leche':
                        
                        $Numero_pendiente = $data->Numero_pendiente;
                        $litros =$data->litros;
                        $fecha_recogida = $data->fecha_recogida;
                    
                    
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("INSERT INTO Leite ( Numero_pendiente, litros,IdUsuario,fecha_recogida) VALUES(?,?,?,?)");
                        $sentencia->bind_param("ids", $Numero_pendiente,$litros,$IdUsuario,$fecha_recogida);
                        
                        // Ejecutar la sentencia
                        $sentencia->execute();

                        // Después de ejecutar la sentencia
                        if ($conexion->affected_rows > 0) {
                            $idNuevoUsuario = $conexion->insert_id; // Obtener el ID del nuevo usuario
                            echo json_encode(["mensaje" => "Usuario insertado con éxito", "id" => $idNuevoUsuario]);
                        } else {
                            echo json_encode(["mensaje" => "Error al insertar usuario"]);
                        }
                        break;
                        
                    case 'dias_pasto':
                        
                        $Numero_pendiente = $$data->Numero_pendiente;
                        $dias_de_pasto =$data->dias_de_pasto;
                        $mes_de_pastore =$data->mes_de_pastore;
                        
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("INSERT INTO Pasto  (Numero_pendiente, dias_de_pasto,IdUsuario,mes_de_pastore)  VALUES(?,?,?,?)");
                        $sentencia->bind_param("iss", $Numero_pendiente,$dias_de_pasto,$IdUsuario,$mes_de_pastore);
                        
                        // Ejecutar la sentencia
                        $sentencia->execute();
                        
                        // Después de ejecutar la sentencia
                        if ($conexion->affected_rows > 0) {
                            $idNuevoUsuario = $conexion->insert_id; // Obtener el ID del nuevo usuario
                            echo json_encode(["mensaje" => "Usuario insertado con éxito", "id" => $idNuevoUsuario]);
                        } else {
                            echo json_encode(["mensaje" => "Error al insertar usuario"]);
                        }
                        break;
                    case 'gps':
                    
                        $Numero_pendiente = $$data->Numero_pendiente;
                        $longitud =$data->longitud;
                        $latitud =$data->latitud;
                        $fecha =$data->fecha;
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("INSERT INTO gps  (Numero_pendiente,IdUsuario,longitud,latitud)  VALUES(?,?,?,?)");
                        $sentencia->bind_param("iidd", $Numero_pendiente,$IdUsuario,$longitud,$latitud);
                        
                        // Ejecutar la sentencia
                        $sentencia->execute();
                        
                        // Después de ejecutar la sentencia
                        if ($conexion->affected_rows > 0) {
                            $idNuevoUsuario = $conexion->insert_id; // Obtener el ID del nuevo usuario
                            echo json_encode(["mensaje" => "gps insertado con éxito", "id" => $idNuevoUsuario]);
                        } else {
                            echo json_encode(["mensaje" => "Error al insertar gps"]);
                        }
                        break;
                    case 'puerta':
                
                        $hora_apertura = $data->hora_apertura;
                        $hora_cierre =$data->hora_cierre;
                        // Las contraseñas coinciden
                        $sentencia = $conexion->prepare("INSERT INTO puerta (IdUsuario,hora_apertura,hora_cierre)  VALUES(?,?,?)");
                        $sentencia->bind_param("iss",$IdUsuario,$hora_apertura,$hora_cierre);
                        
                        // Ejecutar la sentencia
                        $sentencia->execute();
                        
                        // Después de ejecutar la sentencia
                        if ($conexion->affected_rows > 0) {
                            $idNuevoUsuario = $conexion->insert_id; // Obtener el ID del nuevo usuario
                            echo json_encode(["mensaje" => "puerta insertado con éxito", "id" => $idNuevoUsuario]);
                        } else {
                            echo json_encode(["mensaje" => "Error al insertar puerta"]);
                        }
                        break;
                    default:
                        header("HTTP/1.1 404 Not Found");
                        exit();
                }
            }else{
                $Numero_pendiente =  $data->Numero_pendiente;
                $Fecha_Nacimiento =  $data->Fecha_nacimiento;
                
                // Las contraseñas coinciden
                $sentencia = $conexion->prepare("INSERT INTO Vaca( Numero_pendiente,IdUsuario,Fecha_nacimiento)  VALUES(?,?)");
                $sentencia->bind_param("sii",$Numero_pendiente,$IdUsuario,$Fecha_Nacimiento);

                // Ejecutar la sentencia
                $sentencia->execute();

                // Después de ejecutar la sentencia
                if ($conexion->affected_rows > 0) {
                    $idNuevoUsuario = $conexion->insert_id; // Obtener el ID del nuevo usuario
                    echo json_encode(["mensaje" => "Usuario insertado con éxito", "id" => $idNuevoUsuario]);
                } else {
                    echo json_encode(["mensaje" => "Error al insertar usuario"]);
                }
            }
        // Prueba Mail:
        }elseif($uri[1] =='contacto'){
            require("envioMails.php");

            $asunto =  $_POST["asunto"];
            $cuerpo = $_POST["cuerpo"];
            $cuerpo = $_POST["usuario"];

            echo json_encode(["asunto"  => $asunto,
            "cuerpo"  => $cuerpo,
            "usuario" => $IdUsuario]);
            
            $sentencia = $conexion->prepare("SELECT correo FROM usuario 
                                             WHERE id = ?");
            $sentencia->bind_param('i',$IdUsuario);
            
            // Ejecutar la sentencia
            $sentencia->execute();
            
            // Obtener el resultado
            $resultado = $sentencia->get_result();
            $fila = $resultado->fetch_assoc();
            
            $email = $fila['correo'];
            sendMail($email, $asunto, $cuerpo);
            
        }elseif($uri[1] == 'llamada'){
 	        require("asterisk.php");
            call();
        }
        break;
        
    case 'DELETE':
        if($uri[1] == 'parcelas' and isset($uri[2]) ){

            // Obtener el ID de la parcela a eliminar
            $idParcela = $uri[2];

            // Iniciar una transacción para garantizar la consistencia de los datos
            $conexion->begin_transaction();

            // Eliminar las coordenadas asociadas a la parcela, esto igual no hace falta ya que en parcela tenemos on delete cascade
            $sentenciaEliminarCoordenadas = $conexion->prepare("DELETE FROM coordenadas WHERE id_parcela = ?");
            $sentenciaEliminarCoordenadas->bind_param("i", $idParcela);
            $sentenciaEliminarCoordenadas->execute();

            // Eliminar la parcela
            $sentenciaEliminarParcela = $conexion->prepare("DELETE FROM parcela WHERE id_parcela = ?");
            $sentenciaEliminarParcela->bind_param("i", $idParcela);
            $sentenciaEliminarParcela->execute();

            // Verificar si la parcela y las coordenadas asociadas fueron eliminadas correctamente
            if ($sentenciaEliminarParcela->affected_rows > 0) {
                // Confirmar la transacción si todo fue exitoso
                $conexion->commit();
                echo json_encode(["mensaje" => "Parcela y coordenadas eliminadas correctamente"]);
            } else {
                // Revertir la transacción si hubo un error
                $conexion->rollback();
                echo json_encode(["mensaje" => "Error al eliminar parcela y coordenadas"]);
            }

        }elseif($uri[1] =='vacas'){
            if(isset($uri[2])){
                switch ($uri[2]) {
                    case 'enfermedades':
                        // Preparar la sentencia SQL
                        $id_enfermedad_vaca = $uri[3];

                        $sentencia = $conexion->prepare("DELETE FROM Enfermedades WHERE id_enfermedad_vaca = ?");
                        $sentencia->bind_param("i", $id_enfermedad_vaca);

                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0){
                                echo json_encode(["mensaje" => "Enfermedad eliminada"]);
                            }else{
                                echo json_encode(["mensaje" => "No se ah podido eliminar la Enfermedad"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error al eliminar la Enfermedad"]);
                        }
                        // Cerrar la sentencia
                        $sentencia->close();
                        break;
                        
                    case 'fechas_parto':
                        // Preparar la sentencia SQL
                        $id_vaca_parto =  $uri[3];
                        $sentencia = $conexion->prepare("DELETE FROM Partos WHERE id_vaca_parto = ? ");
                        $sentencia->bind_param("i", $id_vaca_parto);

                        // Ejecutar y verificar el resultado
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0){
                                echo json_encode(["mensaje" => "Parto eliminado"]);
                            }else{
                                echo json_encode(["mensaje" => "No se ah podido eliminar el Parto"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error al eliminar el Parto"]);
                        }
                        // Cerrar la sentencia
                        $sentencia->close();
                        break;
                        
                    case 'volumen_leche':
                        // Preparar la sentencia SQL
                        $id_vaca_leite =  $uri[3];

                        $sentencia = $conexion->prepare("DELETE FROM Leite WHERE id_vaca_leite = ?");
                        $sentencia->bind_param("i", $id_vaca_leite);

                        // Ejecutar y verificar el resultado
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0){
                                echo json_encode(["mensaje" => "Leche eliminada"]);
                            }else{
                                echo json_encode(["mensaje" => "No se ah podido eliminar la Leche"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error al eliminar la Leche"]);
                        }
                        // Cerrar la sentencia
                        $sentencia->close();
                        break;
                            
                    case 'dias_pasto':
                        $id_vaca_pasto =  $uri[3];

                        $sentencia = $conexion->prepare("DELETE FROM Pasto WHERE  id_vaca_pasto = ?");
                        $sentencia->bind_param("i", $id_vaca_pasto);

                        // Ejecutar y verificar el resultado
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0){
                                echo json_encode(["mensaje" => "Pasto eliminado"]);
                            }else{
                                echo json_encode(["mensaje" => "No se ah podido eliminar el Pasto"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error al eliminar el Pasto"]);
                        }
                        // Cerrar la sentencia
                        $sentencia->close();
                        break;
                    case 'gps':
                        // Preparar la sentencia SQL
                        $id_vaca_gps =  $uri[3];

                        $sentencia = $conexion->prepare("DELETE FROM gps WHERE  id_vaca_gps = ?");
                        $sentencia->bind_param("i", $id_vaca_gps);

                        // Ejecutar y verificar el resultado
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0){
                                echo json_encode(["mensaje" => "GPS eliminado"]);
                            }else{
                                echo json_encode(["mensaje" => "No se ah podido eliminar el GPS"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error al eliminar el GPS"]);
                        }
                        // Cerrar la sentencia
                        $sentencia->close();
                        break;
                    case 'puerta':
                        // Preparar la sentencia SQL
                        $id_puerta =  $uri[3];

                        $sentencia = $conexion->prepare("DELETE FROM puerta WHERE  id_puerta = ?");
                        $sentencia->bind_param("i", $id_puerta);

                        // Ejecutar y verificar el resultado
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0){
                                echo json_encode(["mensaje" => "Puerta eliminada"]);
                            }else{
                                echo json_encode(["mensaje" => "No se ah podido eliminar la Puerta"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error al eliminar la Puerta"]);
                        }
                        // Cerrar la sentencia
                        $sentencia->close();
                        break;
                    
                    default:
                        $Numero_pendiente = $uri[2];
                        $sentencia = $conexion->prepare("DELETE FROM Vaca WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        $sentencia->bind_param("ii", $Numero_pendiente,$IdUsuario);
        
                        // Ejecutar y verificar el resultado
                        if ($sentencia->execute()) {
                            if ($sentencia->affected_rows > 0){
                                echo json_encode(["mensaje" => "Vaca eliminada"]);
                            }else{
                                echo json_encode(["mensaje" => "No se ah podido eliminar la vaca"]);
                            }
                        } else {
                            echo json_encode(["mensaje" => "Error al eliminar la vaca"]);
                        }
        
                        // Cerrar la sentencia
                        $sentencia->close();
                }
            }
        }
        break;
    default:
        header("HTTP/1.1 404 Not Found");
        exit();
}
