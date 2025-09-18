let recognition;
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const transcriptBox = document.getElementById("transcript");
const hindiBox = document.getElementById("hindiTranslation");
const spanishBox = document.getElementById("spanishTranslation");
const speakBtn = document.getElementById("speakBtn");

startBtn.onclick = () => {
    recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US"; // you can change to auto detect if needed
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onresult = async (event) => {
        const transcript = event.results[0][0].transcript;
        transcriptBox.value = transcript;
        await sendToBackend(transcript);
    };

    recognition.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
};

stopBtn.onclick = () => {
    if (recognition) recognition.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
};

async function sendToBackend(text) {
    hindiBox.value = "Translating...";
    spanishBox.value = "Translating...";
    speakBtn.disabled = true;

    try {
        const response = await fetch("/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        hindiBox.value = data.hindi || "No Hindi result";
        spanishBox.value = data.spanish || "No Spanish result";
        speakBtn.disabled = false;
    } catch (error) {
        hindiBox.value = "Error: " + error.message;
        spanishBox.value = "Error: " + error.message;
    }
}

speakBtn.onclick = () => {
    if (hindiBox.value) {
        const hiVoice = new SpeechSynthesisUtterance(hindiBox.value);
        hiVoice.lang = "hi-IN";
        speechSynthesis.speak(hiVoice);
    }
    if (spanishBox.value) {
        const esVoice = new SpeechSynthesisUtterance(spanishBox.value);
        esVoice.lang = "es-ES";
        speechSynthesis.speak(esVoice);
    }
};
