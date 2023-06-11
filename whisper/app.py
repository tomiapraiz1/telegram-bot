import re, os, html
from flask import Flask, request, Response
from faster_whisper import WhisperModel
from pytube import YouTube
from gtts import gTTS

model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

app = Flask(__name__)

def transcript(archivo):
    """
        Devuelve la transcripcion completa de un archivo de audio o video
    """
    segments, info = model.transcribe(archivo, beam_size=5)

    print("Lenguaje detectado '%s' con probabilidad %f" % (info.language, info.language_probability))

    transcription = ""
    
    for segment in segments:
        transcription += ("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    transcription_complete = re.sub(r"\[(.*?)\]", "", transcription)
    print(transcription_complete)
    
    return transcription_complete

@app.route('/', methods=['GET'])
def index():
    return "Whisper running!"

@app.route('/tts', methods=['POST'])
def tts():
    """
        Devuelve un archivo .mp3 con el texto pedido
    """
    try:
        text = request.json.get("text")
    except:
        return "Falta el texto a convertir", 400
    

    tts = gTTS(text, lang='es', tld='com.mx', slow=False)
    filename = 'output.mp3'
    script_dir = os.path.dirname(__file__)
    save_path = os.path.join(script_dir, filename)
    tts.save(save_path)
    
    with open(save_path, 'rb') as f:
        mp3_data = f.read()

    response = Response(mp3_data, mimetype='audio/mpeg')
    response.headers.set('Content-Disposition', 'attachment', filename=filename)

    return response

@app.route('/transcript', methods=['POST'])
def transcription():
    """
        Devuelve la transcripcion en un JSON junto al titulo del video/audio
    """
    try:
        url = request.json.get("url")
    except:
        return "Falta la url", 400
    
    video = YouTube(url).streams.filter(type='video',file_extension='mp4',progressive=True).first().download()
    titulo = YouTube(url).streams.filter(type='video',file_extension='mp4',progressive=True).first().title
    video = video.replace("3gpp","mp4")
    
    transcripcion = transcript(video)

    if os.path.exists(video):
        os.remove(video)

    transcripcion_decodificada = html.unescape(transcripcion)

    return  {'nombre del archivo': titulo, 'transcripcion': transcripcion_decodificada}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)