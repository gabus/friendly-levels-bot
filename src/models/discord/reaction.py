from src.models.database.reaction import Reaction as ReactionModel
from src.models.database.member import Member as MemberModel
from src.models.database.channel import Channel as ChannelModel
from src.models.database.guild import Guild as GuildModel
from discord.raw_models import RawReactionActionEvent as DiscordRawReaction


class Reaction:

    def __init__(self, reaction: DiscordRawReaction):
        self.reaction = reaction

    def serialize(self) -> ReactionModel:
        guild = GuildModel(self.reaction.member.guild.id, self.reaction.member.guild.name)
        channel = ChannelModel(self.reaction.channel_id, '', guild)
        member = MemberModel(self.reaction.member.id, self.reaction.member.name)
        reaction = ReactionModel(self.reaction.emoji.name, member, channel)
        return reaction
