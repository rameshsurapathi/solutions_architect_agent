// Card question click event
const cardQuestions = document.querySelectorAll('.card-questions div');
cardQuestions.forEach(q => {
    q.addEventListener('click', () => {
        document.querySelector('.chat-input').value = q.textContent;
        document.querySelector('.chat-input').focus();
    });
});

// Quick action buttons
const quickActions = document.querySelectorAll('.quick-action');
quickActions.forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelector('.chat-input').value = btn.textContent.trim();
        document.querySelector('.chat-input').focus();
    });
});

// Chat send button
const chatForm = document.querySelector('.chat-form');
const chatInput = document.querySelector('.chat-input');
const chatMessages = document.querySelector('.chat-messages');

function cleanBotResponse(text) {
    // Remove repetitive intro lines like 'As a Solutions Architect with over 25 years of experience'
    return text.replace(/As a Solutions Architect with over 25 years of experience[.,]?/gi, '').trim();
}

function getBotAvatar() {
    // SVG avatar for AI agent (modern, professional look)
    return `
    <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="18" cy="18" r="18" fill="#6c7ae0"/>
      <rect x="10" y="14" width="16" height="10" rx="5" fill="#fff"/>
      <ellipse cx="18" cy="13" rx="6" ry="5" fill="#fff"/>
      <ellipse cx="15.5" cy="13.5" rx="1.5" ry="2" fill="#6c7ae0"/>
      <ellipse cx="20.5" cy="13.5" rx="1.5" ry="2" fill="#6c7ae0"/>
      <rect x="15" y="19" width="6" height="2" rx="1" fill="#6c7ae0"/>
    </svg>
    `;
}

function appendMessage(text, isBot = false) {
    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ' + (isBot ? 'bot' : 'user');
    let content = isBot ? cleanBotResponse(text) : text;
    // Convert Markdown to HTML for bot responses
    msgDiv.innerHTML = `
        <div class="avatar">${isBot ? getBotAvatar() : '🧑'}</div>
        <div>
            <div class="bubble">${isBot ? marked.parse(content) : escapeHtml(content)}</div>
            <div class="timestamp">${time}</div>
        </div>
    `;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function sendChatMessage(message) {
    // Show thinking indicator
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message bot thinking';
    thinkingDiv.innerHTML = `
        <div class="avatar">💼</div>
        <div>
            <div class="bubble">Thinking<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></div>
        </div>
    `;
    chatMessages.appendChild(thinkingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Disable input and question selection
    chatInput.disabled = true;
    document.querySelectorAll('.card-questions div, .quick-action, .send-btn').forEach(el => el.disabled = true);

    try {
        const apiUrl = 'https://solutions-architect-agent-948325778469.northamerica-northeast2.run.app/chat';
        
        const res = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        if (!res.ok) {
            throw new Error('Error: ' + res.status);
        }
        const data = await res.json();
        // Remove thinking indicator
        thinkingDiv.remove();
        appendMessage(data.response, true);
    } catch (err) {
        thinkingDiv.remove();
        appendMessage('Sorry, there was an error getting a response from the agent.', true);
    } finally {
        chatInput.disabled = false;
        document.querySelectorAll('.card-questions div, .quick-action, .send-btn').forEach(el => el.disabled = false);
        chatInput.focus();
    }
}

if (chatForm) {
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const value = chatInput.value.trim();
        if (!value) return;
        appendMessage(value, false);
        chatInput.value = '';
        sendChatMessage(value);
    });
}
