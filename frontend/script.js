document.addEventListener('DOMContentLoaded', function() {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Add welcome message
    addMessage('AI', 'Hello! I am Lucifer AI. How can I help you today?');

    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);

    // Send message on Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage('You', message);
        userInput.value = '';

        // Show loading indicator
        const loadingElement = addLoadingIndicator();

        // Send to backend
        fetch('/chat/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Remove loading indicator
            if (loadingElement.parentNode) {
                chatHistory.removeChild(loadingElement);
            }
            
            // Add AI response
            addMessage('AI', data.response);
        })
        .catch(error => {
            // Remove loading indicator
            if (loadingElement.parentNode) {
                chatHistory.removeChild(loadingElement);
            }
            
            // Show error message
            addMessage('AI', 'Sorry, I encountered an error. Please try again.');
            console.error('Error:', error);
        });
    }

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender === 'You' ? 'user-message' : 'ai-message'}`;
        
        const senderSpan = document.createElement('div');
        senderSpan.className = 'sender';
        senderSpan.textContent = sender;
        
        const textSpan = document.createElement('div');
        textSpan.className = 'text';
        textSpan.textContent = text;
        
        messageDiv.appendChild(senderSpan);
        messageDiv.appendChild(textSpan);
        
        chatHistory.appendChild(messageDiv);
        
        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function addLoadingIndicator() {
        const loadingElement = document.createElement('div');
        loadingElement.className = 'message ai-message loading';
        loadingElement.innerHTML = '<div class="sender">AI</div><div class="text">Thinking...</div>';
        chatHistory.appendChild(loadingElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return loadingElement;
    }
});
