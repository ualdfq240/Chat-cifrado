<?php
require_once('../archivos/class/Amistades.php');
require_once('../archivos/class/BD.php');
require_once('../archivos/class/Chat.php');
require_once('../archivos/class/Usuarios.php');



// Obtener los IDs de los usuarios
session_start();
$idUser = Usuarios::obtenerIdUsuario($_SESSION['usuario']); // ID del usuario actual, almacenado en la sesión
$chatUserId = $_GET['amistadId']; // ID del amigo con quien se está chateando

// Obtener datos del usuario con quien se chatea
$chatUser = Usuarios::obtenerUsuario($chatUserId);
//$mensajes = Chat::obtenerMensajes($chatUser, $chatUserId);

// Enviar un mensaje si el formulario ha sido enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['contenido'])) {
    $contenido = htmlspecialchars($_POST['contenido']); // Filtra el contenido para evitar inyecciones de HTML
    Chat::enviarMensaje($currentUserId, $chatUserId, $contenido);
    header("Location: chat.php?userId=$chatUserId"); // Recarga la página para mostrar el nuevo mensaje
    exit;
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat con <?php echo htmlspecialchars($chatUser['name'] . ' ' . $chatUser['lastname']); ?></title>
    <link rel="stylesheet" href="styles.css"> <!-- Tu archivo de estilos -->
</head>
<body>
    <div class="chat-container">
        <h2>Chat con <?php echo htmlspecialchars($chatUser['name'] . ' ' . $chatUser['lastname']); ?></h2>
        
        <div class="messages">
            <?php if (!empty($mensajes)): ?>
                <?php foreach ($mensajes as $mensaje): ?>
                    <div class="message <?php echo $mensaje['from_user_id'] == $currentUserId ? 'sent' : 'received'; ?>">
                        <p><?php echo htmlspecialchars($mensaje['contenido']); ?></p>
                        <span class="timestamp"><?php echo htmlspecialchars($mensaje['fecha_envio']); ?></span>
                    </div>
                <?php endforeach; ?>
            <?php else: ?>
                <p class="no-messages">No hay mensajes aún. ¡Comienza la conversación!</p>
            <?php endif; ?>
        </div>

        <form method="POST" class="message-form">
            <input type="text" name="contenido" placeholder="Escribe tu mensaje..." required>
            <button type="submit">Enviar</button>
        </form>
    </div>
</body>
</html>
