<?php

use PhpParser\Node\Stmt\While_;

session_start();


require_once('../../archivos/class/Usuarios.php');
require_once('../../archivos/class/videojuegos.php');
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="../../archivos/css/Css1.css" rel="stylesheet" type="text/css">
    <link href="../../archivos//css/bootstrap.min.css" rel="stylesheet">
    <title>Document</title>

</head>


<body>
    <?php
    require_once("../header/header.php");

    if (!empty($_GET['alerta'])) {
        $alerta = $_GET['alerta'];
        if ($alerta == 'ok') {
            $mensaje = "Se introdujeron los campos correctamente";
            $colorAlerta = "alert-success";
        } else {
            $mensaje = "Error en los Campos";
            $colorAlerta = "alert-danger";
        }
    ?>
        <div class="alert <?php echo $colorAlerta; ?>" role="alert">
            <?php echo $mensaje; ?>
        </div>
    <?php

    }
    ?>
    <div id="indexPerfil">


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
                <a href="editarPerfil.php" class="btn btn-primary"> Editar</a>
            </form>

        </div>
    </div>



    <script src="/../archivos//js//bootstrap.bundle.min.js"></script>

</body>
<?php
require_once("../footer/footer.php")
?>

</html>

<?php


?>