from loguru import logger
from src.utils import logging
from src.utils import datetime_util
from src.storage import StatsType
from src.storage import Storage


class Events:

    def __init__(self, bot, db: Storage):

        voip_time_tracker = {}

        @bot.event
        async def on_ready():
            logger.success('{} has connected to Discord!'.format(bot.user))
            logger.success('{} is connected to the following guilds:'.format(bot.user))
            for guild in bot.guilds:
                logger.success('{} (id: {})'.format(guild.name, guild.id))

        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return

            logging.log(message.guild.id, message.guild.name, message.author.id, message.author.name, StatsType.chat)
            db.add_stats(message.guild.id, message.author.id, StatsType.chat, 1)
            # m = ("message received from {}: {}".format(message.author, message.content))
            # await message.channel.send(m)
            await bot.process_commands(message)  # required for commands to work https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working

        @bot.event
        async def on_voice_state_update(member, before, after):
            key = str(member.guild.id) + '-' + str(member.id)

            if after.channel:
                logging.log(member.guild.id, member.guild.name, member.id, member.name, StatsType.voip, "joined")

                if key in voip_time_tracker:
                    return

                voip_time_tracker[key] = datetime_util.now()
            else:
                logging.log(member.guild.id, member.guild.name, member.id, member.name, StatsType.voip, "left")
                to_time = datetime_util.now()
                value = (to_time - voip_time_tracker[key]).total_seconds()
                db.add_stats(member.guild.id, member.id, StatsType.voip, round(value))
                del (voip_time_tracker[key])

        @bot.event
        async def on_raw_reaction_add(payload):
            logging.log(payload.guild_id, 'missing', payload.member.id, payload.member.name, StatsType.reaction)
            db.add_stats(payload.guild_id, payload.member.id, StatsType.reaction, 1)
