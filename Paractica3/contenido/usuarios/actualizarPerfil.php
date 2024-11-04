<?php

session_start();
if (!isset($_SESSION['usuario'])) {
    header("location: ../contenido/login/login.php");
}
require_once('../../archivos/class/BD.php');
require_once('../../archivos/class/Usuarios.php');
require_once('../../archivos/class/Videojuegos.php');
$infoTotalPerfil =  Usuarios::selectPerfil($_SESSION["usuario"]);
$infoPerfil = $infoTotalPerfil->fetch(PDO::FETCH_ASSOC);

// variables de  datos de eidtarPerfil.php
$nombreAvatar=$_FILES['avatar']['name'];
$tipoAvatar=$_FILES['avatar']['type'];
$tamanioAvatar=$_FILES['avatar']['size'];




$municipioPerfil=$_POST['municipio'];

$arrayNombreAvatar= explode(".", $nombreAvatar);
$nombreAvatarId=$infoPerfil["id"].".".end($arrayNombreAvatar);

/* echo "nombre: ".$nombreAvatar."</br>";
echo   "tipo: ".$tipoAvatar."</br>";
echo  "tamaño: ".$tamanioAvatar."</br>";
echo   "id: ". $infoPerfil['id']."<br>";
echo   "nombre imagen: ". $nombreAvatarId. "<br>";
 */

$rutaAvatar=$_SERVER['DOCUMENT_ROOT']. '/archivos/img/perfil/';
echo "Ruta: ".$rutaAvatar;

move_uploaded_file($_FILES['avatar']['tmp_name'], $rutaAvatar.$nombreAvatarId);
//optener videojuegos usuario
$idJuegosUsuario =   Usuarios::selectPerfil($_SESSION["usuario"]);
$idJuegoUsuario = $idJuegosUsuario->fetch(PDO::FETCH_ASSOC);

echo $idJuegoUsuario["id"];


$nombre = filter_input(INPUT_POST,'nombre', FILTER_SANITIZE_STRING);
$apellido = filter_input(INPUT_POST,'apellido', FILTER_SANITIZE_STRING);
$sexoPerfil = filter_input(INPUT_POST,'sexo', FILTER_SANITIZE_STRING);
$municipioPerfil = filter_input(INPUT_POST,'municipio', FILTER_SANITIZE_STRING);




    $estadoConsulta =  Usuarios::actualizarPerfil($nombre,$apellido,$sexoPerfil, $nombreAvatarId, $municipioPerfil,$infoPerfil['id']);
    

//Actualizar perfil 




$ruta="http://local.repositygames/contenido/usuarios/perfil.php";
if($estadoConsulta==true){
    $url=$ruta. "?alerta=ok";
}else{
    $url=$ruta. "?alerta=error";
}

header("Location: ".$url);
 