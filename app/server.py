from flask import Flask, request, jsonify
import os
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer

app = Flask(__name__)

# Load models once
models = {
    "en": Model("model"),           # English model path
    "hi": Model("model-hindi")      # Hindi model path
}

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    lang = request.args.get("lang", "en")
    if lang not in models:
        return jsonify({'error': 'Unsupported language'}), 400

    model = models[lang]
    uploaded_file = request.files['audio']
    input_path = "input_audio"
    converted_path = "converted.wav"

    uploaded_file.save(input_path)

    try:
        with wave.open(input_path, "rb") as wf:
            channels = wf.getnchannels()
            width = wf.getsampwidth()
            rate = wf.getframerate()

            if channels == 1 and width == 2 and rate in [8000, 16000, 44100]:
                final_path = input_path
            else:
                raise Exception("Invalid WAV format")
    except:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-ac", "1", "-ar", "16000", converted_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        final_path = converted_path

    try:
        wf = wave.open(final_path, "rb")
        rec = KaldiRecognizer(model, wf.getframerate())

        result_text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                result_text += res.get("text", "")
        wf.close()
    except Exception as e:
        return jsonify({'error': f"Error during transcription: {str(e)}"}), 500
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(converted_path): os.remove(converted_path)

    return jsonify({'text': result_text.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
