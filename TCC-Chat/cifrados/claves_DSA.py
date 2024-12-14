import os
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    PrivateFormat,
    NoEncryption,
)

def generar_claves_dsa():
    """Genera las claves pública y privada de DSA."""
    private_key = dsa.generate_private_key(key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def exportar_clave_privada(clave_privada, ruta):
    """Exporta la clave privada a la ruta especificada."""

    with open(ruta, 'wb') as file:
        file.write(
            clave_privada.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption()
            )
        )
    print(f'Clave privada exportada en: {ruta}')

def exportar_clave_publica(clave_publica, ruta):
    """Exporta la clave pública a la ruta especificada."""
    with open(ruta, 'wb') as file:
        file.write(
            clave_publica.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            )
        )
    print(f'Clave pública exportada en: {ruta}')

def generar_y_exportar_claves(ruta_carpeta):
    """Genera las claves y las guarda en la ruta especificada."""
    # Crear la carpeta si no existe
    os.makedirs(ruta_carpeta, exist_ok=True)
    
    # Generar claves
    private_key, public_key = generar_claves_dsa()
    
    
    
    # Exportar claves con prefijo basado en la ruta
    exportar_clave_privada(private_key, os.path.join(ruta_carpeta,'clave_privada.pem'))
    exportar_clave_publica(public_key, os.path.join(ruta_carpeta,'clave_publica.pem'))

    return public_key, private_key

if __name__ == '__main__':
    # Ruta donde se guardarán las claves
    ruta_deseada = input("Introduce la ruta donde guardar las claves: ").strip()
    generar_y_exportar_claves(ruta_deseada)
