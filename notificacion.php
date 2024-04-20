<?php   
function notificacion($title, $message){
    // URL del servidor FCM:
    $urlSend = 'https://fcm.googleapis.com/fcm/send';

    // Token:
    $notificationId = "APA91bGqLdpBmh0c5cbdlbR6VfSx93Ov17s5ZY6m8XViJIIZYbPPxiuMVqsvRN2HeXsNkITNfihvZJf0If4Uf_lZCZbMZnKcmGM8rJF-wf4Jkt19WMOVXDE";

    // Clave del servidor FCM
    $server_key = 'AAAAvwb3TCE:APA91bH5ljrS5_Hzk1pvWpmpLMLYDaq1UPJ7ssnvtjHh5qZev7G2qc-5-H3cWZuxy2LYSuGRS_T_8M4dlHyawhzIXSbJQGkz3FZrp6ezhlrEv96qwotwd0pzU3mgDN9vgyIpG4c6W635';

    //$resultado = exec("python3 python/script.py");
    // Datos del mensaje:
    $message = [
        'to' => $notificationId,
        'data' => [
            'title' => $title,
            'message' => $message
        ]
    ];

    // Cabeceras de la petición HTTP
    $headers = [
        'Authorization: key=' . $server_key,
        'Content-Type: application/json'
    ];

    // Inicializar cURL
    $ch = curl_init();

    // Configurar opciones de cURL
    curl_setopt($ch, CURLOPT_URL, $urlSend);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($message));

    // Ejecutar la petición
    $response = curl_exec($ch);

    // Cerrar la conexión cURL
    curl_close($ch);

    // Procesar la respuesta
    if ($response === FALSE) {
        echo 'Error al enviar la notificación: ' . curl_error($ch);
    } else {
        echo 'Notificación enviada correctamente: ' . $response;
    }
}


?>