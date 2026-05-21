let persona = "normale";

// selezione modalità
function setPersona(value) {
    persona = value;
}

// ENTER per inviare
document.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {

    const input = document.getElementById("input");
    const text = input.value.trim();

    if (!text) return;

    const chat = document.getElementById("chat");

    // USER MESSAGE
    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.innerText = text;
    chat.appendChild(userDiv);

    input.value = "";

    // AI MESSAGE
    const aiDiv = document.createElement("div");
    aiDiv.className = "message ai";
    aiDiv.innerText = "Gemini sta scrivendo...";
    chat.appendChild(aiDiv);

    chat.scrollTop = chat.scrollHeight;

    // 🔄 animazione loading
    let dots = 0;
    const loading = setInterval(() => {
        dots = (dots + 1) % 4;
        aiDiv.innerText = "Gemini sta scrivendo" + ".".repeat(dots);
    }, 500);

    try {

        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text,
                persona: persona
            })
        });

        if (!res.ok) {
            throw new Error("HTTP error: " + res.status);
        }

        const data = await res.json();

        clearInterval(loading);
        aiDiv.innerText = data.reply || "Nessuna risposta";

    } catch (err) {

        clearInterval(loading);

        console.log(err);
        aiDiv.innerText = "Errore di connessione al server";

    }

    chat.scrollTop = chat.scrollHeight;
}