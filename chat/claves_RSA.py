from Crypto.PublicKey import RSA


# Obtener la clave privada de RSA que obtiene tanto, la clave publica, el n, p y q. 
# El tamaño del cifrado, será de 256 bytes (2048 bits).
private_key = RSA.generate(2048)  

# Escribir los datos en el archivo 'clave_privada.txt'.
with open('clave_privada.txt', 'wb') as file:
    file.write(private_key.export_key())

print('Clave privada exportada en el archivo clave_privada.txt')  

# Obtener la clave publica.
public_key = private_key.public_key() 

# Escribir los datos en el archivo 'clave_publica.txt'.
with open('clave_publica.txt', 'wb') as file:
    file.write(public_key.export_key())
    
print('Clave publica exportada en el archivo clave_publica.txt')

# Obtener p, q y n.
p = private_key.p
q = private_key.q
n = private_key.n

# Escribir los datos en el archivo 'valores_pqn.txt'.
with open('valores_pqn.txt', 'w') as file:
    file.write(f"p: {p}\n")
    file.write(f"q: {q}\n")
    file.write(f"n: {n}\n")

print('Valores de p, q y n exportados en el archivo valores_pqn.txt')