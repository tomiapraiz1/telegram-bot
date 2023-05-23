import re
from flask import Flask, request
from faster_whisper import WhisperModel

model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

app = Flask(__name__)

@app.route('/')
def index():
    return "Whisper running!"

@app.route('/whisper', methods=['POST'])
def whisper():
    if not request.files:
        return "Falta el archivo a traducir", 400
    
    archivo = request.files['file']
    
    segments, info = model.transcribe(archivo, beam_size=5)

    print("Lenguaje detectado '%s' con probabilidad %f" % (info.language, info.language_probability))

    transcription = ""
    
    for segment in segments:
        transcription += ("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    transcription_complete = re.sub(r"\[(.*?)\]", "", transcription)
    print(transcription_complete)

    return {'nombre del archivo': archivo.filename, 'transcripcion': transcription_complete}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)