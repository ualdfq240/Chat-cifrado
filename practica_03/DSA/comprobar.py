import json
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes

# Cargar la clave pública desde el archivo
with open("public_key.pem", "rb") as public_file:
    public_key = load_pem_public_key(public_file.read())

# Cargar el mensaje firmado desde el archivo JSON
with open("firma.txt", "rb") as file:
    texto = file.read()

message = texto[:800]
signature = texto[800:]


# Verificar la firma
try:
    public_key.verify(
        signature,
        message,
        hashes.SHA256()  # DSA no requiere padding, solo el hash usado
    )
    print("La firma es válida.")
except Exception as e:
    print("La firma no es válida:", e)
