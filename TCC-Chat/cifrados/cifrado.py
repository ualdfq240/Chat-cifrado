from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256
from cifrados import firmar
from cifrados.kyber_py.kyber import Kyber512

# Extraer los datos a cifrar, por defecto se almacenarán en el archivo 'texto.txt'.
def obtener_datos(archivo_origen='texto.txt'):
    with open(archivo_origen, 'rb') as file:  
        datos = file.read()  
        file.close()
    return datos

# Extraer la clave publica del RSA, por defecto se almacenará en el archivo 'clave_publica.txt'.
def obtener_clave_publica(archivo_clave_publica= 'clave_publica.txt'):
    with open(archivo_clave_publica, 'rb') as file:
        clave = file.read()
        file.close()

    return clave

def obtener_key_and_c(clave_publica,sk, archivo_c="firma_c.txt"):
    key, c = Kyber512.encaps(clave_publica)
    firma_c = firmar.firmar_mensaje(sk, c)
    firmar.guardar_firma(archivo_c, c, firma_c)
    
    return key, c


def obtener_32_bytes(texto):
    """
    Genera 32 bytes a partir de un texto o número usando SHA-256.

    :param texto: Texto o número a convertir (str o int).
    :return: Bytes generados de 32 bytes (SHA-256 hash).
    """
    if isinstance(texto, int):
        texto = str(texto)  # Convierte el número a cadena
    elif not isinstance(texto, str):
        raise ValueError("El texto debe ser una cadena o un número.")
    
    # Crea un objeto hash y devuelve el digest de 32 bytes
    hash_obj = SHA256.new(data=texto.encode('utf-8'))
    return hash_obj.digest() 

# Obtener el iv del AES para cifrar los datos, este tendrá un tamaño de 16 bytes (128 bits).
def obtener_iv():
    return get_random_bytes(16)  

# Cifrar los datos, obtenidos anteriormente, usando el iv y la clave de AES generada anteriormente.
def cifrar_datos(clave, iv, datos):
    cipher = AES.new(clave, AES.MODE_CBC, iv)
    
    return cipher.encrypt(pad(datos, AES.block_size))

# Escribir la clave del AES cifrada con RSA, el iv y los datos cifrados con AES, por defecto se escriben en el archivo'texto_cifrado.bin'.
def escribir_datos(iv, datos, archivo_destino='texto_cifrado.bin'):
     
    with open(archivo_destino, 'wb') as file:  
        file.write(iv)    
        file.write(datos)  
        file.close()
    print(f'Datos cifrados con exito y almacenados en el archivo {archivo_destino}')

