from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes

def load_public_key(file_path):
    """
    Carga una clave pública desde un archivo.

    :param file_path: Ruta del archivo PEM que contiene la clave pública.
    :return: La clave pública cargada.
    """
    with open(file_path, "rb") as public_file:
        return load_pem_public_key(public_file.read(), password=None)
 
def verify_signature(public_key, tipo, file_path = None, padding_Size= None, texto = None):
    """
    Verifica la firma en un archivo y devuelve el mensaje si es válido.

    :param file_path: Ruta del archivo que contiene el mensaje y la firma concatenados.
    :param public_key: Clave pública para verificar la firma.
    :param sk: clave secreta
    :return: El mensaje si la firma es válida.
    :raises Exception: Si la firma no es válida.
    """
    if file_path is not None:
        with open(file_path, "rb") as file:
            texto = file.read()

    
    if tipo == "clave_publica":
        message = texto[:800]
        signature = texto[800:]
        padding_Size = 800
    elif tipo == "c": 
        message = texto[:768]
        signature = texto[768:]
        padding_Size = 768
    else:
        message = texto[:1000]
        signature = texto[1000:]
        
    public_key.verify(
        signature,
        message,
        hashes.SHA256()  # DSA no requiere padding, solo el hash usado
    )

    if tipo == 'mensaje':
        message = message[:1000-padding_Size]


    return message  
        