const menuItems = document.querySelectorAll('.nav-item');

menuItems.forEach(item => {
    item.addEventListener('click', function () {
        menuItems.forEach(el => el.classList.remove('active'));
        this.classList.add('active');
    });
});

const chatbot = document.querySelector('.chatbot-icon');
const chatContainer = document.getElementById("chat-container");
const chatbox = document.getElementById("chatbox");

chatbot.addEventListener('click', () => {
    chatContainer.style.display =
        chatContainer.style.display === "none" ? "flex" : "none";
});

async function sendMessage() {
    const input = document.getElementById("userInput");
    const userText = input.value;

    if (!userText) return;

    // show user message
    chatbox.innerHTML += `<div class="user">You: ${userText}</div>`;

    // call backend
    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: userText })
    });

    const data = await response.json();

    // show bot reply
    chatbox.innerHTML += `<div class="bot">Bot: ${data.reply}</div>`;

    input.value = "";
    chatbox.scrollTop = chatbox.scrollHeight;
    loadBookings();
}

async function loadBookings() {
    const response = await fetch("http://127.0.0.1:8000/bookings");
    const data = await response.json();

    const tableBody = document.querySelector("#bookingTable tbody");
    tableBody.innerHTML = "";

    for (let id in data) {
        const booking = data[id];

        const row = `
            <tr>
                <td>${id}</td>
                <td>${booking.destination}</td>
                <td>${booking.month}</td>
                <td>${booking.day}</td>
            </tr>
        `;

        tableBody.innerHTML += row;
    }
}
window.onload = loadBookings;