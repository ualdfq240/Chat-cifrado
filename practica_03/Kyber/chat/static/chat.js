document.addEventListener("DOMContentLoaded", () => {
    const socket = io();
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");
    const chatBox = document.getElementById("chat-box");
    const showUsersBtn = document.getElementById("show-users-btn");
    const userSelect = document.getElementById("user-select");

    showUsersBtn.addEventListener("click", () => {
        socket.emit("request_users");
    });

    socket.on("user_list", (users) => {
        userSelect.innerHTML = ''; // Limpiar las opciones
        users.forEach(user => {
            const option = document.createElement("option");
            option.value = user;
            option.textContent = user;
            userSelect.appendChild(option);
        });
    });
    

    messageForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const message = messageInput.value;
        const recipient = userSelect.value;
        if (message) {
            socket.emit("message", { message, recipient });
            messageInput.value = "";
        }
    });

    socket.on("message", (data) => {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message");

        messageElement.innerHTML = `
        <strong>${data.username}➔${data.recipient || 'todos'}:</strong>
        <button class="show-message-btn">Mostrar mensaje</button>
        <div class="message-content" style="display: none;" data-message="${data.message}"></div>
        `;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;

        const showMessageBtn = messageElement.querySelector(".show-message-btn");
        showMessageBtn.addEventListener("click", () => {
        const messageContent = messageElement.querySelector(".message-content");
        if (messageContent.style.display === "none") {
            // Enviar el objeto data completo en lugar de solo el mensaje
            socket.emit("decrypt_message", data.username, data.message);
        } else {
            messageContent.style.display = "none";
            showMessageBtn.textContent = "Mostrar mensaje";
        }
        });

    });

    socket.on("decrypted_message", (decryptedMessage) => {
        const messageContent = document.querySelector(".message-content[data-message]");
        if (messageContent) {
            messageContent.textContent = decryptedMessage.message;
            messageContent.style.display = "block";
            const showMessageBtn = messageContent.previousElementSibling;
            showMessageBtn.textContent = "Ocultar mensaje";
        }
    });
});