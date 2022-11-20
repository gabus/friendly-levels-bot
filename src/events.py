from loguru import logger
from src.utils import logging
from src.utils import datetime_util
from src.storage import StatsType
from src.storage import Storage
from discord.activity import ActivityType


class Events:

    def __init__(self, bot, db: Storage):

        voip_time_tracker = {}
        playing_time_tracker = {}

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
            # todo save room id too -- interesting which room chatted the most
            db.add_stats(message.guild.id, message.author.id, StatsType.chat, 1)
            await bot.process_commands(message)  # required for commands to work https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working

        @bot.event
        async def on_voice_state_update(member, before, after):
            key = str(member.guild.id) + '-' + str(member.id)
            # todo store which channel member is in
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
            # todo store which emoji is used the most
            logging.log(payload.guild_id, 'missing', payload.member.id, payload.member.name, StatsType.reaction)
            db.add_stats(payload.guild_id, payload.member.id, StatsType.reaction, 1)

        @bot.event
        async def on_presence_update(before, after):
            # todo store which game is being played (or multiple)
            guild_id = before.guild.id
            guild_name = before.guild.name
            member_id = before.id
            member_name = before.name
            key = str(before.guild.id) + '-' + str(before.id)

            activity_found = False
            for activity in after.activities:
                if activity.type == ActivityType.playing:
                    print(activity)
                    print(activity.application_id)
                    print(activity.name)
                    activity_found = True

            # if activity_found:
                # playing_time_tracker[]