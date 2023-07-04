from loguru import logger
from psycopg import cursor
from src.utils import logging
from src.models.discord.reaction import Reaction
from src.models.discord.voip import Voip
from src.models.discord.member_playing import MemberPlaying
from src.models.discord.message import Message
from src.models.database.guild import Guild as GuildModel
from src.repositories.repository import Repository
from discord.voice_client import VoiceClient as DiscordVoiceClient
from discord.member import Member as DiscordMember
from discord.message import Message as DiscordMessage
from discord.activity import ActivityType
from discord.raw_models import RawReactionActionEvent as DiscordRawReaction


class Events:

    def __init__(self, bot, db: cursor):

        @bot.event
        async def on_ready():
            logger.success('{} has connected to Discord!'.format(bot.user))
            logger.success('{} is connected to the following guilds:'.format(bot.user))
            repo = Repository(db)
            for guild in bot.guilds:
                logger.success('{} (id: {})'.format(guild.name, guild.id))

                # create default level_weights and guild
                repo.level_weights.create(guild.id)
                repo.guild.save(GuildModel(guild.id, guild.name))

        @bot.event
        async def on_message(message: DiscordMessage):
            if message.author == bot.user:
                return

            m = Message(message).serialize()
            logging.log("MESSAGE", m.as_dict())

            repo = Repository(db)
            repo.channel.save(m.channel)
            repo.member.save(m.member)
            repo.message.save(m)

            await bot.process_commands(message)  # required for commands to work https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working

        @bot.event
        async def on_raw_reaction_add(payload: DiscordRawReaction):
            r = Reaction(payload).serialize()
            logging.log("REACTION", r.as_dict())

            repo = Repository(db)
            repo.channel.save(r.channel)
            repo.member.save(r.member)
            repo.reaction.save(r)

        @bot.event
        async def on_voice_state_update(member: DiscordMember, before: DiscordVoiceClient, after: DiscordVoiceClient):
            repo = Repository(db)

            if after.channel:
                v = Voip(member, after, True).serialize()
                logging.log("VOIP JOINED", v.as_dict())

                repo.member.save(v.member)
                repo.voip.save(v)

            if before.channel:
                v = Voip(member, before, True).serialize()
                logging.log("VOIP LEFT", v.as_dict())

                voip = repo.voip.get(before.channel.id, member.id, True)
                repo.voip.update_is_open(voip, False)

        @bot.event
        async def on_presence_update(before: DiscordMember, after: DiscordMember):
            repo = Repository(db)

            if before.bot:
                logging.log("ACTIVITY BOT skipped", "{}: {}".format(before.name, before.activities[0].name))
                return

            # Finished activities
            for activity in before.activities:
                """
                    On MacOS activity is Game class instead of Activity. 
                    Game class is very limited. No implementation made atm
                """
                if activity.type == ActivityType.playing:
                    mp = MemberPlaying(activity, before, False).serialize()

                    logging.log("ACTIVITY STOPPED", mp.as_dict())

                    repo.game.save(mp.game)
                    repo.member.save(mp.member)
                    repo.member_playing.stop_game(mp)

            # Started and ongoing activities
            for activity in after.activities:
                if activity.type == ActivityType.playing:
                    mp = MemberPlaying(activity, after, True).serialize()

                    logging.log("ACTIVITY STARTED", mp.as_dict())

                    # check if session already exist
                    if repo.member_playing.session_exits(mp):
                        continue

                    repo.game.save(mp.game)
                    repo.member.save(mp.member)
                    repo.member_playing.start_game(mp)
