// Get room_name from URL query parameter or use 'default'
const params = new URLSearchParams(window.location.search);
const roomName = params.get('room_name') || 'default';

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);
const messages = document.getElementById("chatMessages");
const input = document.getElementById("chatInput");
const button = document.getElementById("sendButton");

chatSocket.onopen = () => {
    document.getElementById(
        "connection-status"
    ).innerText = "Connected";
};

chatSocket.onmessage = (event) => {
    const message = document.createElement("div");
    message.className =
        "d-flex justify-content-end mb-3";
    message.innerHTML = `
        <div class="p-3 text-white bg-gray-400 shadow-sm" style="max-width:75%; border-radius:15px;">
            ${event.data}
        </div>
    `;
    messages.appendChild(message);
    messages.scrollTop =
        messages.scrollHeight;
};

chatSocket.onerror = (e) => {
    console.error('WebSocket error:', e);
};

chatSocket.onclose = function(e) {
    document.getElementById(
        "connection-status"
    ).innerText = "Disconnected";
    console.error('Chat socket closed unexpectedly');
};

button.onclick = sendMessage;
input.addEventListener(
    "keypress",
    (e) => {
        if (e.key === "Enter")
            sendMessage();
    }
);

// Send message to server
function sendMessage() {
    const text = input.value;
    if (!text.trim())
        return;
    chatSocket.send(text);
    input.value = "";
}
