<?php


require_once('../../archivos/class/Usuarios.php');

if (isset($_POST['enviar'])) {

    if (empty($_POST['nombre']) || empty($_POST['password']) || empty($_POST['municipio']) || empty($_POST['apellidos']) || empty($_POST['apodo'])) {
        $alerta = "Debes introducir un nombre de usuario y una contraseña";
    } else {
        // Comprobamos las credenciales con la base de datos

        $nombre = filter_input(INPUT_POST, 'nombre', FILTER_SANITIZE_STRING);
        $contrasenia = filter_input(INPUT_POST, 'password', FILTER_SANITIZE_STRING);
        $municipio = filter_input(INPUT_POST, 'municipio', FILTER_SANITIZE_STRING);
        $apellidos = filter_input(INPUT_POST, 'apellidos', FILTER_SANITIZE_STRING);;
        $apodo = filter_input(INPUT_POST, 'apodo', FILTER_SANITIZE_STRING);
        $sexo = filter_input(INPUT_POST, 'sexo', FILTER_SANITIZE_STRING);
        $fecha_creacion = date("Y-m-d");

        if (empty($nombre) || empty($contrasenia) || empty($municipio) || empty($apellidos) ||  empty($apodo) ||  empty($fecha_creacion)) {
        } else {
            usuarios::registrarUsuario($nombre, $apellidos, $contrasenia, $municipio, $apodo, $fecha_creacion, $sexo);
        }
    }
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- Desarrollo Web en Entorno Servidor -->
<!-- Tema 5 : Programación orientada a objetos en PHP -->
<!-- Ejemplo Tienda Web: login.php -->
<html>

<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>Game Repository</title>
    <link href="../../archivos/css/Css1.css" rel="stylesheet" type="text/css">
    <link href="../../archivos//css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
    <h1 id='titulo'>Reposity Games</h1>

    

    <div id='sign_in'>

        <form action='sign_in.php' method='post'>
            <fieldset>
                <legend>Login</legend>
                <div class='campo'>
                    <label for='nombre'>Nombre:</label><br />
                    <input class="form-control" type='text' name='nombre' id='nombre' maxlength="50" /><br />
                </div>
                <div class='campo'>
                    <label for='apellidos'>Apellidos:</label><br />
                    <input class="form-control" type='text' name='apellidos' id='apellidos' maxlength="50" /><br />
                </div>

                <div class='campo'>
                    <label for='municipio'>Municipio:</label><br />
                    <input class="form-control" type='text' name='municipio' id='municipio' maxlength="50" /><br />
                </div>
                <div class='campo'>
                    <label for='apodo'>apodo:</label><br />
                    <input class="form-control" type='text' name='apodo' id='apodo' maxlength="50" /><br />
                </div>
                <div class='campo'>
                    <label for='apodo'>sexo:</label><br />
                    <input class="form-control" type='text' name='sexo' id='apodo' maxlength="50" /><br />
                </div>
                <div class='campo'>
                    <label for='password'>Contraseña:</label><br />
                    <input class="form-control" type='text' name='password' id='password' maxlength="50" /><br />
                </div>


                <div class='campo'>
                    <input type='submit' class="btn btn-primary" name='enviar' value='Enviar' />
                </div>
            </fieldset>
        </form>

    </div>
    <?php
    require_once("../footer/footer.php")
    ?>
    <script src="../../archivos//js//bootstrap.bundle.min.js"></script>

</body>


</html>