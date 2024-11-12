from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from kyber import Kyber512
import os

# Extraer los datos a cifrar, por defecto se almacenarán en el archivo 'texto.txt'.
def obtener_datos(archivo_origen='texto.txt'):
    with open(archivo_origen, 'rb') as file:  
        datos = file.read()  
        file.close()
    return datos

# Extraer la clave publica del RSA, por defecto se almacenará en el archivo 'clave_publica.txt'.
def obtener_clave_publica(archivo_clave_publica= 'clave_publica_Kyber.txt'):
    with open(archivo_clave_publica, 'rb') as file:
        clave = file.read()
        file.close()

    return clave

def obtener_c_and_key(clave_publica, archivo_c="c.txt"):
    c, key = Kyber512.enc(clave_publica)
    with open(archivo_c, "wb") as file:
        file.write(c)
        file.close()
    return c, key

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

if __name__ == "__main__":
    clave_publica = obtener_clave_publica()
    datos = obtener_datos()
    t, clave = obtener_c_and_key(clave_publica)
    iv = obtener_iv()
    datos_cifrados = cifrar_datos(clave, iv, datos)
    escribir_datos(iv, datos_cifrados)
