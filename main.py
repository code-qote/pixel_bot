from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, Document
from io import BytesIO
from image_editing import edit_image
import logging
import random
import os

TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '5000'))
URL = os.environ.get('URL')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def get_callback(type, obj):
    return "{'type':" + f"'{type}'" + ", 'id':" + f"{obj['id']}" + "}"


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


@run_async
def photo(update, context):
    photo_file = update.message.photo[0].get_file()
    filename = photo_file.file_path.split('/')[-1]
    outfilename = 'out' + filename
    photo_file.download(filename)
    update.message.reply_text(
        'The photo has been accepted for processing. This may take some time.')
    edit_image(filename, outfilename)
    with open(outfilename, 'rb') as file:
        update.message.reply_photo(file)
    os.remove(filename)
    os.remove(outfilename)


@run_async
def start(update, context):
    update.message.reply_text('send me a picture!')


def main():
    updater = Updater(TOKEN, use_context=True)
    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(URL + TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, photo))
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
