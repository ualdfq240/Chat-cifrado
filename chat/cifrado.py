from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA

def obtener_datos(archivo_origen='texto.txt'):
    with open(archivo_origen, 'rb') as file:  
        datos = file.read()  
        file.close()
    return datos

def obtener_clave_publica(obtenidas=False, clave=''):
    try:
        if obtenidas and not clave:
            print("Clave pública no proporcionada.")
            exit()

        if not obtenidas:
            with open('clave_publica.txt', 'rb') as file:
                clave = file.read()
                file.close()

        clave_publica = RSA.import_key(clave)
        return clave_publica

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"Error al obtener la clave pública: {e}")
        exit()

def obtener_clave():
    return get_random_bytes(32)

def obtener_iv():
    return get_random_bytes(16)  

def cifrar_clave(clave_publica, clave):
    cipher = PKCS1_OAEP.new(clave_publica)
    
    return cipher.encrypt(clave)

def cifrar_datos(clave, iv, datos):
    cipher = AES.new(clave, AES.MODE_CBC, iv)
    
    return cipher.encrypt(pad(datos, AES.block_size))

def obtener_tamaño_clave(clave_cifrada):
    return len(clave_cifrada).to_bytes(4, byteorder='big') 

def escribir_datos(clave_cifrada_len, clave_cifrada, iv, datos, archivo_destino='texto_cifrado.bin'):
     
    with open(archivo_destino, 'wb') as file:
        file.write(clave_cifrada_len)  
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
    clave_cifrada_len = obtener_tamaño_clave(clave_cifrada)
    escribir_datos(clave_cifrada_len, clave_cifrada, iv, datos_cifrados)
