<?php
require_once('BD.php');

class Usuarios
{
    protected $id;           // ID Primaria
    protected $password;     // Contraseña
    protected $username;     // Nombre de usuario
    protected $name;         // Nombre
    protected $lastname;     // Apellidos

    public function __construct($username, $password, $name, $lastname)
    {
        $this->username = $username;
        $this->password = $password;
        $this->name = $name;
        $this->lastname = $lastname;
    }

    // Función para registrar un usuario
    static public function registrarUsuario($username, $password, $name, $lastname)
    {
        $estadoConsulta = true;
        $conexion = BD::conexionBD();

        // Verificar si ya existe el usuario
        if (!self::selectUsuario($username)) {
            $sqlInsert = "INSERT INTO usuarios (username, password, name, lastname) VALUES (?, ?, ?, ?)";
            $consulta = $conexion->prepare($sqlInsert);
            $consulta->bindParam(1, $username);
            $consulta->bindParam(2, $password);
            $consulta->bindParam(3, $name);
            $consulta->bindParam(4, $lastname);

            if (!$consulta->execute()) {
                $estadoConsulta = false;
            }
        } else {
            // El usuario ya existe
            $estadoConsulta = false;
        }

        return $estadoConsulta;
    }

    // Función para verificar si un usuario ya existe
    static public function selectUsuario($username)
    {
        $sql = "SELECT * FROM usuarios WHERE username = ?";
        $conexion = BD::conexionBD();
        $consulta = $conexion->prepare($sql);
        $consulta->bindParam(1, $username);
        $consulta->execute();

        return $consulta->fetch(PDO::FETCH_ASSOC) !== false;
    }

    // Función para obtener los datos de un usuario
    static public function obtenerUsuario($id)
    {
        $sql = "SELECT * FROM usuarios WHERE id = ?";
        $conexion = BD::conexionBD();
        $consulta = $conexion->prepare($sql);
        $consulta->bindParam(1, $id);
        $consulta->execute();

        return $consulta->fetch(PDO::FETCH_ASSOC);
    }
    // Función para obtener Id de un usuario
    static public function obtenerIdUsuario($username)
    {
        $sql = "SELECT * FROM usuarios WHERE username = ?";
        $conexion = BD::conexionBD();
        $consulta = $conexion->prepare($sql);
        $consulta->bindParam(1, $username);
        $consulta->execute();

        return $consulta->fetch(PDO::FETCH_ASSOC);
    }

    // Función para actualizar el perfil de un usuario
    static public function actualizarPerfil($id, $username, $password, $name, $lastname)
    {
        $estadoConsulta = true;
        $conexion = BD::conexionBD();

        $sqlUpdate = "UPDATE usuarios SET username = ?, password = ?, name = ?, lastname = ? WHERE id = ?";
        $consulta = $conexion->prepare($sqlUpdate);
        $consulta->bindParam(1, $username);
        $consulta->bindParam(2, $password);
        $consulta->bindParam(3, $name);
        $consulta->bindParam(4, $lastname);
        $consulta->bindParam(5, $id);

        if (!$consulta->execute()) {
            $estadoConsulta = false;
        }

        return $estadoConsulta;
    }
}
?>
