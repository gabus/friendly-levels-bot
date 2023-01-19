from src.models.database.channel import Channel
from src.models.database.member import Member


class Message:

    def __init__(self, message: str, member: Member, channel: Channel):
        self.message = message
        self.member = member
        self.channel = channel

    def as_dict(self) -> dict:
        return {
            'message': self.message,
            'member': self.member.as_dict(),
            'channel': self.channel.as_dict()
        }
