let recognition;
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const transcriptBox = document.getElementById("transcript");
const hindiBox = document.getElementById("hindiTranslation");
const spanishBox = document.getElementById("spanishTranslation");
const speakBtn = document.getElementById("speakBtn");
const transcriptStatus = document.getElementById("transcriptStatus");
const hindiStatus = document.getElementById("hindiStatus");
const spanishStatus = document.getElementById("spanishStatus");

function updateStatus(element, status) {
    element.className = `status-indicator status-${status}`;
}

startBtn.onclick = () => {
    recognition = new webkitSpeechRecognition();
    recognition.lang = "auto";
    recognition.interimResults = false;
    recognition.continuous = true;

    recognition.onstart = () => {
        updateStatus(transcriptStatus, 'listening');
        transcriptBox.placeholder = "Listening... Please speak now";
    };

    recognition.onresult = async (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript;
        transcriptBox.value = transcript;
        updateStatus(transcriptStatus, 'ready');
        await sendToBackend(transcript);
    };

    recognition.onerror = (event) => {
        transcriptBox.value = "Speech recognition failed: " + event.error;
        updateStatus(transcriptStatus, 'idle');
        startBtn.disabled = false;
        stopBtn.disabled = true;
    };

    recognition.onend = () => {
        startBtn.disabled = false;
        stopBtn.disabled = true;
    };

    recognition.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
};

stopBtn.onclick = () => {
    if (recognition) recognition.stop();
    updateStatus(transcriptStatus, 'idle');
    startBtn.disabled = false;
    stopBtn.disabled = true;
};

async function sendToBackend(text) {
    updateStatus(hindiStatus, 'translating');
    updateStatus(spanishStatus, 'translating');
    hindiBox.value = "🔄 Translating...";
    spanishBox.value = "🔄 Translating...";
    speakBtn.disabled = true;

    try {
        const response = await fetch("/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        if (data.hindi && data.spanish) {
            hindiBox.value = data.hindi;
            spanishBox.value = data.spanish;
            updateStatus(hindiStatus, 'ready');
            updateStatus(spanishStatus, 'ready');
            speakBtn.disabled = false;
        } else {
            hindiBox.value = "❌ Translation failed";
            spanishBox.value = "❌ Translation failed";
            updateStatus(hindiStatus, 'idle');
            updateStatus(spanishStatus, 'idle');
        }
    } catch (error) {
        hindiBox.value = "❌ Network error: " + error.message;
        spanishBox.value = "❌ Network error: " + error.message;
        updateStatus(hindiStatus, 'idle');
        updateStatus(spanishStatus, 'idle');
    }
}

speakBtn.onclick = () => {
    // Speak Hindi
    if (hindiBox.value && !hindiBox.value.includes('❌') && !hindiBox.value.includes('🔄')) {
        const hindiUtterance = new SpeechSynthesisUtterance(hindiBox.value);
        hindiUtterance.lang = "hi-IN"; // Hindi voice
        hindiUtterance.rate = 0.9;
        hindiUtterance.pitch = 1;
        speechSynthesis.speak(hindiUtterance);
    }

    
    // Speak Spanish
    if (spanishBox.value && !spanishBox.value.includes('❌') && !spanishBox.value.includes('🔄')) {
        const spanishUtterance = new SpeechSynthesisUtterance(spanishBox.value);
        spanishUtterance.lang = "es-ES"; // Spanish voice
        spanishUtterance.rate = 0.9;
        spanishUtterance.pitch = 1;
        speechSynthesis.speak(spanishUtterance);
    }
};

updateStatus(transcriptStatus, 'idle');
updateStatus(hindiStatus, 'idle');
updateStatus(spanishStatus, 'idle');
