from cifrados import cifrado, descifrado, claves, claves_DSA, firmar, comprobar
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.secret_key = "secret_key"
socketio = SocketIO(app)

mkdir = lambda path: os.makedirs(path, exist_ok=True) 
file_exists = lambda path: os.path.exists(path) 
join_path = lambda *args: os.path.join(*args)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GENERAL_CHATS_PATH = join_path(BASE_PATH, "general/chats")
GENERAL_USERS_PATH = join_path(BASE_PATH, "general/users")
LOCAL_USERS_PATH = join_path(BASE_PATH, "local/users")
SERVER_PATH = join_path(BASE_PATH, 'server')

# Crear directorios generales si no existen
mkdir(GENERAL_USERS_PATH)
mkdir(LOCAL_USERS_PATH)
mkdir(SERVER_PATH)

pk, sk = claves_DSA.generar_y_exportar_claves(SERVER_PATH)

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

        GENERAL_USER_PATH = join_path(GENERAL_USERS_PATH, username)
        LOCAL_USER_PATH = join_path(LOCAL_USERS_PATH, username)
        LOCAL_USER_CHATS_PATH = join_path(LOCAL_USER_PATH, 'Registro chats')
        mkdir(GENERAL_USER_PATH)
        mkdir(LOCAL_USER_PATH)
        

        # Generar y exportar claves
        clave_publica, clave_privada = claves.generar_claves_kyber()
        claves.exportar_clave_privada(clave_privada, join_path(LOCAL_USER_PATH, 'clave_privada.txt'))

        firma = firmar.firmar_mensaje(sk, clave_publica)
        firmar.guardar_firma(join_path(GENERAL_USER_PATH, 'firma_clave_publica.txt'), clave_publica, firma)        
        

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

    LOCAL_USERNAME_PATH = join_path(LOCAL_USERS_PATH, username)
    LOCAL_USERNAME_RECIPIENT_PATH = join_path(LOCAL_USERNAME_PATH, recipient)
    mkdir(LOCAL_USERNAME_RECIPIENT_PATH)

    LOCAL_RECIPIENT_PATH = join_path(LOCAL_USERS_PATH, recipient)

    KEY_PATH = join_path(LOCAL_USERNAME_RECIPIENT_PATH, 'key.txt')
    if file_exists(KEY_PATH):
        with open(KEY_PATH, 'rb') as file:
            clave = file.read()
    else:
        GENERAL_RECIPIENT_PATH = join_path(GENERAL_USERS_PATH, recipient)
        try:
            # Intentamos verificar la firma de la clave pública del destinatario
            clave_publica = comprobar.verify_signature(join_path(GENERAL_RECIPIENT_PATH, 'firma_clave_publica.txt'),pk)

            # Si la firma es válida, obtenemos la clave
            GENERAL_RECIPIENT_USERNAME_PATH = join_path(GENERAL_RECIPIENT_PATH, username)
            mkdir(GENERAL_RECIPIENT_USERNAME_PATH)
            clave, c = cifrado.obtener_key_and_c(clave_publica, join_path(GENERAL_RECIPIENT_USERNAME_PATH, 'c.txt'))
            with open(KEY_PATH, 'wb') as file:
                file.write(clave)
        except Exception as e:
            # Si la firma no es válida, generamos nuevas claves y firma
            print("La firma no es válida, generando nuevas claves y firma...")
            clave_publica, clave_privada = claves.generar_claves_kyber()
            
            # Guardar la nueva clave privada
            claves.exportar_clave_privada(clave_privada, join_path(LOCAL_RECIPIENT_PATH, 'clave_privada.txt'))

            # Firmar la nueva clave pública y guardarla
            firma = firmar.firmar_mensaje(sk, clave_publica)
            firmar.guardar_firma(join_path(GENERAL_RECIPIENT_PATH, 'firma_clave_publica.txt'), clave_publica, firma)

            print(e)
            return

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

    print(username)
    print(recipient)

    LOCAL_USERNAME_PATH = join_path(LOCAL_USERS_PATH, username)
    LOCAL_USERNAME_RECIPIENT_PATH = join_path(LOCAL_USERNAME_PATH, recipient)
    KEY_PATH = join_path(LOCAL_USERNAME_RECIPIENT_PATH, 'key.txt')

    try:
        if file_exists(KEY_PATH):
            with open(KEY_PATH, 'rb') as file:
                clave = file.read()
        else:

            GENERAL_USER_PATH = join_path(GENERAL_USERS_PATH, username)
            GENERAL_USER_RECIPIENT_PATH = join_path(GENERAL_USER_PATH, recipient)
            C_PATH = join_path(GENERAL_USER_RECIPIENT_PATH, 'c.txt')

            c = descifrado.obtener_c(C_PATH)
            PK_PATH = join_path(LOCAL_USERNAME_PATH, 'clave_privada.txt')

            clave_privada = descifrado.obtener_clave_privada(PK_PATH)
            clave = descifrado.obtener_clave(clave_privada, c)

            mkdir(LOCAL_USERNAME_RECIPIENT_PATH)
            with open(KEY_PATH, 'wb') as file:
                file.write(clave)
                file.close()

        iv = descifrado.obtener_iv(encrypted_message)
        datos_cifrados = descifrado.obtener_datos_cifrados(encrypted_message)
        message = descifrado.descifrar_datos(clave, iv, datos_cifrados).decode()
        
    except Exception:
        print(Exception)
        message = encrypted_message.hex()

    emit('decrypted_message', {'message': message}, to=request.sid)




if __name__ == '__main__':
    socketio.run(app, debug=True)


