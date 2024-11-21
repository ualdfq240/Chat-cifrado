from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA

# Extraer la clave privada del RSA, por defecto se almacenará en el archivo 'clave_privada.txt'.
def obtener_clave_privada(archivo_clave_privada= 'clave_privada_RSA.txt'):
    with open(archivo_clave_privada, 'rb') as file:
        clave = file.read()
        file.close()

    clave_privada = RSA.import_key(clave)
    return clave_privada

# Extraer la clave del AES cifrada con RSA, el iv y los datos cifrados con AES, por defecto se encuentran en el archivo 'texto_cifrado.bin'.
def obtener_datos(archivo_origen='texto_cifrado.bin'):
    with open(archivo_origen, 'rb') as file:
        datos = file.read()
    return datos

# Obtener la clave del AES cifrada con RSA, que tendrá un tamaño fijo 256 bytes (2048 bits) tal y como se especificó en la generación de las claves.
def obtener_clave_cifrada(datos):
    return datos[:256]

# Obtener el iv del AES, que ocupará los siguientes 16 bytes (128 bits) a partir de los 256 bytes (2048 bits) de la clave AES cifrada.
def obtener_iv(datos):
    return datos[256: 256 + 16]

# Obtener los datos cifrados, que ocuparán los bytes restantes a partir de los 256 bytes (2048 bits) de la clave AES cifrada y los 16 bytes (128 bits) del iv. 
def obtener_datos_cifrados(datos):
    return datos[256 + 16:]  

# Descifrar la clave AES, usando la clave privada de la clave publica con la que se cifró la clave del AES.
def obtener_clave_descifrada(clave_cifrada, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(clave_cifrada)

# Descifrar los datos cifrados con AES, usando su clave y su iv.
def descifrar_datos(clave_descifrada, iv, datos):
    cipher = AES.new(clave_descifrada, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(datos), AES.block_size)

# Escribir los datos descifrados, por defecto se escribirán en el archivo 'texto_descifrado.txt'.
def escribir_datos(datos_descifrados, archivo_destino='texto_descifrado.txt'):
    with open(archivo_destino, 'w') as file:  # Cambié a modo 'w'
        file.write(datos_descifrados.decode('utf-8'))  # Asegúrate de que los datos sean texto
    print(f'Datos descifrados con éxito y almacenados en el archivo {archivo_destino}')

if __name__ == "__main__":
    clave_privada = obtener_clave_privada()
    datos = obtener_datos()
    clave_cifrada = obtener_clave_cifrada(datos)
    iv = obtener_iv(datos)
    datos_cifrados = obtener_datos_cifrados(datos)  
    clave_descifrada = obtener_clave_descifrada(clave_cifrada, clave_privada)
    datos_descifrados = descifrar_datos(clave_descifrada, iv, datos_cifrados)
    escribir_datos(datos_descifrados)
