import json
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes

def cargar_clave_privada(ruta_clave):
    with open(ruta_clave, "rb") as private_file:
        return load_pem_private_key(private_file.read(), password=None)

def firmar_mensaje(private_key, mensaje):
    return private_key.sign(
        mensaje,
        hashes.SHA256()
    )

def guardar_firma(ruta_archivo, mensaje, firma):
    with open(ruta_archivo, 'wb') as file:
        file.write(mensaje)
        file.write(firma)
        file.close()
    
    print(f'firma guardada en {ruta_archivo}')

def main():
    # Cargar la clave privada desde el archivo
    private_key = cargar_clave_privada("private_key.pem")

    with open('clave_publica_Kyber.txt', 'rb') as file:
        message = file.read()

    # Firmar el mensaje
    signature = firmar_mensaje(private_key, message)

    # Guardar el texto firmado y la firma en un archivo JSON
    # guardar_firma("firma.txt", message, signature)

    print("Texto firmado y guardado en 'firma.txt'")

if __name__ == "__main__":
    main()