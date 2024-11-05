from cifrado import claves_RSA, cifrado, descifrado
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.secret_key = "secret_key"
socketio = SocketIO(app)

# Ruta base donde se crearán los directorios de los usuarios
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
USERS_PATH = os.path.join(BASE_PATH, 'users')

# Crea el directorio base si no existe
if not os.path.exists(USERS_PATH):
    os.mkdir(USERS_PATH)

users = {}
connected_users = {}  # Almacena los usuarios conectados

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    if username and username not in users:
        users[username] = username
        session['username'] = username

        user_dir = os.path.join(USERS_PATH, username)
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        clave_privada = claves_RSA.generar_clave_privada()
        claves_RSA.exportar_clave_privada(clave_privada, os.path.join(user_dir, 'clave_privada.txt'))
        claves_RSA.exportar_clave_publica(clave_privada, os.path.join(user_dir, 'clave_publica.txt'))

        return redirect(url_for('chat', username=username))
    return 'El nombre de usuario ya existe o es inválido.'

@app.route('/chat/<username>')
def chat(username):
    if username in users:
        return render_template('chat.html', username=username)
    return redirect(url_for('home'))

@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    if username:
        connected_users[request.sid] = username

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in connected_users:
        del connected_users[request.sid]

@socketio.on('request_users')
def handle_request_users():
    username = session.get('username')  # Obtiene el nombre de usuario de la sesión
    filtered_users = [user for user in users.keys() if user != username]  # Filtra el usuario de origen
    emit('user_list', filtered_users, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = session.get('username')  # Propietario del mensaje (quien envía)
    recipient = data.get('recipient')  # Destinatario del mensaje
    message = data['message'].encode()  # Convertimos el mensaje en bytes

    print(f"recipient {recipient}")

    # Obtener la clave pública del destinatario
    if recipient in users:
        recipient_key_path = os.path.join(USERS_PATH, recipient, 'clave_publica.txt')
    else:
        recipient_key_path = os.path.join(USERS_PATH, username, 'clave_publica.txt')

    # Cargar la clave pública del destinatario
    clave_publica = cifrado.obtener_clave_publica(recipient_key_path)

    # Cifrar el mensaje
    clave_aes = cifrado.obtener_clave()  # Generar la clave de AES
    iv = cifrado.obtener_iv()  # Generar el IV de AES
    clave_aes_cifrada = cifrado.cifrar_clave(clave_publica, clave_aes)  # Cifrar la clave de AES
    mensaje_cifrado = cifrado.cifrar_datos(clave_aes, iv, message)  # Cifrar el mensaje

    # Guardar el mensaje cifrado en el archivo del propietario
    path = os.path.join(USERS_PATH, username)
    file_text = os.path.join(path, "texto.txt")
    message_crypto = clave_aes_cifrada + iv + mensaje_cifrado
    with open(file_text, 'ab') as file:
        file.write(message_crypto)

    # Enviar el mensaje cifrado a todos los usuarios conectados
    send({
        'username': username,
        'recipient': recipient if recipient else 'todos',
        'message': message_crypto  # Enviar el mensaje cifrado
    }, broadcast=True)

@socketio.on('decrypt_message')
def handle_decrypt_message(data):
    encrypted_message = data
    username = session.get('username')
    
    user_dir = os.path.join(USERS_PATH, username)
    private_key_path = os.path.join(user_dir, 'clave_privada.txt')
    clave_privada = descifrado.obtener_clave_privada(private_key_path)

    try:
        # Extraer clave cifrada, IV y datos cifrados
        clave_cifrada = descifrado.obtener_clave_cifrada(encrypted_message)
        iv = descifrado.obtener_iv(encrypted_message)
        datos_cifrados = descifrado.obtener_datos_cifrados(encrypted_message)
        
        clave = descifrado.obtener_clave_descifrada(clave_cifrada, clave_privada)
        message = descifrado.descifrar_datos(clave, iv, datos_cifrados).decode()
    except Exception as e:
        message = encrypted_message.hex()

    # Enviar el mensaje (descifrado o cifrado) junto con el remitente al cliente
    emit('decrypted_message', {'message': message}, to=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
