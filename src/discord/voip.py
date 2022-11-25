from src.models.voip import Voip as VoipModel
from src.models.member import Member as MemberModel
from src.models.guild import Guild as GuildModel
from discord.voice_client import VoiceClient as DiscordVoiceClient
from discord.member import Member as DiscordMember


class Voip:

    def __init__(self, member: DiscordMember, voip: DiscordVoiceClient, is_open: bool):
        self.voip = voip
        self.member = member
        self.is_open = is_open

    def serialize(self) -> VoipModel:
        guild = GuildModel(self.member.guild.id, self.member.guild.name)
        member = MemberModel(self.member.id, self.member.name)
        voip = VoipModel(self.voip.channel.id, self.is_open, member, guild)
        return voip
