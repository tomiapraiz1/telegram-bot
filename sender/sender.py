from telegram import Bot
from flask import Flask, request
import os

bot_token = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
   return "TELEGRAM BOT SENDER", 200

telegram_bot = Bot(token=bot_token)

@app.route('/send', methods = ['POST'])
def send_message():
    try:
        chatid = request.json.get("chatid")
        msg = request.json.get("msg")
    except:
        return "Faltan parametros del json", 400
    
    telegram_bot.send_message(chat_id=chatid, text=msg)

    return "Mensaje enviado", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)