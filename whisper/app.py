import re, os, html
from flask import Flask, request, Response
from faster_whisper import WhisperModel
from gtts import gTTS
import yt_dlp

model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

app = Flask(__name__)

def download_video(url):
    """
        Descarga el video de Youtube y lo devuelve
    """
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video = ydl.extract_info(url)
        video_id = video['id']
        title = video['title']

    return f'{title} [{video_id}].m4a', title

def transcript(file):
    """
        Devuelve la transcripcion completa de un archivo de audio o video
    """
    segments, info = model.transcribe(file, beam_size=5)

    print("Lenguaje detectado '%s' con probabilidad %f" % (info.language, info.language_probability))

    transcription_text = ""
    
    for segment in segments:
        transcription_text += ("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    transcription_complete = re.sub(r"\[(.*?)\]", "", transcription_text)
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
    except Exception as e:
        return f'Error: {e}', 400
    

    speech = gTTS(text, lang='es', tld='com.mx', slow=False)
    filename = 'output.mp3'
    script_dir = os.path.dirname(__file__)
    save_path = os.path.join(script_dir, filename)
    speech.save(save_path)
    
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
    except Exception as e:
        return f'Error: {e}', 400
    
    video, titulo = download_video(url)
    
    transcripcion = transcript(video)

    if os.path.exists(video):
        os.remove(video)

    transcripcion_decodificada = html.unescape(transcripcion)

    return  {'nombre del archivo': titulo, 'transcripcion': transcripcion_decodificada}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)