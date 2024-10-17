



# Función para seleccionar el tamaño de la clave
def elegir_tamaño_clave():
    print()
    
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
                1. CBC (Cipher Block Chaining)
                2. ECB (Electronic Codebook)
                3. OFB (Output Feedback Mode)
                Ingrese su opción (1/2/3): """))
    while True: 
        if opcion == 1:
            return 'MODE_CBC'
        elif opcion == 2:
            return 'MODE_ECB'
        elif opcion == 3:
            return 'MODE_OFB'
        opcion = int(input("""  
                Seleccione el modo de operación AES:
                1. CBC (Cipher Block Chaining)
                2. ECB (Electronic Codebook)
                3. OFB (Output Feedback Mode)
                Ingrese su opción (1/2/3): """))
bits = elegir_tamaño_clave()
criptografia = elegir_modo_operacion()

print(f"""
Numero de bits de la clave: {bits}
Modo de operación: {criptografia}""")   
# Función para cifrar un archivo