function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute("content");
}

function askAssistant(taskId) {
    const modal = document.getElementById(`assistant-modal-${taskId}`);
    const responseBox = document.getElementById(`assistant-response-${taskId}`);
    modal.classList.add("is-active");
    responseBox.innerText = "🤔 Thinking...";
  
    fetch(`/task/${taskId}/assistant`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken()
      },
      body: JSON.stringify({}) 
    })
      .then(res => res.json())
      .then(data => {
        if (data.question) {
          responseBox.innerText = data.question;
        } else {
          responseBox.innerText = data.error || "Something went wrong.";
        }
      })
      .catch(() => {
        responseBox.innerText = "Request failed.";
      });
  }

  function closeAssistantModal(taskId) {
    document.getElementById(`assistant-modal-${taskId}`).classList.remove("is-active");
  }
  
  function saveAssistantResponse(taskId) {
    const input = document.getElementById(`assistant-input-${taskId}`).value;
  
    fetch(`/task/${taskId}/update-description`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ description: input })
    }).then(res => {
      if (res.ok) {
        location.reload();
      } else {
        alert("Failed to update.");
      }
    });
  }
  
  function sendAssistantReply(taskId) {
    const input = document.getElementById(`assistant-input-${taskId}`);
    const button = document.querySelector(`#assistant-modal-${taskId} .button.is-primary`);
    const modal = document.getElementById(`assistant-modal-${taskId}`);
    const responseEl = document.getElementById(`assistant-response-${taskId}`);
  
    const userMessage = input.value.trim();
    if (!userMessage) return;
  
    // Show loader state
    button.classList.add("is-loading");
    responseEl.textContent = "Thinking...";
  
    fetch(`/task/${taskId}/assistant/reply`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken()
      },
      body: JSON.stringify({ message: userMessage }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.reply) {
          responseEl.textContent = `Assistant: ${data.reply}`;
          input.value = ""; 
        } else {
          responseEl.textContent = "Something went wrong.";
        }
      })
      .catch(() => {
        responseEl.textContent = "Error connecting to assistant.";
      })
      .finally(() => {
        button.classList.remove("is-loading");
      });
  }

  function toggleAssistantNote(taskId) {
  const noteDiv = document.getElementById(`assistant-note-${taskId}`);
  noteDiv.classList.toggle("is-hidden");
}