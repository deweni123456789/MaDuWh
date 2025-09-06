from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from config.config import Config

def get_developer_button():
    keyboard = [[InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{Config.DEVELOPER_USERNAME}")]]
    return InlineKeyboardMarkup(keyboard)

def clean_download_dir():
    if os.path.exists(Config.DOWNLOAD_PATH):
        for file in os.listdir(Config.DOWNLOAD_PATH):
            file_path = os.path.join(Config.DOWNLOAD_PATH, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error: {e}")

def create_download_dir():
    if not os.path.exists(Config.DOWNLOAD_PATH):
        os.makedirs(Config.DOWNLOAD_PATH)

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
