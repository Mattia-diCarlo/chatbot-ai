function toggleTheme() {
    if (document.body.classList.contains("dark")) {
        document.body.classList.remove("dark");
        document.body.classList.add("light");
    } else {
        document.body.classList.remove("light");
        document.body.classList.add("dark");
    }
}

document.body.classList.add("light");

async function sendMessage() {
    const input = document.getElementById("message");
    const chat = document.getElementById("chat");

    const text = input.value;
    if (!text) return;

    chat.innerHTML += `<div class="user">${text}</div>`;
    input.value = "";

    // typing
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

        document.getElementById("typing").remove();
        chat.innerHTML += `<div class="bot">${data.reply}</div>`;

    } catch (err) {
        document.getElementById("typing").remove();
        chat.innerHTML += `<div class="bot">Errore di connessione</div>`;
    }
}