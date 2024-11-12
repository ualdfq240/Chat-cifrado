from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA

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

    clave_publica = RSA.import_key(clave)
    return clave_publica

# Generar la clave del AES para cifrar los datos, esta tendrá un tamaño de 32 bytes (256 bits).
def obtener_clave():
    return get_random_bytes(32)

# Obtener el iv del AES para cifrar los datos, este tendrá un tamaño de 16 bytes (128 bits).
def obtener_iv():
    return get_random_bytes(16)  

# Cifrar la clave del AES usando la clave publica del RSA obtenida anteriormente.
def cifrar_clave(clave_publica, clave):
    cipher = PKCS1_OAEP.new(clave_publica)
    
    return cipher.encrypt(clave)

# Cifrar los datos, obtenidos anteriormente, usando el iv y la clave de AES generada anteriormente.
def cifrar_datos(clave, iv, datos):
    cipher = AES.new(clave, AES.MODE_CBC, iv)
    
    return cipher.encrypt(pad(datos, AES.block_size))

# Escribir la clave del AES cifrada con RSA, el iv y los datos cifrados con AES, por defecto se escriben en el archivo'texto_cifrado.bin'.
def escribir_datos(clave_cifrada, iv, datos, archivo_destino='texto_cifrado.bin'):
     
    with open(archivo_destino, 'wb') as file: 
        file.write(clave_cifrada)    
        file.write(iv)    
        file.write(datos)  
        file.close()
    print(f'Datos cifrados con exito y almacenados en el archivo {archivo_destino}')

if __name__ == "__main__":
    clave_publica = obtener_clave_publica()
    datos = obtener_datos()
    clave = obtener_clave()
    iv = obtener_iv()
    clave_cifrada = cifrar_clave(clave_publica, clave)
    datos_cifrados = cifrar_datos(clave, iv, datos)
    escribir_datos(clave_cifrada, iv, datos_cifrados)
