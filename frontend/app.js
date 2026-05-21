async function sendMessage() {
    const input = document.getElementById("message");
    const chat = document.getElementById("chat");

    const text = input.value;
    if (!text) return;

    // mostra messaggio utente
    chat.innerHTML += `<div class="user">${text}</div>`;

    input.value = "";

    // 👇 SOLO "sta scrivendo"
    const typing = document.createElement("div");
    typing.className = "bot";
    typing.id = "typing";
    typing.innerText = "sta scrivendo...";
    chat.appendChild(typing);

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text,
                persona: "pirandello"
            })
        });

        const data = await res.json();

        // rimuove typing
        document.getElementById("typing").remove();

        chat.innerHTML += `<div class="bot">${data.reply}</div>`;

    } catch (err) {
        document.getElementById("typing").remove();
        chat.innerHTML += `<div class="bot">Errore di connessione</div>`;
    }
}