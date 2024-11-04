<?php
require_once('BD.php'); // Incluye la conexión a la base de datos

class Chat
{
    // Atributos
    protected $id;
    protected $userId1;
    protected $userId2;
    protected $messages;

    // Constructor opcional para inicializar la clase
    public function __construct($userId1, $userId2)
    {
        $this->userId1 = $userId1;
        $this->userId2 = $userId2;
    }

    // Método para enviar un mensaje
    public static function enviarMensaje($fromUserId, $toUserId, $contenido)
    {
        $conexion = BD::conexionBD();
        $sqlInsert = "INSERT INTO mensajes (from_user_id, to_user_id, contenido, fecha_envio) VALUES (?, ?, ?, NOW())";
        $consulta = $conexion->prepare($sqlInsert);
        $consulta->bindParam(1, $fromUserId);
        $consulta->bindParam(2, $toUserId);
        $consulta->bindParam(3, $contenido);

        return $consulta->execute(); // Devuelve true si el mensaje se envió correctamente
    }

    // Método para obtener los mensajes de un chat específico
    public static function obtenerMensajes($userId1, $userId2)
    {
        $conexion = BD::conexionBD();
        $sql = "SELECT * FROM mensajes 
                WHERE (from_user_id = ? AND to_user_id = ?) 
                OR (from_user_id = ? AND to_user_id = ?)
                ORDER BY fecha_envio ASC";
        $consulta = $conexion->prepare($sql);
        $consulta->bindParam(1, $userId1);
        $consulta->bindParam(2, $userId2);
        $consulta->bindParam(3, $userId2);
        $consulta->bindParam(4, $userId1);
        $consulta->execute();

        return $consulta->fetchAll(PDO::FETCH_ASSOC); // Devuelve todos los mensajes en formato de arreglo
    }

    // Método para obtener la lista de chats de un usuario
    public static function obtenerChats($userId)
    {
        $conexion = BD::conexionBD();
        $sql = "SELECT DISTINCT 
                    CASE 
                        WHEN from_user_id = ? THEN to_user_id 
                        ELSE from_user_id 
                    END AS chat_user_id
                FROM mensajes
                WHERE from_user_id = ? OR to_user_id = ?";
        $consulta = $conexion->prepare($sql);
        $consulta->bindParam(1, $userId);
        $consulta->bindParam(2, $userId);
        $consulta->bindParam(3, $userId);
        $consulta->execute();

        return $consulta->fetchAll(PDO::FETCH_ASSOC); // Devuelve la lista de usuarios con los que ha tenido chats
    }
}
?>
