with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

chat_widget = '''
<style>
#chatWidget{position:fixed;bottom:24px;right:24px;z-index:999;font-family:var(--font-body);}
#chatToggleBtn{width:58px;height:58px;border-radius:50%;border:none;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;font-size:24px;cursor:pointer;box-shadow:0 0 20px rgba(168,85,247,.5);display:flex;align-items:center;justify-content:center;animation:chatPulse 2.4s infinite;position:relative;}
@keyframes chatPulse{0%,100%{box-shadow:0 0 15px rgba(168,85,247,.4);}50%{box-shadow:0 0 28px rgba(6,182,212,.6);}}
#chatUnreadBadge{position:absolute;top:-4px;right:-4px;background:var(--danger);color:#fff;font-size:11px;font-weight:700;min-width:20px;height:20px;border-radius:10px;display:none;align-items:center;justify-content:center;padding:0 5px;}
#chatBox{width:340px;height:460px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);position:absolute;bottom:74px;right:0;display:flex;overflow:hidden;box-shadow:var(--shadow-md);animation:modalIn .25s cubic-bezier(.2,.8,.2,1) both;}
#chatBox.hidden{display:none!important;}
#chatContactsPanel{width:120px;background:var(--surface-alt);border-right:1px solid var(--border);overflow-y:auto;flex-shrink:0;}
.chat-contact{padding:10px 8px;font-size:12px;font-weight:600;color:var(--text-muted);cursor:pointer;border-bottom:1px solid var(--border);text-align:center;transition:.2s;}
.chat-contact:hover,.chat-contact.active{background:var(--primary);color:#fff;}
#chatMainPanel{flex:1;display:flex;flex-direction:column;min-width:0;}
#chatHeader{background:linear-gradient(90deg,var(--primary),var(--accent));color:#fff;padding:12px 14px;font-weight:600;font-size:13.5px;display:flex;justify-content:space-between;align-items:center;}
#chatCloseBtn{background:none;border:none;color:#fff;font-size:18px;cursor:pointer;opacity:.85;}
#chatMessages{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:6px;}
.msg-bubble{padding:7px 11px;border-radius:12px;font-size:12.5px;max-width:80%;line-height:1.4;word-wrap:break-word;}
.msg-sent{background:linear-gradient(135deg,var(--primary),var(--primary-light));color:#fff;align-self:flex-end;border-bottom-right-radius:3px;}
.msg-received{background:var(--surface-alt);color:var(--text);align-self:flex-start;border-bottom-left-radius:3px;}
.msg-empty{color:var(--text-muted);font-size:12px;text-align:center;margin-top:20px;}
#chatInputArea{display:flex;padding:8px;border-top:1px solid var(--border);gap:6px;}
#chatInput{flex:1;background:var(--bg);border:1px solid var(--border);color:var(--text);padding:8px 10px;border-radius:8px;font-size:12.5px;outline:none;}
#chatInput:focus{border-color:var(--primary);}
#chatSendBtn{background:linear-gradient(135deg,var(--primary),var(--accent));border:none;color:#fff;width:34px;height:34px;border-radius:8px;cursor:pointer;font-size:14px;}
#chatSelectPrompt{flex:1;display:flex;align-items:center;justify-content:center;color:var(--text-muted);font-size:12px;text-align:center;padding:20px;}
</style>

<div id="chatWidget">
  <button id="chatToggleBtn">💬<span id="chatUnreadBadge">0</span></button>
  <div id="chatBox" class="hidden">
    <div id="chatContactsPanel"></div>
    <div id="chatMainPanel">
      <div id="chatHeader"><span id="chatHeaderName">Select a contact</span><button id="chatCloseBtn">✕</button></div>
      <div id="chatMessages"><div class="msg-empty">Select someone to start chatting</div></div>
      <div id="chatInputArea" style="display:none;">
        <input type="text" id="chatInput" placeholder="Type a message...">
        <button id="chatSendBtn">➤</button>
      </div>
    </div>
  </div>
</div>

<script>
(function(){
  let chatActiveContact = null;
  let chatPollInterval = null;

  async function chatFetchContacts(){
    const res = await fetch('/chat/contacts');
    const contacts = await res.json();
    const panel = document.getElementById('chatContactsPanel');
    panel.innerHTML = '';
    contacts.forEach(c => {
      const div = document.createElement('div');
      div.className = 'chat-contact';
      div.textContent = c.username;
      div.onclick = () => chatSelectContact(c.id, c.username);
      panel.appendChild(div);
    });
  }

  function chatSelectContact(id, name){
    chatActiveContact = id;
    document.querySelectorAll('.chat-contact').forEach(el => el.classList.remove('active'));
    [...document.querySelectorAll('.chat-contact')].find(el => el.textContent === name)?.classList.add('active');
    document.getElementById('chatHeaderName').textContent = name;
    document.getElementById('chatInputArea').style.display = 'flex';
    chatLoadHistory();
  }

  async function chatLoadHistory(){
    if(!chatActiveContact) return;
    const res = await fetch(`/chat/history/${chatActiveContact}`);
    const msgs = await res.json();
    const box = document.getElementById('chatMessages');
    if(msgs.length === 0){
      box.innerHTML = '<div class="msg-empty">No messages yet. Say hi!</div>';
      return;
    }
    box.innerHTML = '';
    msgs.forEach(m => chatAppendMsg(m.message, m.sender_id !== chatActiveContact));
    box.scrollTop = box.scrollHeight;
    chatUpdateUnread();
  }

  function chatAppendMsg(text, isSent){
    const box = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = 'msg-bubble ' + (isSent ? 'msg-sent' : 'msg-received');
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  async function chatSend(){
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if(!text || !chatActiveContact) return;
    await fetch('/chat/send', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({receiver_id: chatActiveContact, message: text})
    });
    chatAppendMsg(text, true);
    input.value = '';
  }

  async function chatUpdateUnread(){
    const res = await fetch('/chat/unread-count');
    const data = await res.json();
    const badge = document.getElementById('chatUnreadBadge');
    if(data.unread > 0){
      badge.textContent = data.unread;
      badge.style.display = 'flex';
    } else {
      badge.style.display = 'none';
    }
  }

  document.getElementById('chatToggleBtn').addEventListener('click', () => {
    const box = document.getElementById('chatBox');
    box.classList.toggle('hidden');
    if(!box.classList.contains('hidden')){
      chatFetchContacts();
      if(!chatPollInterval) chatPollInterval = setInterval(chatLoadHistory, 3000);
    }
  });
  document.getElementById('chatCloseBtn').addEventListener('click', () => {
    document.getElementById('chatBox').classList.add('hidden');
  });
  document.getElementById('chatSendBtn').addEventListener('click', chatSend);
  document.getElementById('chatInput').addEventListener('keypress', e => {
    if(e.key === 'Enter') chatSend();
  });

  setInterval(chatUpdateUnread, 5000);
})();
</script>
'''

marker = "</body>"
if marker in content:
    content = content.replace(marker, chat_widget + "\\n" + marker)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Chat widget added successfully")
else:
    print("❌ </body> marker not found")
