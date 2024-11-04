<?php
require_once('BD.php');
class usuarios
{
    protected $nombre;
    protected $apellidos;
    protected $contrasenia;
    protected $municipio;
    protected $fecha_creacion;
    protected $apodo;


    public function __construct($nombre, $apellidos, $contrasenia, $municipio, $fecha_creacion)
    {
        $this->nombre = $nombre;
        $this->apellidos = $apellidos;
        $this->contrasenia = $contrasenia;
        $this->municipio = $municipio;
        $this->fecha_creacion = $fecha_creacion;
    }
    static  public function registrarUsuario($nombre, $apellidos, $contrasenia, $municipio, $apodo, $fecha_creacion)
    {
        $conexion = BD::conexionBD();


        $sqlInsert = "INSERT INTO usuarios (nombre, apellidos, contrasenia, municipio, apodo, fecha_creacion ) VALUES ( :nombre, :apellidos, :contrasenia, :municipio, :apodo, :fecha_creacion)";

        $consulta = $conexion->prepare($sqlInsert);
        $consulta->bindParam(":nombre", $nombre);
        $consulta->bindParam(":apellidos", $apellidos);
        $consulta->bindParam(":contrasenia", $contrasenia);
        $consulta->bindParam(":municipio", $municipio);
        $consulta->bindParam(":apodo", $apodo);
        $consulta->bindParam(":fecha_creacion", $fecha_creacion);

        if ($consulta->execute()) {
            echo "Datos insertados corretamente";
            header("Location: login.php");
        } else {
        }
    }

    static  public function selectPerfil($nombre)
    {

        $sql = "SELECT * FROM usuarios WHERE apodo='$nombre'";
        
        $resultado = BD::conexionBD()->query($sql);
    
       // $resultado = BD::conexionBD()->query($sql);

       return $resultado;
        
    }

}
