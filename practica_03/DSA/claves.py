from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

# Generar clave privada DSA
private_key = dsa.generate_private_key(key_size=2048)

# Guardar la clave privada
with open("private_key.pem", "wb") as private_file:
    private_file.write(
        private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        )
    )

# Guardar la clave pública
public_key = private_key.public_key()
with open("public_key.pem", "wb") as public_file:
    public_file.write(
        public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Claves pública y privada generadas y guardadas.")