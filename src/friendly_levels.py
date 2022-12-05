import os
import discord
from discord.ext import commands
from src.events import Events
from src.commands import Commands
from src.middleware.database import PostgresDatabase


class FriendlyLevels(discord.Client):

    def __init__(self, token):

        db = PostgresDatabase(
            os.getenv('POSTGRES_HOST'),
            os.getenv('POSTGRES_DATABASE'),
            os.getenv('POSTGRES_USER'),
            os.getenv('POSTGRES_PASSWORD'),
        )
        session = db.get_cursor()

        intents = discord.Intents.default()
        intents.message_content = True
        intents.presences = True
        intents.members = True

        bot = commands.Bot(command_prefix='!', intents=intents)

        Events(bot, session)
        Commands(bot, session)

        bot.run(token)
