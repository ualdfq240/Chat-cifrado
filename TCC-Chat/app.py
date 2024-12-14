from cifrados import cifrado, descifrado, claves, claves_DSA, firmar, comprobar
import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, send, emit
from cryptography.hazmat.primitives.asymmetric import padding

app = Flask(__name__)
app.secret_key = "secret_key"
socketio = SocketIO(app)

mkdir = lambda path: os.makedirs(path, exist_ok=True) 
file_exists = lambda path: os.path.exists(path) 
join_path = lambda *args: os.path.join(*args)
delete_dir = lambda path: shutil.rmtree(path) if os.path.exists(path) else None



BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GENERAL_CHATS_PATH = join_path(BASE_PATH, "general/chats")
GENERAL_USERS_PATH = join_path(BASE_PATH, "general/users")
LOCAL_USERS_PATH = join_path(BASE_PATH, "local/users")

# Crear directorios generales si no existen
mkdir(GENERAL_USERS_PATH)
mkdir(LOCAL_USERS_PATH)

sk, pk = claves_DSA.generar_claves_dsa()

users = {}
connected_users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']  # Obtener la contraseña
    if username and password:
        if username not in users:
            # Registrar usuario nuevo
            users[username] = password
            session['username'] = username

            GENERAL_USER_PATH = join_path(GENERAL_USERS_PATH, username)
            LOCAL_USER_PATH = join_path(LOCAL_USERS_PATH, username)
            mkdir(GENERAL_USER_PATH)
            mkdir(LOCAL_USER_PATH)

            # Generar y exportar claves
            clave_publica, clave_privada = claves.generar_claves_kyber()

            # Cifrar la clave privada de Kyber
            cifrar_local(username, clave_privada, 'clave_privada.txt')

            # Firmar la clave pública de Kyber usando la clave privada del servidor
            firma = firmar_mensaje(clave_publica)
            firmar.guardar_firma(join_path(GENERAL_USER_PATH, 'firma_clave_publica.txt'), clave_publica, firma)

            return redirect(url_for('chat', username=username))
        elif users[username] == password:
            # Validar si la contraseña coincide
            session['username'] = username
            return redirect(url_for('chat', username=username))
        else:
            return 'Contraseña incorrecta.'
    return 'El nombre de usuario o contraseña no son válidos.'

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


# Cifrar y mandar mensaje
@socketio.on('message')
def handle_message(data):
    username = session.get('username')
    recipient = data.get('recipient')
    message = data['message'].encode()
    tipo = None
    if recipient != "todos":
        LOCAL_USERNAME_PATH = join_path(LOCAL_USERS_PATH, username)
        LOCAL_USERNAME_RECIPIENT_PATH = join_path(LOCAL_USERNAME_PATH, recipient)
        mkdir(LOCAL_USERNAME_RECIPIENT_PATH)

        LOCAL_RECIPIENT_PATH = join_path(LOCAL_USERS_PATH, recipient)

        KEY_PATH = join_path(LOCAL_USERNAME_RECIPIENT_PATH, 'key.txt')
        if file_exists(KEY_PATH):
            clave = descifrar_local(username, KEY_PATH)
        else:
            GENERAL_RECIPIENT_PATH = join_path(GENERAL_USERS_PATH, recipient)
            try:
                # Verificar la firma de la clave pública del destinatario
                clave_publica = verificar_firma(join_path(GENERAL_RECIPIENT_PATH, 'firma_clave_publica.txt'), "clave_publica")

                # Si la firma es válida, obtener la clave
                GENERAL_RECIPIENT_USERNAME_PATH = join_path(GENERAL_RECIPIENT_PATH, username)
                mkdir(GENERAL_RECIPIENT_USERNAME_PATH)
                clave, c = cifrado.obtener_key_and_c(clave_publica,sk, join_path(GENERAL_RECIPIENT_USERNAME_PATH, 'firma_c.txt'))
                cifrar_local(username, clave, KEY_PATH)
            except Exception as e:
                # Generar nuevas claves y firma si la verificación falla
                clave_publica, clave_privada = claves.generar_claves_kyber()

                # Guardar la nueva clave privada
                clave_contraseña = cifrado.obtener_32_bytes(users[recipient])
                iv = cifrado.obtener_iv()
                clave_privada_cifrada = cifrado.cifrar_datos(clave_contraseña, iv, clave_privada)
                cifrado.escribir_datos(iv, clave_privada_cifrada, join_path(LOCAL_RECIPIENT_PATH, 'clave_privada.txt'))

                # Firmar la nueva clave pública y guardarla
                firma = firmar_mensaje(clave_publica)
                firmar.guardar_firma(join_path(GENERAL_RECIPIENT_PATH, 'firma_clave_publica.txt'), clave_publica, firma)

                print(e)
                socketio.emit("alert_message", {"message": "La firma de la clave publica no es válida, generando nuevas claves y firma..."})
                return

        iv = cifrado.obtener_iv()
        mensaje_cifrado = cifrado.cifrar_datos(clave, iv, message)
        message_crypto = iv + mensaje_cifrado
    else:
        message_crypto = message.decode()
        tipo = 'general'
    
    

    padding_Size, message_crypto = standar_bytes(message_crypto)
    
    firma = firmar_mensaje(message_crypto)
    certificado = message_crypto
    certificado += firma

    send({
        'username': username,
        'recipient': recipient,
        'message': certificado,
        'tipo' : tipo,
        'padding_Size' : padding_Size
    }, broadcast=True)



@socketio.on('decrypt_message')
def handle_decrypt_message(recipient, certificado, tipo, padding_Size):
    username = session.get('username')
    encrypted_message = verificar_firma(None, 'mensaje', padding_Size=padding_Size, mensaje=certificado)
    if tipo != "general":
        LOCAL_USERNAME_PATH = join_path(LOCAL_USERS_PATH, username)
        LOCAL_USERNAME_RECIPIENT_PATH = join_path(LOCAL_USERNAME_PATH, recipient)
        KEY_PATH = join_path(LOCAL_USERNAME_RECIPIENT_PATH, 'key.txt')
        fallo_Firma = True
        GENERAL_USER_PATH = join_path(GENERAL_USERS_PATH, username)
        GENERAL_USER_RECIPIENT_PATH = join_path(GENERAL_USER_PATH, recipient)
        LOCAL_RECIPIENT_PATH = join_path(LOCAL_USERS_PATH, recipient)
        LOCAL_RECIPIENT_USER_PATH = join_path(LOCAL_RECIPIENT_PATH, username)
       
        try:
            if file_exists(KEY_PATH):
                clave = descifrar_local(username, KEY_PATH)
            else:
                C_PATH = join_path(GENERAL_USER_RECIPIENT_PATH, 'firma_c.txt')

                
                
                c = verificar_firma(C_PATH, "c")
                PK_PATH = join_path(LOCAL_USERNAME_PATH, 'clave_privada.txt')
                fallo_Firma = False
                clave_privada = descifrar_local(username, PK_PATH)
                clave = descifrado.obtener_clave(clave_privada, c)

                mkdir(LOCAL_USERNAME_RECIPIENT_PATH)
                cifrar_local(username, clave, KEY_PATH)

                delete_dir(GENERAL_USER_RECIPIENT_PATH)
            iv = descifrado.obtener_iv(encrypted_message)
            datos_cifrados = descifrado.obtener_datos_cifrados(encrypted_message)
            message = descifrado.descifrar_datos(clave, iv, datos_cifrados).decode()
            
        except Exception:
            if fallo_Firma:
                delete_dir(GENERAL_USER_RECIPIENT_PATH)

                delete_dir(LOCAL_RECIPIENT_USER_PATH)
                socketio.emit("alert_message", {"message": "La firma de c ha sido inválida, solicite el mensaje de nuevo"})
                
            print(Exception)
            message = encrypted_message.hex()
    else:
        message = encrypted_message.decode('utf-8')
    

    emit('decrypted_message', {'message': message}, to=request.sid)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Rutas de directorios a eliminar
    paths_to_delete = [join_path(BASE_PATH, 'local'), join_path(BASE_PATH, 'general')] 


    try:
        # Eliminar directorios si existen
        for path in paths_to_delete:
            if os.path.exists(path):
                shutil.rmtree(path)
        # Finalizar la aplicación
        func = request.environ.get('werkzeug.server.shutdown')
        if func:
            func()
        return jsonify({"message": "El servidor se cerró correctamente y los archivos fueron eliminados."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def cifrar_local(user, dato, archivo):
    LOCAL_USER_PATH = join_path(LOCAL_USERS_PATH, user)
    clave_contraseña = cifrado.obtener_32_bytes(users[user])
    iv = cifrado.obtener_iv()
    #Cifrar la clave privada de kyber usando la clave AES del usuario
    dato_cifrado = cifrado.cifrar_datos(clave_contraseña, iv, dato)
    cifrado.escribir_datos(iv, dato_cifrado, join_path(LOCAL_USER_PATH, archivo))

def descifrar_local(user, archivo):

    iv_and_datos_cifrados = descifrado.obtener_datos(archivo)
    iv = descifrado.obtener_iv(iv_and_datos_cifrados)
    dato_cifrado = descifrado.obtener_datos_cifrados(iv_and_datos_cifrados)
    clave_contraseña = cifrado.obtener_32_bytes(users[user])
    dato = descifrado.descifrar_datos(clave_contraseña, iv, dato_cifrado)
    return dato

# Método para firmar un mensaje
def firmar_mensaje(mensaje):
    try:
        firma = firmar.firmar_mensaje(sk, mensaje)
        return firma
    except Exception as e:
        print(f"Error al firmar el mensaje: {e}")
        raise

# Método para verificar una firma
def verificar_firma(ruta_firma, tipo, padding_Size = None, mensaje= None):
    try:
        if tipo == 'mensaje':
            dato = comprobar.verify_signature(pk, tipo, padding_Size=padding_Size, texto=mensaje)
        else:
            dato = comprobar.verify_signature(pk, tipo, file_path=ruta_firma)
        return dato
    except Exception as e:
        print(f"Error al verificar la firma: {e}")
        raise
    

def standar_bytes(mensaje):
    if isinstance(mensaje, str):
        mensaje = mensaje.encode('utf-8')  # Codifica si es una cadena de texto
    if len(mensaje) < 1000:
        padding_size = 1000 - len(mensaje)
        # Rellenar con padding (puedes elegir el tipo de padding que prefieras)
        mensaje += b'\0' * padding_size

    return padding_size, mensaje

if __name__ == '__main__':
    socketio.run(app, debug=True)