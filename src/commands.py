from src.utils import logging
from psycopg import cursor
from src.repositories.repository import Repository
from src.formatters.formatters import Formatters


class Commands:

    def __init__(self, bot, db: cursor):
        repo = Repository(db)
        formatters = Formatters()

        @bot.command(name='rank', help='Get back top users')
        async def top_x_rank(ctx):
            logging.log('rank', "Guild: {}".format(ctx.guild.id))
            member_ids = [member.id for member in ctx.guild.members]
            stats = repo.stats.get_top_x_users(ctx.guild.id, member_ids, 5)
            await ctx.send(formatters.top_stats(stats))

        @bot.command(name='rank-me', help='Get back my stats')
        async def rank_me(ctx):
            logging.log('rank-me', "Guild: {}, Member: {}".format(ctx.guild.id, ctx.member.id))
            level_weights = repo.stats.get_my_stats(ctx.guild.id, ctx.member.id)
            await ctx.send(level_weights())

        @bot.command(name='set-message-weight', help='Set how much messages matters (default 1)')
        async def set_message_weights(ctx, weight=None):
            logging.log('set-message-weight for guild_id', ctx.guild.id)

            try:
                float(weight)
            except TypeError as te:
                await ctx.send("need to set a number value")
                return
            except ValueError as ve:
                await ctx.send("value needs to be a number")
                return

            repo.level_weights.set_message_weight(ctx.guild.id, weight)
            level_weights = repo.level_weights.get(ctx.guild.id)
            await ctx.send(level_weights.as_dict())

        @bot.command(name='set-reaction-weight', help='Set how much reaction matters (default 2)')
        async def set_reaction_weights(ctx, weight=None):
            logging.log('set-reaction-weight for guild_id', ctx.guild.id)

            try:
                float(weight)
            except TypeError as te:
                await ctx.send("need to set a number value")
                return
            except ValueError as ve:
                await ctx.send("value needs to be a number")
                return

            repo.level_weights.set_reaction_weight(ctx.guild.id, weight)
            level_weights = repo.level_weights.get(ctx.guild.id)
            await ctx.send(level_weights.as_dict())

        @bot.command(name='set-voip-weight', help='Set how much voip matters (default 0.2)')
        async def set_voip_weights(ctx, weight=None):
            logging.log('set-voip-weight for guild_id', ctx.guild.id)

            try:
                float(weight)
            except TypeError as te:
                await ctx.send("need to set a number value")
                return
            except ValueError as ve:
                await ctx.send("value needs to be a number")
                return

            repo.level_weights.set_voip_weight(ctx.guild.id, weight)
            level_weights = repo.level_weights.get(ctx.guild.id)
            await ctx.send(level_weights.as_dict())

        @bot.command(name='set-playing-weight', help='Set how much playing matters (default 0)')
        async def set_playing_weights(ctx, weight=None):
            logging.log('set-voip-weight for guild_id', ctx.guild.id)

            try:
                float(weight)
            except TypeError as te:
                await ctx.send("need to set a number value")
                return
            except ValueError as ve:
                await ctx.send("value needs to be a number")
                return

            repo.level_weights.set_playing_weight(ctx.guild.id, weight)
            level_weights = repo.level_weights.get(ctx.guild.id)
            await ctx.send(level_weights.as_dict())

        @bot.command(name='get-weights', help='get all interaction weights')
        async def get_weights(ctx):
            logging.log('get-weights for guild_id', ctx.guild.id)
            level_weights = repo.level_weights.get(ctx.guild.id)
            await ctx.send(level_weights.as_dict())
