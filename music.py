import logging
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, \
    MessageHandler, Filters, ConversationHandler, filters
from config import TOKEN
import re

# re.match('https:\/\/www\.youtube\.[a-z]{2,}\/watch\?v=([A-Za-z0-9-_\&]+)', url)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

EXPECT_LINK = range(1)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Bot started...')


def echo(update: Update, context: CallbackContext):
    message_text = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"reply - {message_text}")


def get_link(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me youtube link")
    return EXPECT_LINK


def link_input_by_user(update: Update, context: CallbackContext):
    link = update.message.text
    if re.match('https:\/\/www\.youtube\.[a-z]{2,}\/watch\?v=([A-Za-z0-9-_\&]+)', link):
        update.message.reply_text(f'Your link is VALID')
        update.message.reply_text(f'Start download')
        download_music(link=link)
    else:
        update.message.reply_text("Your link is INVALID or it's not a link!!!!")
    # ends this particular conversation flow
    return ConversationHandler.END


def download_music(link):
    pass


def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='See ya...')
    return ConversationHandler.END


# Handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
ch = ConversationHandler(entry_points=[CommandHandler('getmp3', get_link)],
                         states={
                             EXPECT_LINK: [MessageHandler(Filters.text, link_input_by_user)],
                         },
                         fallbacks=[CommandHandler('cancel', cancel)])
dispatcher.add_handler(ch)
end_handler = CommandHandler('cancel', cancel)
dispatcher.add_handler(end_handler)

updater.start_polling()
updater.idle()
