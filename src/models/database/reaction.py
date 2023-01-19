from src.models.database.channel import Channel
from src.models.database.member import Member


class Reaction:

    def __init__(self, emoji: str, member: Member, channel: Channel):
        self.emoji = emoji
        self.member = member
        self.channel = channel

    def as_dict(self) -> dict:
        return {
            'emoji': self.emoji,
            'member': self.member.as_dict(),
            'channel': self.channel.as_dict()
        }
