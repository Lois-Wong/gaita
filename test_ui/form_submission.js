// Load the JSON file and store the data
let courses = [];

fetch('courses.json')
    .then(response => response.json())
    .then(data => {
        courses = data;
        console.log("Courses loaded:", courses);
    })
    .catch(error => console.error("Error loading JSON:", error));

function searchCourses(query) {
    query = query.toLowerCase();
    return courses.filter(course =>
        course.title.toLowerCase().includes(query) ||
        course.description.toLowerCase().includes(query)
    );
}

function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const messageText = chatInput.value.trim();

    if (messageText) {
        addChatMessage(messageText, 'user');
        chatInput.value = '';

        const results = searchCourses(messageText);
        if (results.length > 0) {
            results.forEach(course => {
                const responseText = `Course: ${course.title}<br>Description: ${course.description}`;
                addChatMessage(responseText, 'bot');
            });
        } else {
            addChatMessage("Sorry, I couldn't find any courses matching your query.", 'bot');
        }
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
