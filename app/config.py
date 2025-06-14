import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # GitHub Configuration
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Application Settings
    APP_NAME = "Code Review Bot"
    VERSION = "1.0.0"
    
    def validate(self):
        """Validate required environment variables"""
        required_vars = {
            "GITHUB_TOKEN": self.GITHUB_TOKEN,
            "WEBHOOK_SECRET": self.WEBHOOK_SECRET
        }
        
        missing = [var for var, value in required_vars.items() if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True

settings = Settings()