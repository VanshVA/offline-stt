
# 🧠 Offline Speech-to-Text API with Vosk + Docker

A fully offline, portable **Speech-to-Text (STT)** engine using [Vosk](https://alphacephei.com/vosk/), built with **Python** and containerized via **Docker**.

Use this to deploy your own STT microservice on any machine (including VPS) and transcribe audio without any internet or third-party API.

## 🧠 What is Vosk?

[Vosk](https://alphacephei.com/vosk/) is an open-source, offline speech recognition toolkit that:

- Runs completely **offline**
- Works with **low memory** (as low as 50MB)
- Supports many languages
- Accepts **WAV audio (mono, 16-bit, 8kHz/16kHz/44.1kHz)**
- Works on **Linux**, **Windows**, **macOS**, and **Raspberry Pi**

## 🎯 Project Features

- Accepts voice/audio recordings from **browser**, **mobile**, or **desktop**
- Supports most formats: `.wav`, `.webm`, `.ogg`, `.mp3`, etc.
- Automatically detects if input is already valid WAV; converts if needed (via `ffmpeg`)
- Runs fully in Docker container
- Output is returned as simple **JSON**: `{ "text": "hello world" }`

## 📦 Requirements

- Docker installed (`https://docs.docker.com/get-docker/`)
- ~512MB+ RAM machine or VPS
- Audio files (can be `.wav`, `.webm`, `.mp3`, etc.)
- Vosk model files (downloaded once)

## 📂 Folder Structure

offline-stt-api/
├── app/
│ ├── server.py # Python Flask API
│ ├── requirements.txt # Python dependencies
│ └── model/ # Vosk model directory (added manually)
├── Dockerfile # For building the container
└── README.md # You're reading it!


## 🛠 Setup Instructions

🔧 1. Clone this Repository


git clone https://github.com/yourname/offline-stt-api.git
cd offline-stt-api


📥 2. Download Vosk Model


Go to: https://alphacephei.com/vosk/models

Example: Small English model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 app/model
📁 After this, app/model should contain conf/, am/, rescore.conf, etc.

🐳 3. Build Docker Container

docker build -t offline-stt .

▶️ 4. Run the Container

docker run -p 7860:7860 offline-stt
Now your API is live at:
📍 http://localhost:7860/api/speech-to-text

You can now upload audio from any frontend or API client.

## ⚙️ Audio Handling Logic

✅ If uploaded file is already WAV (mono, 16-bit, 16000Hz): transcribed directly

🔄 Otherwise: ffmpeg converts the file into valid WAV

🎯 Result is passed to Vosk STT engine

🧹 Temporary files are deleted automatically after use

## 🧪 API Example

Request (with curl):

curl -X POST http://localhost:7860/api/speech-to-text \
  -F "audio=@sample.webm"
Response:
json
{
  "text": "hello world"
}
You can also use this in Postman or from your browser frontend using fetch() or Axios.

## 🧩 System Design

flowchart TD
    A[Browser or App] -->|Uploads audio| B[Flask API]
    B --> C{Is WAV valid?}
    C -->|Yes| D[Vosk Transcribe]
    C -->|No| E[ffmpeg Converts to WAV] --> D
    D --> F[Return JSON Response]
    
## 📚 Use Cases

Browser-based STT input forms

Offline assistants on Raspberry Pi or local machines

Voice-controlled software with no internet access

Integrating into Python/Node.js/React/Flutter apps

## 📦 Example Frontend (Browser)

html
Copy
Edit
<button id="start">Start</button>
<button id="stop">Stop & Upload</button>
<audio id="player" controls></audio>
<p id="result"></p>

<script>
let mediaRecorder;
let audioChunks = [];

document.getElementById("start").onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => {
        if (e.data.size > 0) audioChunks.push(e.data);
    };

    mediaRecorder.start();
};

document.getElementById("stop").onclick = async () => {
    mediaRecorder.stop();

    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: 'audio/webm' });
        document.getElementById("player").src = URL.createObjectURL(blob);

        const formData = new FormData();
        formData.append('audio', blob, 'recorded.webm');

        const res = await fetch('http://localhost:7860/api/speech-to-text', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();
        document.getElementById("result").innerText = data.text || data.error;
    };
};
</script>

## 🎙️ Language Supported

| Lang Code | Language | Folder            |
| --------- | -------- | ----------------- |
| `en`      | English  | `app/model`       |
| `hi`      | Hindi    | `app/model-hindi` |

--> For hindi use [http://localhost:7860/api/speech-to-text?lang=hi]
--> For English use [http://localhost:7860/api/speech-to-text?lang=en]

## 🤝 Credits

Vosk — Offline STT Engine

Flask — Python Microservice Framework

ffmpeg — Audio format convert







