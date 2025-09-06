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
            reply_markup=get_developer_button(),
            parse_mode='Markdown'
        )

    async def download_song(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text(
                "Please provide a song name! Example: `/song Shape of You`",
                reply_markup=get_developer_button(),
                parse_mode='Markdown'
            )
            return
        
        query = " ".join(context.args)
        status_message = await update.message.reply_text("🎵 *Searching for your song...*", parse_mode='Markdown')
        
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(Config.DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)
                file_path = os.path.join(Config.DOWNLOAD_PATH, f"{info['entries'][0]['title']}.mp3")
                
                with open(file_path, 'rb') as audio:
                    await update.message.reply_audio(
                        audio,
                        caption=f"🎵 *{info['entries'][0]['title']}*",
                        reply_markup=get_developer_button(),
                        parse_mode='Markdown'
                    )
                os.remove(file_path)
            
            await status_message.delete()
        except Exception as e:
            logger.error(f"Error downloading song: {str(e)}")
            await status_message.edit_text(
                f"❌ *Error downloading song:* `{str(e)}`",
                reply_markup=get_developer_button(),
                parse_mode='Markdown'
            )

    async def download_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text(
                "Please provide a video name! Example: `/video cute cats`",
                reply_markup=get_developer_button(),
                parse_mode='Markdown'
            )
            return
        
        query = " ".join(context.args)
        status_message = await update.message.reply_text("🎥 *Searching for your video...*", parse_mode='Markdown')
        
        try:
            ydl_opts = {
                'format': f'best[filesize<{Config.MAX_FILE_SIZE}]',
                'outtmpl': os.path.join(Config.DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)
                video_path = os.path.join(Config.DOWNLOAD_PATH, f"{info['entries'][0]['title']}.mp4")
                
                with open(video_path, 'rb') as video:
                    await update.message.reply_video(
                        video,
                        caption=f"🎥 *{info['entries'][0]['title']}*",
                        reply_markup=get_developer_button(),
                        parse_mode='Markdown'
                    )
                os.remove(video_path)
            
            await status_message.delete()
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            await status_message.edit_text(
                f"❌ *Error downloading video:* `{str(e)}`",
                reply_markup=get_developer_button(),
                parse_mode='Markdown'
            )

    async def handle_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        url = update.message.text.strip()
        status_message = await update.message.reply_text("🔄 *Processing your link...*", parse_mode='Markdown')
        
        try:
            if "youtube.com" in url or "youtu.be" in url:
                await self.download_youtube(update, url, status_message)
            elif "instagram.com" in url:
                await self.download_instagram(update, url, status_message)
            elif "tiktok.com" in url:
                await self.download_tiktok(update, url, status_message)
            elif "facebook.com" in url or "fb.com" in url:
                await self.download_facebook(update, url, status_message)
            else:
                await status_message.edit_text(
                    "❌ *Unsupported URL!* Please send a valid social media link.",
                    reply_markup=get_developer_button(),
                    parse_mode='Markdown'
                )
        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}")
            await status_message.edit_text(
                f"❌ *Error processing URL:* `{str(e)}`",
                reply_markup=get_developer_button(),
                parse_mode='Markdown'
            )

    async def download_youtube(self, update: Update, url: str, status_message):
        try:
            ydl_opts = {
                'format': f'best[filesize<{Config.MAX_FILE_SIZE}]',
                'outtmpl': os.path.join(Config.DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = os.path.join(Config.DOWNLOAD_PATH, f"{info['title']}.mp4")
                
                with open(video_path, 'rb') as video:
                    await update.message.reply_video(
                        video,
                        caption=f"📺 *{info['title']}*",
                        reply_markup=get_developer_button(),
                        parse_mode='Markdown'
                    )
                os.remove(video_path)
            
            await status_message.delete()
        except Exception as e:
            raise Exception(f"YouTube download error: {str(e)}")

    def run(self):
        self.application.run_polling()

if __name__ == '__main__':
    bot = SocialMediaBot()
    try:
        bot.run()
    finally:
        clean_download_dir()
