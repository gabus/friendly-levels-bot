from src.models.message import Message as MessageModel
from src.models.member import Member as MemberModel
from src.models.channel import Channel as ChannelModel
from src.models.guild import Guild as GuildModel
from discord.message import Message as DiscordMessage


class Message:

    def __init__(self, message: DiscordMessage):
        self.message = message

    def serialize(self) -> MessageModel:
        guild = GuildModel(self.message.guild.id, self.message.guild.name)
        channel = ChannelModel(self.message.channel.id, self.message.channel.name, guild)
        member = MemberModel(self.message.author.id, self.message.author.name)
        message = MessageModel(self.message.content, member, channel)
        return message
