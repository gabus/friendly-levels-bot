import os
import discord
from dotenv import load_dotenv
from loguru import logger
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

database = {
    "guild_id": {
        "date": {
            "member_id": {
                "messages_count": 46551,
                "voip_time_min": 234525,
                "reactions_count": 234
            }
        }
    }
}


@bot.event
async def on_ready():
    logger.success('{} has connected to Discord!'.format(bot.user))
    logger.success('{} is connected to the following guilds:'.format(bot.user))
    for guild in bot.guilds:
        logger.success('{} (id: {})'.format(guild.name, guild.id))

# todo - with every event require guild_id + member_id
#    stats are collected per guild (server)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    m = ("message received from {}: {}".format(message.author, message.content))
    await message.channel.send(m)
    await bot.process_commands(message)  # required for commands to work https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working


@bot.event
async def on_voice_state_update(member, before, after):
    logger.debug(f'{member.name=}')
    logger.debug(f'{member.guild.name=}')
    logger.debug(f'{before.channel=}')
    logger.debug(f'{after.channel=}')
    if after.channel:
        logger.debug("member joined voip. Start leveling up for VOIP")
    else:
        logger.debug("member quit. stop")


@bot.event
async def on_raw_reaction_add(payload):
    logger.debug(f'{payload.user_id=}')
    logger.debug(f'{payload.guild_id=}')
    logger.debug(f'{payload=}')


@bot.command(name='getallstats', help='gives back all stats')
async def get_all_stats(ctx):
    # todo extract guild id from here
    logger.debug(f'{ctx.guild.id=}')
    logger.debug(f'{ctx.author.id=}')
    await ctx.send(database)


@bot.command(name='getmystats', help='gives back my stats')
async def get_my_stats(ctx):
    # todo extract guild_id + member_id from here
    logger.debug(f'{ctx.guild.id=}')
    logger.debug(f'{ctx.author.id=}')
    await ctx.send(database)

bot.run(TOKEN)
