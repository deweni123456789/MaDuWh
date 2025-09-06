import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import yt_dlp
import asyncio
import os
from config.config import Config
from utils.helpers import get_developer_button, clean_download_dir, create_download_dir
import instaloader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize downloaders
L = instaloader.Instaloader()

class SocialMediaBot:
    def __init__(self):
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        self.setup_handlers()
        create_download_dir()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("song", self.download_song))
        self.application.add_handler(CommandHandler("video", self.download_video))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_url))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            Config.START_MESSAGE,
            reply_markup=get_developer_button()
        )

    # Add all your existing download functions here, modified to use Config and helpers

    def run(self):
        self.application.run_polling()

if __name__ == '__main__':
    bot = SocialMediaBot()
    try:
        bot.run()
    finally:
        clean_download_dir()
