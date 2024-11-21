<?php


require_once('../include/Usuarios.php');

if (isset($_POST['enviar'])) {

    if (empty($_POST['nombre']) || empty($_POST['password'])|| empty($_POST['municipio'])|| empty($_POST['apellidos'])) {
      echo   $error = "Debes introducir un nombre de usuario y una contraseña";
     } else {
        // Comprobamos las credenciales con la base de datos
        $nombre=$_POST['nombre'];
        $contrasenia=$_POST['password'];
        $municipio=$_POST['municipio'];
        $apellidos=$_POST['apellidos'];
        $apodo=$_POST['apodo'];
        $fecha_creacion = date("Y-m-d");
       usuarios::registrarUsuario($nombre, $apellidos, $contrasenia, $municipio, $apodo, $fecha_creacion );
        
         
        
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
  <link href="../Css/Css1.css" rel="stylesheet" type="text/css">
</head>

<body>
    <div id='sign_in'>
    <form action='sign_in.php' method='post'>
    <fieldset >
        <legend>Login</legend>
        <div class='campo'>
            <label for='nombre' >Nombre:</label><br/>
            <input type='text' name='nombre' id='nombre' maxlength="50" /><br/>
        </div>
        <div class='campo'>
            <label for='apellidos' >Apellidos:</label><br/>
            <input type='text' name='apellidos' id='apellidos' maxlength="50" /><br/>
        </div>

        <div class='campo'>
            <label for='municipio' >Municipio:</label><br/>
            <input type='text' name='municipio' id='municipio' maxlength="50" /><br/>
        </div>
        <div class='campo'>
            <label for='apodo' >apodo:</label><br/>
            <input type='text' name='apodo' id='apodo' maxlength="50" /><br/>
        </div>
        <div class='campo'>
            <label for='password' >Contraseña:</label><br/>
            <input type='text' name='password' id='password' maxlength="50" /><br/>
        </div>
        

        <div class='campo'>
            <input type='submit' name='enviar' value='Enviar' />
        </div>
    </fieldset>
    </form>
   
    </div>
</body>
<?php
require_once("../footer/footer.php")
?>
</html>

