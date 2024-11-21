<?php

session_start();
if (!isset($_SESSION['usuario'])) {
    header("location: ../contenido/login/login.php");
}
require_once('../../archivos/class/BD.php');
require_once('../../archivos/class/Usuarios.php');
require_once('../../archivos/class/Videojuegos.php');
$infoPerfil= $_POST['idUsuario'];

// variables de  datos de eidtarPerfil.php
$nombreAvatar=$_FILES['avatar']['name'];
$tipoAvatar=$_FILES['avatar']['type'];
$tamanioAvatar=$_FILES['avatar']['size'];
$nombrePerfil=$_POST['nombre'];
$apellidoPerfil=$_POST['apellido'];
$sexoPerfil=$_POST['sexo'];
$municipioPerfil=$_POST['municipio'];


$arrayNombreAvatar= explode(".", $nombreAvatar);
$nombreAvatarId=$infoPerfil.".".end($arrayNombreAvatar);

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

$nombre = filter_input(INPUT_POST,'nombre', FILTER_SANITIZE_STRING);
$apellido = filter_input(INPUT_POST,'apellido', FILTER_SANITIZE_STRING);
$sexoPerfil = filter_input(INPUT_POST,'sexo', FILTER_SANITIZE_STRING);
$municipioPerfil = filter_input(INPUT_POST,'municipio', FILTER_SANITIZE_STRING);

$idJuegosUsuario =   Usuarios::selectPerfil($_SESSION["usuario"]);
$idJuegoUsuario = $idJuegosUsuario->fetch(PDO::FETCH_ASSOC);

//echo $infoPerfil;

//Actualizar foto 



    $estadoConsulta =  Usuarios::actualizarPerfil($nombre,$apellido,$sexoPerfil, $nombreAvatarId, $municipioPerfil,$infoPerfil);
   
  
echo $nombre, $apellido, $sexoPerfil, $nombreAvatarId, $municipioPerfil, $infoPerfil;

/* 
 $ruta="http://local.repositygames/contenido/usuarios/perfil.php";
if($estadoConsulta==true){
    $url=$ruta. "?alerta=ok";
}else{
    $url=$ruta. "?alerta=error";
}
 
header("Location: ".$url);
*/