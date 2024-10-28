from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA

def obtener_clave_privada(obtenidas=False, clave=''):
    try:
        if obtenidas and not clave:
            print("Clave privada no proporcionada.")
            exit()

        if not obtenidas:
            with open('clave_privada.txt', 'rb') as file:
                clave = file.read()

        clave_privada = RSA.import_key(clave)
        return clave_privada

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"Error al obtener la clave privada: {e}")
        exit()

def obtener_datos(archivo_origen='texto_cifrado.bin'):
    with open(archivo_origen, 'rb') as file:
        datos = file.read()
    return datos

def obtener_tamaño_clave(datos):
    return int.from_bytes(datos[:4], byteorder='big')

def obtener_clave_cifrada(datos, tamaño_clave):
    return datos[4:4 + tamaño_clave]

def obtener_iv(datos, len_key):
    return datos[4 + len_key : 4 + len_key + 16]

def obtener_datos_cifrados(datos, len_key):
    return datos[4 + len_key + 16:]  # Cambié el nombre para claridad

def obtener_clave_descifrada(clave_cifrada, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(clave_cifrada)

def descifrar_datos(clave_descifrada, iv, datos):
    cipher = AES.new(clave_descifrada, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(datos), AES.block_size)

def escribir_datos(datos_descifrados, archivo_destino='texto_descifrado.txt'):
    with open(archivo_destino, 'w') as file:  # Cambié a modo 'w'
        file.write(datos_descifrados.decode('utf-8'))  # Asegúrate de que los datos sean texto
    print(f'Datos descifrados con éxito y almacenados en el archivo {archivo_destino}')

if __name__ == "__main__":
    clave_privada = obtener_clave_privada()
    datos = obtener_datos()
    tamaño_clave = obtener_tamaño_clave(datos)
    clave_cifrada = obtener_clave_cifrada(datos, tamaño_clave)
    iv = obtener_iv(datos, tamaño_clave)
    datos_cifrados = obtener_datos_cifrados(datos, tamaño_clave)  # Asegúrate de que es correcto
    clave_descifrada = obtener_clave_descifrada(clave_cifrada, clave_privada)
    datos_descifrados = descifrar_datos(clave_descifrada, iv, datos_cifrados)
    escribir_datos(datos_descifrados)
