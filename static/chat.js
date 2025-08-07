document.addEventListener('DOMContentLoaded', () => {
  const chatWindow = document.getElementById('chat-window');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-button');


  const API_URL = '/api/chat';

  const systemMsg = {
    role: "user",
    parts: [{ text: "You are an expert agricultural assistant named AgriBot. Provide detailed, accurate and helpful responses about farming, crops, weather impact, soil health, pest control, and sustainable agriculture practices. Format your answers with clear concise minimal paragraphs. If asked about something outside agriculture except greetings, politely decline and refocus on farming topics." }]
  };
  let history = [systemMsg];

  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('suggestion')) {
      chatInput.value = e.target.textContent;
      chatForm.dispatchEvent(new Event('submit'));
    }
  });

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = chatInput.value.trim();
    if (!input) return;

    addMessage('user', input);
    chatInput.value = '';
    const typing = showTyping();
    toggleInput(true);
    history.push({ role: "user", parts: [{ text: input }] });

    try {
      // This fetch call now goes to  Flask api endpoint ('/api/chat')
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: history,
          generationConfig: {
            temperature: 0.7,
            maxOutputTokens: 1000,
            topP: 0.8,
            topK: 40
          }
        })
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      console.log('API Response:', data);

      const reply = data?.candidates?.[0]?.content?.parts?.[0]?.text || "⚠️ I didn't receive a proper response. Please try again.";
      addMessage('bot', reply);
      history.push({ role: "model", parts: [{ text: reply }] });
    } catch (error) {
      console.error('Error:', error);
      addMessage('bot', "⚠️ I'm having trouble connecting right now. Please check your internet connection and try again.");
    } finally {
      typing.remove();
      toggleInput(false);
    }
  });

  const addMessage = (who, txt) => {
    const div = document.createElement('div');
    div.className = `message ${who}`;
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const name = who === 'user' ? 'You' : 'AgriBot';
    div.innerHTML = `
      <div class="message-header"><i class="fas fa-${who === 'user' ? 'user' : 'robot'}"></i> ${name}</div>
      <div class="message-text">${format(txt)}</div>
      <div class="timestamp">${time}</div>
    `;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  };

  const showTyping = () => {
    const typing = document.createElement('div');
    typing.className = 'typing-indicator';
    typing.innerHTML = `<div>AgriBot is typing</div><span></span><span></span><span></span>`;
    chatWindow.appendChild(typing);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return typing;
  };

  const toggleInput = (disable) => {
    sendBtn.disabled = disable;
    chatInput.disabled = disable;
    if (!disable) chatInput.focus();
  };

  const format = (txt) =>
    txt.replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>');

  setTimeout(() => {
    addMessage('bot', 'Hello! 🌱 I\'m AgriBot, your agricultural assistant. I can help you with farming questions, crop management, soil health, pest control, and more. How can I assist you today?');
  }, 500);

  chatInput.focus();
});