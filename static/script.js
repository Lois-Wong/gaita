function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const messageText = chatInput.value.trim();

    if (messageText) {
        addChatMessage(messageText, 'user');
        chatInput.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: messageText }),
        })
        .then(response => response.json())
        .then(data => {
            let responseText = data.response;
            // Convert markdown-like syntax to HTML
            addChatMessage(responseText, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            addChatMessage("Sorry, something went wrong." + " " + error, 'bot');
        });
    }
}

function addChatMessage(text, sender) {
    const chatBody = document.getElementById('chatBody');

    const messageContainer = document.createElement('div');
    messageContainer.classList.add('chatMessage', sender === 'user' ? 'userMessage' : 'botMessage');

    const messageText = document.createElement('div');
    messageText.classList.add('messageText');
    messageText.innerHTML = text;

    messageContainer.appendChild(messageText);
    chatBody.appendChild(messageContainer);

    chatBody.scrollTop = chatBody.scrollHeight;
}