from Crypto.PublicKey import RSA


private_key = RSA.generate(2048)

public_key = private_key.public_key()

with open('clave_publica.txt', 'wb') as file:
    file.write(public_key.export_key())
    
print('Clave publica exportada en el archivo clave_publica.txt')    

with open('clave_privada.txt', 'wb') as file:
    file.write(private_key.export_key())

print('Clave privada exportada en el archivo clave_privada.txt')  