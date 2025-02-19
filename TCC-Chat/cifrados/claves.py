from cifrados.kyber_py.kyber import Kyber512  

def generar_claves_kyber():
    """Genera las claves pública y privada de Kyber512."""
    return Kyber512.keygen()

def exportar_clave_privada(clave_privada, archivo='clave_privada.txt'):
    """Exporta la clave privada a un archivo especificado."""
    with open(archivo, 'wb') as file:
        file.write(clave_privada)
    print(f'Clave privada exportada en el archivo {archivo}')

def exportar_clave_publica(clave_publica, archivo='clave_publica.txt'):
    """Exporta la clave pública a un archivo especificado."""
    with open(archivo, 'wb') as file:
        file.write(clave_publica)
    print(f'Clave pública exportada en el archivo {archivo}')

