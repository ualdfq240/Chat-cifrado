<?php
require_once('../include/BD.php');

// Comprobamos si ya se ha enviado el formulario
$error="";
if (isset($_POST['enviar'])) {

    if (empty($_POST['usuario']) || empty($_POST['password'])) 
        $error = "Debes introducir un nombre de usuario y una contraseña";
    else {
        // Comprobamos las credenciales con la base de datos
        if (BD::verificaCliente($_POST['usuario'], $_POST['password'])) {
            session_start();
            $_SESSION['usuario']=$_POST['usuario'];
            header("Location: ../index.php");                    
        }
        else {
            // Si las credenciales no son válidas, se vuelven a pedir
            $error = "Usuario o contraseña no válidos!";
        }
    }
}

if (isset($_POST['Registrarse'])) {
    header("Location: ../sing_in/sign_in.php");        
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
  <link href="Css/Css1.css" rel="stylesheet" type="text/css">
</head>
</head>

<body>
    <div id='login'>
    <form action='login.php' method='post'>
    <fieldset >
        <legend>Login</legend>
        <div><span class='error'><?php echo $error; ?></span></div>
        <div class='campo'>
            <label for='usuario' >Usuario:</label><br/>
            <input type='text' name='usuario' id='usuario' maxlength="50" /><br/>
        </div>
        <div class='campo'>
            <label for='password' >Contraseña:</label><br/>
            <input type='password' name='password' id='password' maxlength="50" /><br/>
        </div>

        <div class='campo'>
            <input type='submit' name='enviar' value='Enviar' />
        </div>
        <div class='campo'>
    <input type='submit' name='Registrarse' value='Registrarse' />
        </div>
    </fieldset>
    </form>
   
    </div>
</body>
</html>

