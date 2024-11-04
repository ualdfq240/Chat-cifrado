<?php


class BD {

    public static $conexion;
    

    //OK
    // Inicializamos la conexion
     static function conexionBD() {
      
        self::$conexion = new PDO('mysql:host=127.0.0.1;dbname=criptochat;charset=utf8mb4', 'root', '');
        
        return self::$conexion;
 
    }
      static function ejecutaConsulta($sql) {
        $conexion2 = self::conexionBD();
        $resultado = null;

        if (isset($conexion2)) {
            $resultado = self::conexionBD()->query($sql);
            
        }
        return $resultado;
    }
 
    public static function verificaCliente($nombre, $contrasena) {
        $sql = "SELECT password  FROM usuarios WHERE username='$nombre'";
        $resultado = self::ejecutaConsulta($sql);
        $verificado = false;

        if ($resultado) {
            $fila = $resultado->fetch();

            if ($fila !== false) {



                if (($contrasena== $fila['password'])) {
                    $verificado = true;
                } else {
                    $verificado = false;
                }

                return $resultado;
            }
        }
    }
    
    
    
}
?>
