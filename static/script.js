document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    function appendMessage(message, isUser) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;
        messageDiv.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (text === "") return;

        appendMessage(text, true); // User message
        userInput.value = "";

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            if (response.ok) {
                const data = await response.json();
                appendMessage(data.response, false); // Bot message
            } else {
                appendMessage("Sorry, there was an error.", false);
            }
        } catch (error) {
            appendMessage("Sorry, there was an error.", false);
        }
    }
});
