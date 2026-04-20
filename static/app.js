const transcriptEl = document.getElementById("transcript");
const outputEl = document.getElementById("output");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

function speak(text) {
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 1;
  window.speechSynthesis.speak(utter);
}

async function dispatchCommand(commandText) {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  const response = await fetch("/api/command", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command: commandText, email, password })
  });

  const data = await response.json();
  outputEl.textContent = data.response;
  speak(data.response);
}

if (!recognition) {
  outputEl.textContent = "Speech recognition is not supported in this browser.";
} else {
  recognition.lang = "en-US";
  recognition.interimResults = false;

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    transcriptEl.textContent = text;
    dispatchCommand(text).catch((error) => {
      outputEl.textContent = `Error: ${error.message}`;
      speak(outputEl.textContent);
    });
  };

  recognition.onerror = (event) => {
    outputEl.textContent = `Speech error: ${event.error}`;
    speak(outputEl.textContent);
  };

  startBtn.addEventListener("click", () => recognition.start());
  stopBtn.addEventListener("click", () => recognition.stop());
}
