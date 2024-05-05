<?php
/*
Action: Login
Username: admin
Secret: muundoGando
Events: off

Action: Originate
Channel: PJSIP/100
Callerid: MuundoGando
Exten: 1
Context: muundogando
Variable: id_vaca=1
Priority: 1
*/

function call($numeroPendiente){
//    $oSocket = fsockopen("192.168.0.22", 5038, $errno, $errstr, $timeout);
$oSocket = fsockopen("172.20.10.9", 5038, $errno, $errstr, $timeout);

    if (!$oSocket) {
            echo "$errstr ($errno)<br>\n";
    } else {
        //echo json_encode(["mensaje" => "Antes login"]);
        fputs($oSocket, "Action: login\r\n");
        fputs($oSocket, "Username: admin\r\n");
        fputs($oSocket, "Secret: muundoGando\r\n\r\n");

        //echo json_encode(["mensaje" => "Antes originate"]);
        fputs($oSocket, "Action: originate\r\n");
        fputs($oSocket, "Channel: PJSIP/100\r\n");
        fputs($oSocket, "CallerId: MuundoGando\r\n");
        fputs($oSocket, "Exten: 1\r\n");
        fputs($oSocket, "Context: muundogando\r\n");
        fputs($oSocket, "Variable: id_vaca=$numeroPendiente\r\n");
        fputs($oSocket, "Priority: 1\r\n\r\n");

        fputs($oSocket, "Action: Logoff\r\n\r\n");
        sleep(2);
        fclose($oSocket);

        echo 'Llamada realizada con EXITO!';
    }
}
    
