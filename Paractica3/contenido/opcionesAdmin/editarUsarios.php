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
    <title>Editar Usuarios</title>
    <link id="template-file" href="icono/icono.html" rel="import" />
    <link href="../../archivos/css/Css1.css" rel="stylesheet" type="text/css">
    <link href="../../archivos//css/bootstrap.min.css" rel="stylesheet">
</head>


<body>
    <?php
    require_once("../../archivos/class/Usuarios.php");
    require_once("../../contenido/header/header.php");


    $perfileSInfo = Usuarios::selectTodosPerfil();
    $perfileInfo = $perfileSInfo->fetch(PDO::FETCH_ASSOC);
    ?>

    <div id="indexOpcionesAdmin">
        <?php
        while ($perfileInfo != null) {
        ?>
            <!-- Muenu editar perfil -->

            <div class="card" name="menuPerfil" id="menuPerfil2">

                <p> @<?php echo $perfileInfo['apodo'] ?> </p>

                <form action="modificarFormularioUsuario.php?idUsuario" method="POST">
                    <a href="modificarFormularioUsuario.php?idUsuario=<?php echo $perfileInfo['apodo'] ?>" class="btn btn-primary"> Editar Usuario</a>

                </form>
            </div>

    

        <?php

            $perfileInfo = $perfileSInfo->fetch(PDO::FETCH_ASSOC);
        }
        ?>
        </div>
        <?php

        


        require_once("../../contenido/footer/footer.php")
        ?>
        <script src="/../../archivos//js//bootstrap.bundle.min.js"></script>

</body>


</html>