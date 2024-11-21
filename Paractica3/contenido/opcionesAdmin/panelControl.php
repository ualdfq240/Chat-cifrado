<?php
session_start();
if (!isset($_SESSION['usuario'])) {
    header("location: ../contenido/login/login.php");
}




if (!isset($_SESSION['usuario'])) {
    header("location: contenido/login/login.php");
}
require_once('../../archivos/class/Usuarios.php');
require_once('../../archivos/class/Publicaciones.php');
require_once('../../archivos/class/Videojuegos.php');
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Opciones Admin</title>
    <link id="template-file" href="icono/icono.html" rel="import" />
    <link href="../../../archivos/css/Css1.css" rel="stylesheet" type="text/css">
    <link href="../../../archivos/css/bootstrap.min.css" rel="stylesheet">
</head>


<body>
    <?php
    // Panel de control 
    require_once("../../contenido/header/header.php")
    ?>
     <div id="indexOpcionesAdmin">
    <div id="menuPerfil2" border="2" class="card">
        <?php
        $infoTotalPerfil =  Usuarios::selectPerfil($_SESSION["usuario"]);

        $infoPerfil = $infoTotalPerfil->fetch(PDO::FETCH_ASSOC);

        //var_dump( $infoPerfil)
        ?>


        <img class="avatar" src="../../archivos/img/perfil/<?php echo  $infoPerfil["ruta_foto"] . "?" . time(); ?>" width="10%">

        <p> Nombre: <?php echo  $infoPerfil["nombre"] ?> <?php echo  $infoPerfil["apellidos"] ?></p>
        <P>Nike : <?php echo  $infoPerfil["apodo"] ?></P>
        <P> Sexo: <?php echo  $infoPerfil["Sexo"] ?> </P>
        <p> Municipio: <?php echo  $infoPerfil["municipio"] ?></p>

        <form>
            <a href="editarUsarios.php" class="btn btn-primary"> Editar Usuarios</a>
        </form>

    </div>

     </div>

    <?php
    require_once("../../contenido/footer/footer.php")
    ?>
    <script src="/../../archivos//js//bootstrap.bundle.min.js"></script>

</body>


</html>