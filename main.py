from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
import logging
from music import *
from weather import *

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Bot started...')


def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='See ya...')
    return ConversationHandler.END


# Handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
ch = ConversationHandler(entry_points=[CommandHandler('getmp3', get_link), CommandHandler('getweather', get_city)],
                         states={
                             EXPECT_LINK: [MessageHandler(Filters.text, link_input_by_user)],
                             EXPECT_CITY: [MessageHandler(Filters.text, send_weather)],
                         },
                         fallbacks=[CommandHandler('cancel', cancel)])
dispatcher.add_handler(ch)
end_handler = CommandHandler('cancel', cancel)
dispatcher.add_handler(end_handler)

updater.start_polling()
updater.idle()
