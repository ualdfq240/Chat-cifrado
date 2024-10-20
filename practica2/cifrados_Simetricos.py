from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Función para cifrar con el sistema Cesar
def metodo_Cesar():
    modo = elegir_modo()
    diccionario = crear_diccionario()
    desplazamiento, archivoCifrado = cifrar_archivo_Cesar('texto.txt', modo, diccionario)
    descifrar_archivo_Cesar(archivoCifrado, modo, desplazamiento, diccionario)

# Función para elegir el tipo de cifrado Cesar
def elegir_modo():
    opcion = int(input("""  
                Seleccione el modo de cifrado Cesar:
                1. Cifrado César con desplazamiento fijo
                2. Cifrado César con clave
                Ingrese su opción (1/2): """))
    while True: 
        if opcion == 1:
            return 'MODE_fijo'
        elif opcion == 2:
            return 'MODE_Clave'
        opcion = int(input("""  
                Seleccione el modo de cifrado Cesar:
                1. Cifrado César con desplazamiento fijo
                2. Cifrado César con clave
                Ingrese su opción (1/2): """))

def crear_diccionario():
    # Crear un diccionario para las letras y sus posiciones
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    return {letra: i for i, letra in enumerate(alfabeto)}

# Funcion para cifrar el 
def cifrar_archivo_Cesar(archivo, modo, diccionario):
    if modo == 'MODE_fijo':
        desplazamiento = int(input('Eliga de cuanto quiere que sea el desplazamiento '))
        return desplazamiento, cifrado_Fijo(archivo, desplazamiento, diccionario)
    else:
        clave = input('Ingrese un palabra que será su clave ')
        return clave, cifrado_Clave(archivo, clave, diccionario)

# Cifrado usando el metodo Cesar con un desplazamiento fijo
def cifrado_Fijo(archivo, desplazamiento, diccionario):
    with open(archivo, 'r') as file:
        datos = file.read()
    
    datos_cifrados = ""

    for char in datos:
        if char.lower() in diccionario:  # Verificar si es una letra
            nueva_pos = (diccionario[char.lower()] + desplazamiento) % 26
            nuevo_char = list(diccionario.keys())[nueva_pos]
            # Mantener el caso original
            if char.isupper():
                nuevo_char = nuevo_char.upper()
            datos_cifrados += nuevo_char
        else:
            datos_cifrados += char  # Añadir caracteres no alfabéticos sin cambios

    archivoCifrado = 'Cifrado_Fijo.txt'
    with open(archivoCifrado, 'w') as f_cifrado:
        f_cifrado.write(datos_cifrados)

    print(f"Archivo '{archivo}' cifrado en modo Cesar fijo y guardado como f'{archivoCifrado}'")

    return archivoCifrado

# Cifrado usando el metodo Cesar con una clave
def cifrado_Clave(archivo, clave, diccionario):
    with open(archivo, 'r') as file:
        datos = file.read()
    
    datos_cifrados = ""
    clave_ajustada = ajustar_clave(datos, clave)

    for char, char_clave in zip(datos, clave_ajustada):
        if char.lower() in diccionario:  # Verificar si es una letra
            # Obtener el desplazamiento de la letra de la clave
            desplazamiento = diccionario[char_clave]
            # Obtener la posición actual y calcular la nueva
            nueva_pos = (diccionario[char.lower()] + desplazamiento) % 26
            # Obtener la letra correspondiente
            nuevo_char = list(diccionario.keys())[nueva_pos]
            # Mantener el caso original
            if char.isupper():
                nuevo_char = nuevo_char.upper()
            datos_cifrados += nuevo_char
        else:
            datos_cifrados += char  # Añadir caracteres no alfabéticos sin cambios

    archivoCifrado = 'Cifrado_Clave.txt'
    with open(archivoCifrado, 'w') as f_cifrado:
        f_cifrado.write(datos_cifrados)

    print(f"Archivo '{archivo}' cifrado en modo César clave y guardado como '{archivoCifrado}'")
    return archivoCifrado

# Función para descifrar con el sistema Cesar
def descifrar_archivo_Cesar(archivoCifrado, modo, desplazamiento, diccionario):
    if modo == 'MODE_fijo':
        return descifrado_Fijo(archivoCifrado, desplazamiento, diccionario)
    else:
        return descifrado_Clave(archivoCifrado, desplazamiento, diccionario)

# Descifrar usnado cesar con un desplazamiento fijo
def descifrado_Fijo(archivo, desplazamiento, diccionario):
    with open(archivo, 'r') as file:
        datos = file.read()
    
    datos_cifrados = ""

    for char in datos:
        if char.lower() in diccionario:  # Verificar si es una letra
            nueva_pos = (diccionario[char.lower()] - desplazamiento) % 26
            nuevo_char = list(diccionario.keys())[nueva_pos]
            # Mantener el caso original
            if char.isupper():
                nuevo_char = nuevo_char.upper()
            datos_cifrados += nuevo_char
        else:
            datos_cifrados += char  # Añadir caracteres no alfabéticos sin cambios


    archivoCifrado = 'Desifrado_Fijo.txt'
    with open(archivoCifrado, 'w') as f_cifrado:
        f_cifrado.write(datos_cifrados)

    print(f"Archivo '{archivo}' descifrado en modo fijo y guardado como f'{archivoCifrado}'")

# Descifrado usando el metodo Cesar con una clave
def descifrado_Clave(archivo, clave, diccionario):
    with open(archivo, 'r') as file:
        datos = file.read()
    
    datos_descifrados = ""
    clave_ajustada = ajustar_clave(datos, clave)

    for char, char_clave in zip(datos, clave_ajustada):
        if char.lower() in diccionario:  # Verificar si es una letra
            # Obtener el desplazamiento de la letra de la clave
            desplazamiento = diccionario[char_clave.lower()]  # Asegúrate de que sea minúscula
            # Obtener la posición actual y calcular la nueva
            nueva_pos = (diccionario[char.lower()] - desplazamiento) % 26
            # Obtener la letra correspondiente
            nuevo_char = list(diccionario.keys())[nueva_pos]
            # Mantener el caso original
            if char.isupper():
                nuevo_char = nuevo_char.upper()
            datos_descifrados += nuevo_char
        else:
            datos_descifrados += char  # Añadir caracteres no alfabéticos sin cambios

    archivoDescifrado = 'Descifrado_clave.txt'
    with open(archivoDescifrado, 'w') as f_descifrado:
        f_descifrado.write(datos_descifrados)

    print(f"Archivo '{archivo}' descifrado en modo César clave y guardado como '{archivoDescifrado}'")

# Ajustar clave a la lonjitud del texto
def ajustar_clave(texto, clave):
    # Ajustar la clave para que tenga la misma longitud que el texto
    clave_ajustada = []
    for i in range(len(texto)):
        clave_ajustada.append(clave[i % len(clave)].lower())  # Repetir la clave
    return ''.join(clave_ajustada)

# Función para cifrar con AES
def metodo_AES():
    bits = elegir_tamaño_clave()  # Seleccionar tamaño de la clave
    modo = elegir_modo_operacion()  # Seleccionar el modo de operación
    archivoCifrado, clave = cifrar_archivo_AES('texto.txt', modo, bits)  # Cifrar el archivo usando los parámetros seleccionados
    descifrar_archivo_AES(archivoCifrado, modo, bits, clave)  # Descifrar el archivo cifrado

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
def cifrar_archivo_AES(archivo, modo, bits):
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
def descifrar_archivo_AES(archivo, modo, bits, clave):
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
    while True:
        tipo_Cifrado = int(input("""  
                Seleccione el modo de cifrado simetrico:
                1. Cifrado Cesar
                2. Cifrado AES
                Ingrese su opción (1/2: """))
        if tipo_Cifrado == 1:
            metodo_Cesar()
            exit()
        elif tipo_Cifrado == 2:
            metodo_AES()
            exit()
        else:
            tipo_Cifrado = int(input("""  
                Seleccione el modo de cifrado simetrico:
                1. Cifrado Cesar
                2. Cifrado AES
                Ingrese su opción (1/2: """))

# Ejecutar la función principal
if __name__ == '__main__':
    main()
