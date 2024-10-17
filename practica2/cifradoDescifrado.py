


# Función para seleccionar el tamaño de la clave
def elegir_tamaño_clave():
    print("Seleccione el tamaño de la clave AES:")
    print("1. 128 bits (16 bytes)")
    print("2. 192 bits (24 bytes)")
    print("3. 256 bits (32 bytes)")
    
    opcion = input("Ingrese su opción (1/2/3): ")
    
    if opcion == '1':
        return 16  # 128 bits
    elif opcion == '2':
        return 24  # 192 bits
    elif opcion == '3':
        return 32  # 256 bits
    else:
        print("Opción no válida. Seleccionando 128 bits por defecto.")
        return 16

# Función para seleccionar el modo de operación
def elegir_modo_operacion():
    print("\nSeleccione el modo de operación AES:")
    print("1. CBC (Cipher Block Chaining)")
    print("2. ECB (Electronic Codebook)")
    print("3. OFB (Output Feedback Mode)")


    opcion = input("Ingrese su opción (1/2/3): ")
    
    if opcion == '1':
        return AES.MODE_CBC
    elif opcion == '2':
        return AES.MODE_ECB
    elif opcion == '3':
        return AES.MODE_OFB
    else:
        print("Opción no válida. Seleccionando CBC por defecto.")
        return AES.MODE_CBC

