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
  return div;
}

function addActionButtons(container, buttons) {
  const actions = document.createElement("div");
  actions.className = "feedback-row";

  buttons.forEach((item) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "feedback-btn";
    button.textContent = item.label;
    button.addEventListener("click", async () => {
      Array.from(actions.querySelectorAll("button")).forEach((btn) => {
        btn.disabled = true;
      });
      await sendMessage(item.message, { renderUser: false });
    });
    actions.appendChild(button);
  });

  container.appendChild(actions);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addFeedbackButtons(container) {
  addActionButtons(container, [
    { label: "Helpful", message: "yes" },
    { label: "Not helpful", message: "no" },
  ]);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function typeBotMessage(text, options = {}) {
  const div = document.createElement("div");
  div.className = "msg bot";
  chatWindow.appendChild(div);

  const parts = text.split(/(\s+)/).filter(Boolean);

  for (const part of parts) {
    div.textContent += part;
    chatWindow.scrollTop = chatWindow.scrollHeight;
    await sleep(/\s+/.test(part) ? 0 : 45);
  }

  if (options.showFeedback) {
    addFeedbackButtons(div);
  }

  if (options.quickReplies?.length) {
    addActionButtons(div, options.quickReplies);
  }
}

function addTypingIndicator() {
  const div = document.createElement("div");
  div.className = "msg bot typing";
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
    await typeBotMessage(data.reply || "No response.", {
      showFeedback: Boolean(data.show_feedback),
      quickReplies: data.quick_replies || [],
    });
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

addMessage("Hi there. I hope your day is going gently so far. Pick a category on the left or type what you need, and I will find a quote for you.", "bot");

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
