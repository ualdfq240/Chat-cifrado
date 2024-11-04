<?php
session_start();
if (!isset($_SESSION['usuario'])) {
    header("location: ../contenido/login/login.php");
}


require_once('../../archivos/class/Usuarios.php');


?>
<!DOCTYPE html>
<html lang="en">
<?php
require_once("../../contenido/header/header.php");
echo  $idUsuario = $_GET['idUsuario'];
$infoTotalPerfil =  Usuarios::selectPerfil($idUsuario);



$infoPerfil = $infoTotalPerfil->fetch(PDO::FETCH_ASSOC);

?>
<!-- Forumlario editar perfil -->

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="../../archivos/css/Css1.css" rel="stylesheet" type="text/css">
    <link href="../../archivos//css/bootstrap.min.css" rel="stylesheet">
    <title>Editar perfil</title>
</head>

<body>
    <div id="indexOpcionesAdmin">
        <div class="card" name="menuPerfil" id="menuPerfil2">
            <form action="actualizarUsuario.php" method="POST" enctype="multipart/form-data" />

            <img class="avatar" src="../../archivos/img/perfil/<?php echo  $infoPerfil["ruta_foto"] . "?" . time(); ?>" width="10%">

            <div>Añadir imagen: <input name="avatar" id="avatar" type="file" /></div>

            <div> Nombre: <input type="text" id="nombre" name="nombre" placeholder=" <?php echo  $infoPerfil["nombre"] ?>"> </input></div>


            <div> Apellidos: <input type="text" id="apellido" name="apellido" placeholder=" <?php echo  $infoPerfil["apellidos"] ?>"> </input> </div>



            <div> Sexo: <input type="text" id="sexo" name="sexo" placeholder=" <?php echo  $infoPerfil["Sexo"] ?>"></div>

            <div> Municipio: <input type="text" id="municipio" name="municipio" placeholder=" <?php echo  $infoPerfil["municipio"] ?>"></div>
            <input type="hidden" id="idUsuario" name="idUsuario" value="<?php echo  $idUsuario ?>">


            <input type="submit" name="actualizar" value="Actualizar Perfil" class="btn btn-primary" />

            </form>
        </div>
    </div>
    <?php
    require_once("../../contenido/footer/footer.php")

    ?>
    <script src="/../../archivos/js//bootstrap.bundle.min.js"></script>

</body>

</html>