from cifrados import cifrado, descifrado, claves
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.secret_key = "secret_key"
socketio = SocketIO(app)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GENERAL_CHATS_PATH = os.path.join(BASE_PATH, "general/chats")
GENERAL_USERS_PATH = os.path.join(BASE_PATH, "general/users")
LOCAL_USERS_PATH = os.path.join(BASE_PATH, "local/users")

# Crear directorios generales si no existen
os.makedirs(GENERAL_USERS_PATH, exist_ok=True)
os.makedirs(LOCAL_USERS_PATH, exist_ok=True)

users = {}
connected_users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    if username and username not in users:
        users[username] = username
        session['username'] = username

        GENERAL_USER_PATH = os.path.join(GENERAL_USERS_PATH, username)
        LOCAL_USER_PATH = os.path.join(LOCAL_USERS_PATH, username)
        os.makedirs(GENERAL_USER_PATH, exist_ok=True)
        os.makedirs(LOCAL_USER_PATH, exist_ok=True)

        # Generar y exportar claves
        clave_publica, clave_privada = claves.generar_claves_kyber()
        claves.exportar_clave_publica(clave_publica, os.path.join(GENERAL_USER_PATH, 'clave_publica.txt'))
        claves.exportar_clave_privada(clave_privada, os.path.join(LOCAL_USER_PATH, 'clave_privada.txt'))
        
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
    connected_users.pop(request.sid, None)

@socketio.on('request_users')
def handle_request_users():
    username = session.get('username')
    filtered_users = [user for user in users.keys() if user != username]
    emit('user_list', filtered_users, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = session.get('username')
    recipient = data.get('recipient')
    message = data['message'].encode()

    LOCAL_USERNAME_PATH = os.path.join(LOCAL_USERS_PATH, username)
    LOCAL_USERNAME_RECIPIENT_PATH = os.path.join(LOCAL_USERNAME_PATH, recipient)
    os.makedirs(LOCAL_USERNAME_RECIPIENT_PATH, exist_ok=True)

    KEY_PATH = os.path.join(LOCAL_USERNAME_RECIPIENT_PATH, 'key.txt')
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, 'rb') as file:
            clave = file.read()
    else:
        GENERAL_RECIPIENT_PATH = os.path.join(GENERAL_USERS_PATH, recipient)
        clave_publica = cifrado.obtener_clave_publica(os.path.join(GENERAL_RECIPIENT_PATH, 'clave_publica.txt'))
        GENERAL_RECIPIENT_USERNAME_PATH = os.path.join(GENERAL_RECIPIENT_PATH,username)
        os.makedirs(GENERAL_RECIPIENT_USERNAME_PATH, exist_ok=True)
        clave, c = cifrado.obtener_key_and_c(clave_publica, os.path.join(GENERAL_RECIPIENT_USERNAME_PATH,'c.txt'))
        with open(KEY_PATH, 'wb') as file:
            file.write(clave)

    iv = cifrado.obtener_iv()
    mensaje_cifrado = cifrado.cifrar_datos(clave, iv, message)
    message_crypto = iv + mensaje_cifrado

    send({
        'username': username,
        'recipient': recipient or 'todos',
        'message': message_crypto
    }, broadcast=True)

@socketio.on('decrypt_message')
def handle_decrypt_message(recipient, encrypted_message):

    username = session.get('username')

    LOCAL_USERNAME_PATH = os.path.join(LOCAL_USERS_PATH, username)
    LOCAL_USERNAME_RECIPIENT_PATH = os.path.join(LOCAL_USERNAME_PATH, recipient)
    KEY_PATH = os.path.join(LOCAL_USERNAME_RECIPIENT_PATH, 'key.txt')
    

    try:
        if os.path.exists(KEY_PATH):
            with open(KEY_PATH, 'rb') as file:
                clave = file.read()
        else:
            GENERAL_RECIPIENT_PATH = os.path.join(GENERAL_USERS_PATH, recipient)
            clave_publica = cifrado.obtener_clave_publica(os.path.join(GENERAL_RECIPIENT_PATH, 'clave_publica.txt'))
            GENERAL_USERNAME_PATH = os.path.join(GENERAL_USERS_PATH, username)
            GENERAL_USERNAME_RECIPIENT_PATH = os.path.join(GENERAL_USERNAME_PATH, recipient)
            c = descifrado.obtener_c(os.path.join(GENERAL_USERNAME_RECIPIENT_PATH, 'c.txt'))
            clave_privada = descifrado.obtener_clave_privada(os.path.join(LOCAL_USERNAME_PATH, 'clave_privada.txt'))
            clave = descifrado.obtener_clave(clave_privada, c)
            os.mkdir(LOCAL_USERNAME_RECIPIENT_PATH)
            with open(KEY_PATH, 'wb') as file:
                file.write(clave)

        iv = descifrado.obtener_iv(encrypted_message)
        datos_cifrados = descifrado.obtener_datos_cifrados(encrypted_message)
        message = descifrado.descifrar_datos(clave, iv, datos_cifrados).decode()
    except Exception:
        message = encrypted_message.hex()

    emit('decrypted_message', {'message': message}, to=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
