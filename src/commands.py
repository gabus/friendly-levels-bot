from src.storage import Storage
from src.utils import logging
from src.storage import StatsType


class Commands:

    def __init__(self, bot, db: Storage):

        @bot.command(name='getallstats', help='gives back all stats')
        async def get_all_stats(ctx):
            logging.log(ctx.guild.id, ctx.guild.name, ctx.author.id, ctx.author.name, StatsType.chat, "command")
            await ctx.send(db.get_stats_for_guild(ctx.guild.id))

        @bot.command(name='getmystats', help='gives back my stats')
        async def get_my_stats(ctx):
            logging.log(ctx.guild.id, ctx.guild.name, ctx.author.id, ctx.author.name, StatsType.chat, "command")
            stats = db.get_stats_for_member(ctx.guild.id, ctx.author.id)
            print(stats)
            await ctx.send(stats)
