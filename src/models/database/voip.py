from src.models.database.member import Member
from src.models.database.guild import Guild


class Voip:

    def __init__(self, voip_channel_id: int, is_open: bool, member: Member, guild: Guild, duration_time: int = 0):
        self.is_open = is_open
        self.duration_time = duration_time
        self.member = member
        self.guild = guild
        self.voip_channel_id = voip_channel_id

    def as_dict(self) -> dict:
        return {
            'channel': self.voip_channel_id,
            'is_open': self.is_open,
            'duration_time': self.duration_time,
            'guild': self.guild.as_dict(),
            'member': self.member.as_dict(),
        }
