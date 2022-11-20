from src.friendly_levels import FriendlyLevels
from dotenv import load_dotenv
import os


if __name__ == "__main__":
    load_dotenv()
    FriendlyLevels(os.getenv('DISCORD_TOKEN'))
