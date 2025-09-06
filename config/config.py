import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DEVELOPER_USERNAME = "deweni2"
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    DOWNLOAD_PATH = "downloads"
    ALLOWED_EXTENSIONS = [".mp4", ".mp3", ".jpg", ".png"]
    
    # Messages
    START_MESSAGE = """
Welcome to Social Media Downloader Bot! 🚀

Commands:
/song <name> - Download a song 🎵
/video <name> - Download a video 🎥

Or send me links from:
- YouTube 📺
- Instagram 📸
- TikTok 🎭
- Facebook 👥
    """
    
    ERROR_MESSAGES = {
        "NO_QUERY": "Please provide a search query!",
        "FILE_TOO_LARGE": "File is too large to download!",
        "UNSUPPORTED_URL": "This URL is not supported!",
        "DOWNLOAD_ERROR": "Error occurred while downloading!"
    }
