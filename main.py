from src.friendly_levels import FriendlyLevels
from dotenv import load_dotenv
import os


def run():
    load_dotenv()
    FriendlyLevels(os.getenv('DISCORD_TOKEN'))


if __name__ == "__main__":
    run()
