
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
 
def verify_signature(file_path, public_key):
    """
    Verifica la firma en un archivo y devuelve el mensaje si es válido.

    :param file_path: Ruta del archivo que contiene el mensaje y la firma concatenados.
    :param public_key: Clave pública para verificar la firma.
    :param sk: clave secreta
    :return: El mensaje si la firma es válida.
    :raises Exception: Si la firma no es válida.
    """
    with open(file_path, "rb") as file:
        texto = file.read()

    message = texto[:800]
    signature = texto[800:]

    public_key.verify(
        signature,
        message,
        hashes.SHA256()  # DSA no requiere padding, solo el hash usado
    )
    return message  # Devuelve el mensaje como cadena de texto.
        