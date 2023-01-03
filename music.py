from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import re
import youtube_dl
import os

# re.match('https:\/\/www\.youtube\.[a-z]{2,}\/watch\?v=([A-Za-z0-9-_\&]+)', url)

EXPECT_LINK = range(1)


def get_link(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me youtube link")
    return EXPECT_LINK


def link_input_by_user(update: Update, context: CallbackContext):
    link = update.message.text
    if re.match('https:\/\/www\.youtube\.[a-z]{2,}\/watch\?v=([A-Za-z0-9-_\&]+)', link):
        update.message.reply_text('Start download')
        download_music(update, context, link=link)
    else:
        update.message.reply_text("Your link is INVALID or it's not a link!!!!")
    # ends this particular conversation flow
    return ConversationHandler.END


def download_music(update: Update, context: CallbackContext, link):
    video_info = youtube_dl.YoutubeDL().extract_info(url=link, download=False)
    title = video_info['title'].replace(' ', '_')

    #clear the title
    if "_[Lyric_Video]" in title:
        title = title.replace("_[Lyric_Video]", '')
    if "_(Official_Video)" in title:
        title = title.replace("_(Official_Video)", '')

    file_path = f"music/{title}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': file_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        try:
            ydl.download([video_info['webpage_url']])
        except Exception as ex:
            print(ex.args, ex)
        finally:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Downloaded, here is your music:')
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(file_path, 'rb'))
            os.remove(file_path)
