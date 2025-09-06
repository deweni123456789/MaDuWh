import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('7896090354:AAFFPhNJUEprSGGcblgzgExkjVsisXbOFww')
    
    @classmethod
    def validate_token(cls):
        if not cls.BOT_TOKEN or cls.BOT_TOKEN == "your_bot_token_here":
            raise ValueError(
                "Bot token not found! Please set BOT_TOKEN in your .env file\n"
                "1. Create a bot with @BotFather\n"
                "2. Copy the token\n"
                "3. Add it to your .env file"
            )
