const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const tabButtons = document.querySelectorAll(".tab-btn");
const sendButton = chatForm.querySelector("button[type='submit']");

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `msg ${type}`;
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function typeBotMessage(text) {
  const div = document.createElement("div");
  div.className = "msg bot";
  chatWindow.appendChild(div);

  const parts = text.split(/(\s+)/).filter(Boolean);

  for (const part of parts) {
    div.textContent += part;
    chatWindow.scrollTop = chatWindow.scrollHeight;
    await sleep(/\s+/.test(part) ? 0 : 45);
  }
}

function addTypingIndicator() {
  const div = document.createElement("div");
  div.className = "msg bot typing";
  div.setAttribute("data-typing", "true");
  div.innerHTML = [
    "<span class=\"typing-dot\"></span>",
    "<span class=\"typing-dot\"></span>",
    "<span class=\"typing-dot\"></span>",
  ].join("");
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}

async function sendMessage(message, { renderUser = true } = {}) {
  const trimmed = message.trim();
  if (!trimmed) return;

  if (renderUser) {
    addMessage(trimmed, "user");
  }

  sendButton.disabled = true;
  const typingIndicator = addTypingIndicator();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: trimmed, sender: "web_user" }),
    });

    const data = await response.json();
    typingIndicator.remove();
    await typeBotMessage(data.reply || "No response.");
  } catch (error) {
    typingIndicator.remove();
    await typeBotMessage("Network error while connecting to chatbot service.");
  } finally {
    sendButton.disabled = false;
  }
}

function setActiveTab(clicked) {
  tabButtons.forEach((btn) => {
    btn.classList.toggle("active", btn === clicked);
  });
}

addMessage("Welcome. Select a category on the left to instantly get a quote.", "bot");

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value;
  messageInput.value = "";
  await sendMessage(message, { renderUser: true });
});

tabButtons.forEach((btn) => {
  btn.addEventListener("click", async () => {
    setActiveTab(btn);
    const prompt = btn.dataset.prompt || btn.textContent;
    await sendMessage(prompt, { renderUser: true });
  });
});
