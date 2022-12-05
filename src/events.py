from loguru import logger
from src.utils import logging
from src.discord.message import Message
from src.discord.reaction import Reaction
from src.discord.voip import Voip
from src.repositories.repository import Repository
from psycopg import cursor
from discord.voice_client import VoiceClient as DiscordVoiceClient
from discord.member import Member as DiscordMember
from discord.message import Message as DiscordMessage
from discord.raw_models import RawReactionActionEvent as DiscordRawReaction


class Events:

    def __init__(self, bot, db: cursor):

        @bot.event
        async def on_ready():
            logger.success('{} has connected to Discord!'.format(bot.user))
            logger.success('{} is connected to the following guilds:'.format(bot.user))
            for guild in bot.guilds:
                logger.success('{} (id: {})'.format(guild.name, guild.id))

        @bot.event
        async def on_message(message: DiscordMessage):
            if message.author == bot.user:
                return

            m = Message(message).serialize()
            logging.log("MESSAGE", m.as_dict())

            repo = Repository(db)
            repo.guild.save(m.channel.guild)
            repo.channel.save(m.channel)
            repo.member.save(m.member)
            repo.message.save(m)

            await bot.process_commands(message)  # required for commands to work https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working

        @bot.event
        async def on_raw_reaction_add(payload: DiscordRawReaction):
            r = Reaction(payload).serialize()
            logging.log("MESSAGE", r.as_dict())

            repo = Repository(db)
            repo.guild.save(r.channel.guild)
            repo.channel.save(r.channel)
            repo.member.save(r.member)
            repo.reaction.save(r)

        @bot.event
        async def on_voice_state_update(member: DiscordMember, before: DiscordVoiceClient, after: DiscordVoiceClient):
            repo = Repository(db)

            if after.channel:
                v = Voip(member, after, True).serialize()
                logging.log("VOIP JOINED", v.as_dict())

                repo.guild.save(v.guild)
                repo.member.save(v.member)
                repo.voip.save(v)

            if before.channel:
                v = Voip(member, before, True).serialize()
                logging.log("VOIP LEFT", v.as_dict())
                logging.log('member left voip', f'{member=}')  # todo remove this line after debugging

                voip = repo.voip.get(before.channel.id, member.id, True)
                repo.voip.update_is_open(voip, False)

        # @bot.event
        # async def on_presence_update(before: DiscordMember, after: DiscordMember):
            # todo store which game is being played (or multiple)
            # guild_id = before.guild.id
            # guild_name = before.guild.name
            # member_id = before.id
            # member_name = before.name
            # key = str(before.guild.id) + '-' + str(before.id)
            #
            # activity_found = False
            # for activity in after.activities:
            #     if activity.type == ActivityType.playing:
            #         print(activity)
            #         print(activity.application_id)
            #         print(activity.name)
            #         activity_found = True

