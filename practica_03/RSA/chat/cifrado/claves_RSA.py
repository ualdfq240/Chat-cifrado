from Crypto.PublicKey import RSA

def generar_clave_privada(bits=2048):
    """Genera una clave privada RSA de un tamaño especificado."""
    return RSA.generate(bits)

def exportar_clave_privada(clave_privada, archivo='clave_privada_RSA.txt'):
    """Exporta la clave privada a un archivo especificado."""
    with open(archivo, 'wb') as file:
        file.write(clave_privada.export_key())
    print(f'Clave privada exportada en el archivo {archivo}')

def exportar_clave_publica(clave_privada, archivo='clave_publica_RSA.txt'):
    """Obtiene la clave pública de una clave privada y la exporta a un archivo."""
    public_key = clave_privada.public_key()
    with open(archivo, 'wb') as file:
        file.write(public_key.export_key())
    print(f'Clave pública exportada en el archivo {archivo}')

def exportar_valores_pqn(clave_privada, archivo='valores_pqn.txt'):
    """Exporta los valores p, q y n de una clave privada a un archivo."""
    p = clave_privada.p
    q = clave_privada.q
    n = clave_privada.n
    with open(archivo, 'w') as file:
        file.write(f"p: {p}\n")
        file.write(f"q: {q}\n")
        file.write(f"n: {n}\n")
    print(f'Valores de p, q y n exportados en el archivo {archivo}')

def main():
    # Generar la clave privada
    private_key = generar_clave_privada()
    
    # Exportar clave privada
    exportar_clave_privada(private_key)
    
    # Exportar clave pública
    exportar_clave_publica(private_key)
    
    # Exportar valores de p, q y n
    exportar_valores_pqn(private_key)

if __name__ == '__main__':
    main()
