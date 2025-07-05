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

function saveToPDF(element) {
    try {
        // Get the HTML content from the message bubble
        const bubble = element.closest('.message').querySelector('.bubble');
        const content = bubble.innerHTML || bubble.textContent || '';
        
        // Create a clean version of the content for PDF
        const cleanContent = cleanContentForPDF(content);
        
        // Create a new window with the content formatted for PDF
        const printWindow = window.open('', '_blank');
        
        const htmlContent = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>AI Solutions Architect Response</title>
                <style>
                    body {
                        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        line-height: 1.6;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        color: #333;
                    }
                    .header {
                        border-bottom: 2px solid #6c7ae0;
                        padding-bottom: 10px;
                        margin-bottom: 20px;
                    }
                    .header h1 {
                        color: #6c7ae0;
                        margin: 0;
                        font-size: 24px;
                    }
                    .timestamp {
                        color: #666;
                        font-size: 14px;
                        margin-top: 5px;
                    }
                    .content {
                        margin: 20px 0;
                    }
                    .content h1, .content h2, .content h3 {
                        color: #4b3cc6;
                        margin-top: 20px;
                        margin-bottom: 10px;
                    }
                    .content h1 { font-size: 20px; }
                    .content h2 { font-size: 18px; }
                    .content h3 { font-size: 16px; }
                    .content p {
                        margin: 10px 0;
                    }
                    .content ul, .content ol {
                        margin: 10px 0;
                        padding-left: 25px;
                    }
                    .content li {
                        margin: 5px 0;
                    }
                    code {
                        background-color: #f5f5f5;
                        padding: 2px 4px;
                        border-radius: 3px;
                        font-family: 'Courier New', monospace;
                        border: 1px solid #ddd;
                        font-size: 90%;
                    }
                    pre {
                        background-color: #f8f9fa;
                        border: 1px solid #e9ecef;
                        border-radius: 4px;
                        padding: 12px;
                        overflow-x: auto;
                        margin: 10px 0;
                    }
                    pre code {
                        background: none;
                        border: none;
                        padding: 0;
                    }
                    strong {
                        color: #2d3748;
                        font-weight: 600;
                    }
                    .footer {
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #e2e8f0;
                        font-size: 12px;
                        color: #666;
                        text-align: center;
                    }
                    @media print {
                        body { margin: 0; }
                        .no-print { display: none; }
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🏗️ AI Solutions Architect Response</h1>
                    <div class="timestamp">Generated on: ${new Date().toLocaleString()}</div>
                </div>
                <div class="content">
                    ${cleanContent}
                </div>
                <div class="footer">
                    Generated by AI Solutions Architect | Cloud Infrastructure Solutions
                </div>
            </body>
            </html>
        `;
        
        printWindow.document.write(htmlContent);
        printWindow.document.close();
        
        // Wait for content to load, then trigger print dialog
        printWindow.onload = function() {
            setTimeout(() => {
                printWindow.print();
                // Close the window after a delay to allow printing
                setTimeout(() => {
                    printWindow.close();
                }, 1000);
            }, 500);
        };
        
        // Show success message
        console.log('PDF download initiated! Use your browser\'s print dialog to save as PDF.');
        
    } catch (error) {
        console.error('Error generating PDF:', error);
        alert('Sorry, there was an error generating the PDF.');
    }
}

function cleanContentForPDF(content) {
    // If content is already HTML (from marked.parse), clean it up for better PDF formatting
    let cleaned = content;
    
    // Handle HTML content from markdown
    if (content.includes('<')) {
        // Clean up any problematic HTML elements for printing
        cleaned = content
            .replace(/<br\s*\/?>/gi, '\n')
            .replace(/<\/p>/gi, '</p>\n')
            .replace(/<\/div>/gi, '</div>\n')
            .replace(/<\/li>/gi, '</li>\n');
    } else {
        // Convert plain text markdown-style formatting to HTML
        cleaned = content
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/\*([^*]+)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');
        
        // Wrap in paragraphs if it's plain text
        cleaned = `<p>${cleaned}</p>`;
    }
    
    return cleaned;
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
            ${isBot ? `<button class="save-pdf-btn" onclick="saveToPDF(this)" title="Save response to PDF">📄 Save PDF</button>` : ''}
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
