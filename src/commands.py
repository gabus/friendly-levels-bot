from src.utils import logging
from psycopg import cursor
from src.repositories.repository import Repository
from src.formatters.formatters import Formatters


class Commands:

    def __init__(self, bot, db: cursor):
        repo = Repository(db)
        formatters = Formatters()

        @bot.command(name='rank', help='gives back all stats')
        async def top_10_rank(ctx):
            logging.log('rank for', ctx.guild.id)
            stats = repo.stats.get_top_10_users(ctx.guild.id)
            await ctx.send(formatters.top_stats(stats))

        @bot.command(name='set-stats-weight', help='set how much messages, reactions, voip and playing matters')
        async def set_stats_weight(ctx):
            stats = repo.stats.get_top_10_users(ctx.guild.id)
            await ctx.send(formatters.top_stats(stats))

        @bot.command(name='get-stats-weight', help='set how much messages, reactions, voip and playing matters')
        async def get_stats_weight(ctx):
            # stats = repo.stats.get_top_10_users(ctx.guild.id)
            await ctx.send("get-stats-weight")

        @bot.command(name='rank-me', help='gives back my stats')
        async def rank_me(ctx):
            # todo add #23 which tells ranking position
            repo.stats.get_my_stats(ctx.guild.id, ctx.author.id)
            logging.log(ctx.guild.id, ctx.guild.name, ctx.author.id, ctx.author.name, StatsType.chat, "command")
            stats = db.get_stats_for_member(ctx.guild.id, ctx.author.id)
            print(stats)
            await ctx.send(stats)
