<?php
$hostname='localhost';
$database='muundoGando';
$username='root';
$password='LPRO_2024';

$conexion=new mysqli($hostname,$username,$password,$database);

if($conexion->connect_errno){
    echo "El sitio web está experimentado problemas";
}
?>
