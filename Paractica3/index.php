<?php
session_start();
if (!isset($_SESSION['usuario'])) {
    header("location: login/login.php");
}
//Controladores
require_once('archivos/class/Usuarios.php');
require_once('archivos/class/Amistades.php');
require_once('archivos/class/Chat.php');

$userName = $_SESSION['usuario']; // Asume que el ID del usuario se guarda en la sesión


?>
<!DOCTYPE html>
<html lang="en">
<head>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CriptoChat</title>
    <link id="template-file" href="icono/icono.html" rel="import" />
  <

</head>
<body>
    
<?php
    // Header y contenido de index 
    require_once("contenido/header/header.php");
    ?>
<?php
// Suponiendo que el ID del usuario está almacenado en una variable
$idUsuario = usuarios::obtenerIdUsuario($userName);
$amistades = amistades::obtenerAmistades($idUsuario["id"]);

?>

<div class="amistades-container">
    <h2>Amistades de Usuario <?php echo htmlspecialchars($userName); ?></h2>
    <?php if (!empty($amistades)): ?>
        <ul>
            <?php foreach ($amistades as $amistad): ?>
                <li>
                    <?php echo htmlspecialchars($amistad['name'] . " " . $amistad['lastname']); ?>
                    <!-- Botón para ir al chat -->
                    <a href="chat/chat.php?amistadId=<?php echo $amistad['id']; ?>" class="btn-chat">Ir al chat</a>
                </li>
            <?php endforeach; ?>
        </ul>
    <?php else: ?>
        <p>Este usuario no tiene amistades.</p>
    <?php endif; ?>
</div>


<?php
    // footer
    require_once("contenido/footer/footer.php")
    ?>
    <script src="../archivos/js/bootstrap.bundle.min.js"></script>
    <script src="../archivos/js/jquery-3.6.0.min.js"></script>
    <script src="../archivos/js/jquery1.js"></script>

</body>

</html>