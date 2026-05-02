
function addMessage(type, text) {
    let div = document.createElement("div");
    div.className = type;
    div.innerHTML = text;
    document.getElementById("chatbox").appendChild(div);
    div.scrollIntoView({ behavior: "smooth" });
}

async function sendMessage() {
    let input = document.getElementById("userInput");
    let msg = input.value.trim();
    if (!msg) return;

    addMessage("user", "You: " + msg);
    input.value = "";

    let loading = document.createElement("div");
    loading.className = "ai";
    loading.innerHTML = "⏳ Thinking...";
    document.getElementById("chatbox").appendChild(loading);

    try {
        let res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        let data = await res.json();

        loading.remove();
        addMessage("ai", "🤖 " + data.reply);

    } catch (e) {
        loading.remove();
        addMessage("ai", "⚠️ Connection error");
    }
}