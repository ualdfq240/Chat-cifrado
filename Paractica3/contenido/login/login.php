<?php
require_once('../../archivos/class/BD.php');

// Comprobamos si ya se ha enviado el formulario
$error = "";
if (isset($_POST['enviar'])) {
    // patrones 

    $contraseñaRegex = "(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$";
    // filtramos 

    $usuario = filter_input(INPUT_POST, 'usuario', FILTER_SANITIZE_STRING);
    $password = filter_input(INPUT_POST, 'password', FILTER_SANITIZE_STRING);

    if (empty($usuario) || empty($password)) {


        $error = "Debes introducir un nombre de usuario y una contraseña ";
    } else {
        // Comprobamos las credenciales con la base de datos
        if (BD::verificaCliente($_POST['usuario'], $_POST['password'])) {
            session_start();
            $_SESSION['usuario'] = $_POST['usuario'];
            header("Location: ../../index.php");
        } else {
            // Si las credenciales no son válidas, se vuelven a pedir
            $error = "Usuario o contraseña no válidos!";
        }
    }
}

if (isset($_POST['Registrarse'])) {
    header("Location: sign_in.php");
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

    <div id=login>
        <h1 id='titulo'>Reposity Games</h1>

        <form action='login.php' method='post'>
            <fieldset>
                <legend>Inicio sesión </legend>
                <div><span class='error'><?php echo $error; ?></span></div>

                <input type='text' name='usuario' placeholder="Usuario" class="form-control" id='usuario' maxlength="50" /><br />



                <input type='password' name='password' placeholder="Contraseña" class="form-control" id='password' maxlength="50" /><br />

                <div id='botones'>
                    <input type='submit' name='enviar' class="btn btn-primary" value='Enviar' />
                    <input type='submit' name='Registrarse' class="btn btn-primary" value='Registrarse' />
                </div>
            </fieldset>
        </form>
        <diiv id="textoLogin">
            <h3>Tu lugar para empezar a colecionar </h3>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Officia modi, dolor reiciendis ut fugiat nobis facere. Natus corrupti nihil esse corporis numquam provident! Atque officia id ipsum, reprehenderit aperiam fugiat.</p>
    </div>

    </div>


    <?php
    require_once('../footer/footer.php');
    ?>
    <script src="../../archivos//js//bootstrap.bundle.min.js"></script>


</body>

</html>