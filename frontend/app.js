let persona = "normale";

function setPersona(value) {
    persona = value;
}

// ENTER INVIO
document.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

async function sendMessage() {

    const input = document.getElementById("input");
    const text = input.value.trim();
    if (!text) return;

    const chat = document.getElementById("chat");

    // USER
    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.innerText = text;
    chat.appendChild(userDiv);

    input.value = "";

    // AI
    const aiDiv = document.createElement("div");
    aiDiv.className = "message ai";
    aiDiv.innerText = "Scrivo...";
    chat.appendChild(aiDiv);

    try {

        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: text,
                persona: persona
            })
        });

        const data = await res.json();
        aiDiv.innerText = data.reply;

    } catch (err) {
        aiDiv.innerText = "Errore connessione server";
    }
}