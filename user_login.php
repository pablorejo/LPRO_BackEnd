<?php
    header("Content-Type: application/json");

    // Inicio una sesión de PHP
    session_start();

    // Verifico la variable 'user_id' no está establecida
    // if (!isset($_SESSION['user_id'])) {
        // Cojo los parámetros del usuario y la contraseña, si están varíos los pongo a null.
        $user = isset($_POST['usuario']) ? $_POST['usuario'] : null;
        $password = isset($_POST['password']) ? $_POST['password'] : null;
        
        if ($user && $password) {
            // Preparar la consulta SQL para seleccionar el usuario por ID
            $sentencia = $conexion->prepare("SELECT * FROM usuario WHERE correo = ?");
            $sentencia->bind_param('s', $user);

            // Ejecutar la sentencia
            $sentencia->execute();

            // Obtener el resultado
            $resultado = $sentencia->get_result();

            $fila = mysqli_fetch_assoc($resultado);
            
            // Variable $hash tiene la contraseña hasheada de la BD
            $hash = isset($fila['usu_password']) ? $fila['usu_password'] : '';
            /*
            password_Verify() verifica que la contraseña introducida por el usuario
            es la misma que la contraseña hasheada de la BD.
            */
            
            if (strcmp($password, $hash) == 0){

                $_SESSION['user_id'] = $fila['id'];
                $_SESSION['user_name'] = $fila['nombre'];
                $_SESSION['user_nickname'] = $fila['apellidos'];
                $_SESSION['user_email'] = $fila['correo'];
                $_SESSION['session_start'] = time();

                $IdUsuario = $fila['id'];

                // Suponiendo que ya tienes un $IdUsuario especificado
                $datos_usuario = [
                    'id' => $fila['id'],
                    'nombre' => $fila['nombre'],
                    'apellidos' => $fila['apellidos'],
                    'correo' => $fila['correo'],
                    "session_id" => session_id(),
                    "nota" => $fila['nota'],
                    "mensaje" => "Sesión inciada"
                ];

            
                if ($datos_usuario) {
                    $datos_usuario['vacas'] = [];
                    $sentencia = $conexion->prepare("SELECT * FROM Vaca WHERE IdUsuario = ?");
                    $sentencia->bind_param('i', $IdUsuario);
                    $sentencia->execute();
                    $resultadoVacas = $sentencia->get_result();
            
                    while ($vaca = $resultadoVacas->fetch_assoc()) {
                        $vaca['enfermedades'] = [];
                        $sentenciaEnfermedades = $conexion->prepare("SELECT * FROM Enfermedades WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        // Suponiendo que $vaca['Numero_pendiente'] existe y contiene el número de pendiente de la vaca
                        $sentenciaEnfermedades->bind_param('ii', $vaca['Numero_pendiente'], $IdUsuario);
                        $sentenciaEnfermedades->execute();
                        $resultadoEnfermedades = $sentenciaEnfermedades->get_result();
            
                        while ($enfermedad = $resultadoEnfermedades->fetch_assoc()) {
                            $vaca['enfermedades'][] = $enfermedad;
                        }
    
    
                        $vaca['leiteHistorico'] = [];
                        $sentenciaEnfermedades = $conexion->prepare("SELECT * FROM Leite WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        // Suponiendo que $vaca['Numero_pendiente'] existe y contiene el número de pendiente de la vaca
                        $sentenciaEnfermedades->bind_param('ii', $vaca['Numero_pendiente'], $IdUsuario);
                        $sentenciaEnfermedades->execute();
                        $resultadoEnfermedades = $sentenciaEnfermedades->get_result();
            
                        while ($enfermedad = $resultadoEnfermedades->fetch_assoc()) {
                            $vaca['leiteHistorico'][] = $enfermedad;
                        }
    
                        $vaca['partos'] = [];
                        $sentenciaEnfermedades = $conexion->prepare("SELECT * FROM Partos WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        // Suponiendo que $vaca['Numero_pendiente'] existe y contiene el número de pendiente de la vaca
                        $sentenciaEnfermedades->bind_param('ii', $vaca['Numero_pendiente'], $IdUsuario);
                        $sentenciaEnfermedades->execute();
                        $resultadoEnfermedades = $sentenciaEnfermedades->get_result();
            
                        while ($enfermedad = $resultadoEnfermedades->fetch_assoc()) {
                            $vaca['partos'][] = $enfermedad;
                        }
                        
                        // $vaca['datosGps'] = [];
                        // $sentenciaEnfermedades = $conexion->prepare("SELECT * FROM gps WHERE Numero_pendiente = ? AND IdUsuario = ?");
                        // // Suponiendo que $vaca['Numero_pendiente'] existe y contiene el número de pendiente de la vaca
                        // $sentenciaEnfermedades->bind_param('ii', $vaca['Numero_pendiente'], $IdUsuario);
                        // $sentenciaEnfermedades->execute();
                        // $resultadoEnfermedades = $sentenciaEnfermedades->get_result();
            
                        // while ($enfermedad = $resultadoEnfermedades->fetch_assoc()) {
                        //     $vaca['datosGps'][] = $enfermedad;
                        // }
                        
                        
                        // Repetir para partos, leiteHistorico, etc.
                        $datos_usuario['vacas'][] = $vaca;
                    }

                    $datos_usuario['parcelas'] = [];
                    $sentenciaEnfermedades = $conexion->prepare("SELECT * FROM parcela WHERE IdUsuario = ?");
                    // Suponiendo que $vaca['Numero_pendiente'] existe y contiene el número de pendiente de la vaca
                    $sentenciaEnfermedades->bind_param('i', $IdUsuario);
                    $sentenciaEnfermedades->execute();
                    $resultadoEnfermedades = $sentenciaEnfermedades->get_result();


                    while ($parcela = $resultadoEnfermedades->fetch_assoc()) {
                        $parcela['coordenadas'] = [];

                        $sentenciaCoordenadas = $conexion->prepare("SELECT * FROM coordenadas WHERE id_parcela = ?");
                        // Suponiendo que $vaca['Numero_pendiente'] existe y contiene el número de pendiente de la vaca
                        $sentenciaCoordenadas->bind_param('i', $parcela['id_parcela']);
                        $sentenciaCoordenadas->execute();
                        $resultadoCoordenadas = $sentenciaCoordenadas->get_result();

                        while ($coordenada = $resultadoCoordenadas->fetch_assoc()) {
                            $parcela['coordenadas'][] = $coordenada;
                        }
                        
                        $parcela['sector'];
                        $sentenciaCoordenadas = $conexion->prepare("SELECT * FROM sector WHERE id_parcela = ?");
                        // Suponiendo que $vaca['Numero_pendiente'] existe y contiene el número de pendiente de la vaca
                        $sentenciaCoordenadas->bind_param('i', $parcela['id_parcela']);
                        $sentenciaCoordenadas->execute();
                        $resultadoCoordenadas = $sentenciaCoordenadas->get_result();

                        while ($sector = $resultadoCoordenadas->fetch_assoc()) {

                            $sector['coordenadasSector'] = [];
                            $sentenciaCoordenadas = $conexion->prepare("SELECT * FROM coordenadas_sector WHERE id_sector = ?");
                            // Suponiendo que $vaca['Numero_pendiente'] existe y contiene el número de pendiente de la vaca
                            $sentenciaCoordenadas->bind_param('i', $sector['id_sector']);
                            $sentenciaCoordenadas->execute();
                            $resultadoCoordenadas = $sentenciaCoordenadas->get_result();

                            while ($coordenada = $resultadoCoordenadas->fetch_assoc()) {
                                $sector['coordenadasSector'][] = $coordenada;
                            }

                            $parcela['sector'] = $sector;
                        }

                        $datos_usuario['parcelas'][] = $parcela;
                    }
                }
            
                echo json_encode($datos_usuario ?: ["mensaje" => "ERROR"]);

            }else{
                echo json_encode(["mensaje" => "Algo ha salido mal"]);
            }
        }
    // }
?>