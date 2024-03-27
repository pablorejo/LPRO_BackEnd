<?php
//Import PHPMailer classes into the global namespace
//These must be at the top of your script, not inside a function
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

require 'PHPMailer/Exception.php';
require 'PHPMailer/PHPMailer.php';
require 'PHPMailer/SMTP.php';

require 'configMail.php';


function sendMail($email, $subject, $message){
    echo json_encode(["mensaje" => "Dentro función 1"]);

    //Create an instance; passing `true` enables exceptions
    $mail = new PHPMailer(true);

    echo json_encode(["mensaje" => "Dentro función"]);

    try{
        //Server settings
        $mail->isSMTP();                                            //Send using SMTP
        $mail->SMTPAuth   = true;                                   //Enable SMTP authentication
        $mail->Host       = MAILHOST;                               //Set the SMTP server to send through
        $mail->Username   = USERMAIL;                               //SMTP username
        $mail->Password   = PASSWORD;                               //SMTP password
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTTLS;        //Enable implicit TLS encryption
        $mail->Port       = 587;                                    //TCP port to connect to; use 587 if you have set `SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS`

        //Recipients
        $mail->setFrom(SEND_FROM, SEND_FROM_NAME);
        $mail->addAddress($email);                                  
        $mail->addReplyTo(REPLAY_TO, REPLAY_TO_NAME); 
        
        //Content
        $mail->isHTML(true);                                        //Set email format to HTML
        $mail->Subject = $subject;
        $mail->Body    = $message;
        $mail->AltBody = $message;

        // Send Mail
        $mail->send();
        echo 'Mail enviado correctamente';
    }catch (Exception $e) {
        echo "El Mail no pudo ser enviado. Mail ERROR: {$mail->ErrorInfo}";
    }
}
