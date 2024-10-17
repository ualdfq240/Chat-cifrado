from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# Función para seleccionar el tamaño de la clave
def elegir_tamaño_clave():
    opcion = int(input("""  
                Seleccione el tamaño de la clave AES:
                1. 128 bits (16 bytes)
                2. 192 bits (24 bytes)
                3. 256 bits (32 bytes)
                Ingrese su opción (1/2/3): """))
    while True:
        if opcion == 1:
            return 16  # 128 bits
        elif opcion == 2:
            return 24  # 192 bits
        elif opcion == 3:
            return 32  # 256 bits
        opcion = int(input("""  
                Seleccione el tamaño de la clave AES:
                1. 128 bits (16 bytes)
                2. 192 bits (24 bytes)
                3. 256 bits (32 bytes)
                Ingrese su opción (1/2/3): """))

# Función para seleccionar el modo de operación
def elegir_modo_operacion():
    opcion = int(input("""  
                Seleccione el modo de operación AES:
                1. ECB (Electronic Codebook)
                2. CBC (Cipher Block Chaining)
                3. OFB (Output Feedback Mode)
                Ingrese su opción (1/2/3): """))
    while True: 
        if opcion == 1:
            return 'MODE_ECB'
        elif opcion == 2:
            return 'MODE_CBC'
        elif opcion == 3:
            return 'MODE_OFB'
        opcion = int(input("""  
                Seleccione el modo de operación AES:
                1. CBC (Cipher Block Chaining)
                2. ECB (Electronic Codebook)
                3. OFB (Output Feedback Mode)
                Ingrese su opción (1/2/3): """))

# Función para cifrar un archivo
def cifrar_archivo(archivo, modo, bits):
    if modo == 'MODE_ECB':
        return cifrado_ECB(archivo, bits)
    elif modo == 'MODE_CBC':
        return cifrado_CBC(archivo, bits)
    else:
        return cifrado_OFB(archivo, bits)

# Función para cifrar usando ECB
def cifrado_ECB(archivo, bits):
    # Leer el archivo 
    with open(archivo, 'rb') as f:
        datos = f.read()

    # Generar la clave con el tamaño seleccionado por el usuario
    clave = get_random_bytes(bits)

    # Crear el cifrador AES en modo ECB
    cipher = AES.new(clave, AES.MODE_ECB)

    # Cifrar los datos (con padding)
    datos_cifrados = cipher.encrypt(pad(datos, AES.block_size))

    # Guardar los datos cifrados en un nuevo archivo
    archivoCifrado = 'Cifrado_ECB.txt'
    with open(archivoCifrado, 'wb') as f_cifrado:
        f_cifrado.write(datos_cifrados)

    print(f"Archivo '{archivo}' cifrado en modo ECB y guardado como f'{archivoCifrado}'")
    return archivoCifrado, clave

# Función para cifrar usando CBC
def cifrado_CBC(archivo, bits):
    # Leer el archivo
    with open(archivo, 'rb') as f:
        datos = f.read()

    # Generar la clave con el tamaño seleccionado por el usuario
    clave = get_random_bytes(bits)

    # Generar el vector de inicialización (IV)
    iv = get_random_bytes(16)

    # Crear el cifrador AES en modo CBC
    cipher = AES.new(clave, AES.MODE_CBC, iv)

    # Cifrar los datos (con padding)
    datos_cifrados = iv + cipher.encrypt(pad(datos, AES.block_size))

    # Guardar los datos cifrados en un nuevo archivo
    archivoCifrado = 'Cifrado_CBC.txt'
    with open(archivoCifrado, 'wb') as f_cifrado:
        f_cifrado.write(datos_cifrados)

    print(f"Archivo '{archivo}' cifrado en modo CBC y guardado como f'{archivoCifrado}'")
    
    # Retornar la clave para usarla en el descifrado
    return archivoCifrado, clave

# Función para cifrar usando OFB
def cifrado_OFB(archivo, bits):
    # Leer el archivo
    with open(archivo, 'rb') as f:
        datos = f.read()

    # Generar la clave y el vector de inicialización (IV)
    clave = get_random_bytes(bits)
    iv = get_random_bytes(16)

    # Crear el cifrador AES en modo OFB
    cipher = AES.new(clave, AES.MODE_OFB, iv)

    # Cifrar los datos
    datos_cifrados = iv + cipher.encrypt(datos)

    # Guardar los datos cifrados en un nuevo archivo
    archivoCifrado = 'Cifrado_OFB.txt'
    with open(archivoCifrado, 'wb') as f_cifrado:
        f_cifrado.write(datos_cifrados)

    print(f"Archivo '{archivo}' cifrado en modo OFB y guardado como '{archivoCifrado}'")
    
    # Retornar la clave para usarla en el descifrado
    return archivoCifrado, clave

# Función para descifrar un archivo
def descifrar_archivo(archivo, modo, bits, clave):
    if modo == 'MODE_ECB':
        return descifrado_ECB(archivo, bits, clave)
    elif modo == 'MODE_CBC':
        return descifrado_CBC(archivo, bits, clave)
    else:
        return descifrado_OFB(archivo, bits, clave)

# Función para descifrar usando ECB
def descifrado_ECB(archivo, bits, clave):
    # Leer el archivo cifrado
    with open(archivo, 'rb') as f:
        datos_cifrados = f.read()

    # Crear el descifrador AES con la clave
    cipher = AES.new(clave, AES.MODE_ECB)

    # Descifrar los datos (con unpadding)
    datos_descifrados = unpad(cipher.decrypt(datos_cifrados), AES.block_size)

    # Guardar los datos descifrados en un nuevo archivo
    with open('Descifrado_ECB.txt', 'wb') as f_descifrado:
        f_descifrado.write(datos_descifrados)

    print(f"Archivo '{archivo}' descifrado en modo ECB y guardado como 'Descifrado_ECB.txt'")
    
# Función para descifrar usando CBC
def descifrado_CBC(archivo, bits, clave):
    # Leer el archivo cifrado
    with open(archivo, 'rb') as f:
        datos_cifrados = f.read()

    # Extraer el IV (los primeros 16 bytes)
    iv = datos_cifrados[:16]

    # El resto son los datos cifrados
    datos_cifrados_sin_iv = datos_cifrados[16:]

    # Crear el descifrador AES con la clave y el IV
    cipher = AES.new(clave, AES.MODE_CBC, iv)

    # Descifrar los datos (con unpadding)
    datos_descifrados = unpad(cipher.decrypt(datos_cifrados_sin_iv), AES.block_size)

    # Guardar los datos descifrados en un nuevo archivo
    with open('Descifrado_CBC.txt', 'wb') as f_descifrado:
        f_descifrado.write(datos_descifrados)

    print(f"Archivo '{archivo}' descifrado en modo CBC y guardado como 'Descifrado_CBC.txt'")

# Función para descifrar usando OFB
def descifrado_OFB(archivo, bits, clave):
    # Leer el archivo cifrado
    with open(archivo, 'rb') as f:
        datos_cifrados = f.read()

    # Extraer el IV (los primeros 16 bytes)
    iv = datos_cifrados[:16]
    datos_cifrados_sin_iv = datos_cifrados[16:]

    # Crear el descifrador AES con la clave y el IV
    cipher = AES.new(clave, AES.MODE_OFB, iv)

    # Descifrar los datos
    datos_descifrados = cipher.decrypt(datos_cifrados_sin_iv)

    # Guardar los datos descifrados en un nuevo archivo
    with open('Descifrado_OFB.txt', 'wb') as f_descifrado:
        f_descifrado.write(datos_descifrados)

    print(f"Archivo '{archivo}' descifrado en modo OFB y guardado como 'Descifrado_OFB.txt'")   

# Función principal
def main():
    bits = elegir_tamaño_clave()  # Seleccionar tamaño de la clave
    modo = elegir_modo_operacion()  # Seleccionar el modo de operación
    archivoCifrado, clave = cifrar_archivo('texto.txt', modo, bits)  # Cifrar el archivo usando los parámetros seleccionados
    descifrar_archivo(archivoCifrado, modo, bits, clave)  # Descifrar el archivo cifrado

# Ejecutar la función principal
if __name__ == '__main__':
    main()
