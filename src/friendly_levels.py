import discord
from loguru import logger
from discord.ext import commands
from src.events import Events
from src.commands import Commands
from src.storage import Storage


class FriendlyLevels(discord.Client):

    def __init__(self, token):

        db = Storage()

        intents = discord.Intents.default()
        intents.message_content = True
        intents.presences = True
        intents.members = True

        bot = commands.Bot(command_prefix='!', intents=intents)

        Events(bot, db)
        Commands(bot, db)

        bot.run(token)

