import re, os
from flask import Flask, request
from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip
from pytube import YouTube

model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

app = Flask(__name__)

def transcript(archivo):
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

@app.route('/transcript', methods=['GET'])
def download():
    try:
        url = request.json.get("url")
    except:
        return "Falta la url", 400
    
    video = YouTube(url).streams.filter(type='video',file_extension='mp4',progressive=True).first().download()
    titulo = YouTube(url).streams.filter(type='video',file_extension='mp4',progressive=True).first().title
    video = video.replace("3gpp","mp4")
    audioname = "test_audio.wav"

    videoclip = VideoFileClip(video) #Hacemos que el video se guarde en formato video en la variable
    audioclip = videoclip.audio #Pasamos el video a formato audio
    audioclip.write_audiofile(audioname) #Escribimos el audio en formato wav
    
    archivo = audioname
    transcripcion = transcript(archivo)

    if os.path.exists("test_audio.wav"):
        os.remove("test_audio.wav")

    return {'nombre del archivo': titulo, 'transcripcion': transcripcion}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)