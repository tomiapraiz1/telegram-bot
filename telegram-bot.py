from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import Bot
from dotenv import load_dotenv
import os

# Carga las variables de entorno del archivo .env
load_dotenv()

token = os.getenv("BOT_TOKEN")
help_text = os.getenv("HELP_TEXT")

updater = Updater(token, use_context=True)
  
def start(update: Update, context: CallbackContext):
    update.message.from_user.id
    update.message.reply_text(
        "Bienvenido al bot complementario. " + f"Tu id de usuario es {update.message.from_user.id}")

def help(update: Update, context: CallbackContext):
    update.message.reply_text(help_text)
    
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
print("Bot is running...")

# - Transcribir audios de video. Obtener informacion del curso. Obtener resultado de los examenes. Filminas. ETC