<?php
require_once('BD.php');

class amistades
{
    // Función para agregar una amistad
    static public function agregarAmistad($usuario_id1, $usuario_id2)
    {
        $estadoConsulta = true;
        $conexion = BD::conexionBD();

        // Verificar si ya existe la amistad
        if (!self::existeAmistad($usuario_id1, $usuario_id2)) {
            $sqlInsert = "INSERT INTO amistades (usuario_id1, usuario_id2) VALUES (?, ?)";
            $consulta = $conexion->prepare($sqlInsert);
            $consulta->bindParam(1, $usuario_id1);
            $consulta->bindParam(2, $usuario_id2);

            if (!$consulta->execute()) {
                $estadoConsulta = false;
            }
        } else {
            // La amistad ya existe
            $estadoConsulta = false;
        }

        return $estadoConsulta;
    }

    // Función para verificar si una amistad ya existe
    static public function existeAmistad($usuario_id1, $usuario_id2)
    {
        $sql = "SELECT * FROM amistades WHERE (usuario_id1 = ? AND usuario_id2 = ?) OR (usuario_id1 = ? AND usuario_id2 = ?)";
        $conexion = BD::conexionBD();
        $consulta = $conexion->prepare($sql);
        $consulta->bindParam(1, $usuario_id1);
        $consulta->bindParam(2, $usuario_id2);
        $consulta->bindParam(3, $usuario_id2);
        $consulta->bindParam(4, $usuario_id1);
        $consulta->execute();

        return $consulta->fetch(PDO::FETCH_ASSOC) !== false;
    }

    // Función para obtener todas las amistades de un usuario
    static public function obtenerAmistades($usuario_id)
    {
        $sql = "SELECT u.* FROM amistades a JOIN usuarios u ON u.id = a.usuario_id2 WHERE a.usuario_id1 = ?";
        $conexion = BD::conexionBD();
        $consulta = $conexion->prepare($sql);
        $consulta->bindParam(1, $usuario_id);
        $consulta->execute();

        return $consulta->fetchAll(PDO::FETCH_ASSOC);
    }

    // Función para eliminar una amistad
    static public function eliminarAmistad($usuario_id1, $usuario_id2)
    {
        $estadoConsulta = true;
        $conexion = BD::conexionBD();

        $sqlDelete = "DELETE FROM amistades WHERE (usuario_id1 = ? AND usuario_id2 = ?) OR (usuario_id1 = ? AND usuario_id2 = ?)";
        $consulta = $conexion->prepare($sqlDelete);
        $consulta->bindParam(1, $usuario_id1);
        $consulta->bindParam(2, $usuario_id2);
        $consulta->bindParam(3, $usuario_id2);
        $consulta->bindParam(4, $usuario_id1);

        if (!$consulta->execute()) {
            $estadoConsulta = false;
        }

        return $estadoConsulta;
    }
    // Función para obtener todas las amistades en la base de datos
    static public function obtenerTodasLasAmistades()
    {
        $sql = "SELECT a.usuario_id1, a.usuario_id2, 
                       u1.name AS nombre_usuario1, u1.lastname AS apellido_usuario1, 
                       u2.name AS nombre_usuario2, u2.lastname AS apellido_usuario2 
                FROM amistades a 
                JOIN usuarios u1 ON u1.id = a.usuario_id1 
                JOIN usuarios u2 ON u2.id = a.usuario_id2";
        $conexion = BD::conexionBD();
        $consulta = $conexion->prepare($sql);
        $consulta->execute();
    
        return $consulta->fetchAll(PDO::FETCH_ASSOC);
    }
    

}
?>
