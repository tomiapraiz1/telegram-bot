from telegram import Bot
from flask import Flask, request
import os, codecs, json, re
import requests

bot_token = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

def download_file_from_drive(url, name):
    # Obtén el ID del archivo desde la URL
    file_id = url.split('/')[-2]

    # Construye la URL de descarga directa del archivo
    download_url = f"https://drive.google.com/uc?id={file_id}"

    # Realiza la solicitud GET para descargar el archivo
    response = requests.get(download_url)
    
    destination_file_path = f'{name}.pdf'

    # Guarda el archivo descargado
    with open(destination_file_path, 'wb') as f:
        f.write(response.content)

    return destination_file_path

@app.route('/', methods = ['GET'])
def index():
   return "TELEGRAM BOT SENDER", 200

telegram_bot = Bot(token=bot_token)

@app.route('/sendfile', methods = ['POST'])
def send_file():
    try:
        chatid = request.json.get("chatid")
        url = request.json.get("url")
        name = request.json.get("name")
    except Exception as e:
        return f'Error: {e}', 400
    
    try:
        # Descargar el archivo y obtener la ruta del archivo descargado
        file_path = download_file_from_drive(url, name)
        
        # Enviar el archivo al chat utilizando la biblioteca de Telegram
        with open(file_path, 'rb') as file:
            telegram_bot.send_document(chat_id=chatid, document=file)
        
        # Eliminar el archivo después de enviarlo
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return "Archivo enviado", 200
    except Exception as e:
        return f'Error al enviar el archivo: {e}', 400

@app.route('/send', methods = ['POST'])
def send_message():
    try:
        chatid = request.json.get("chatid")
        msg = request.json.get("msg")
    except:
        return "Faltan parametros del json", 400
    
    msg = json.dumps(msg)
    
    msg_decodificado = codecs.decode(msg, 'unicode_escape')    
    telegram_bot.send_message(chat_id=chatid, text=msg_decodificado)

    return "Mensaje enviado", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)