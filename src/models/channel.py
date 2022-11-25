from src.models.guild import Guild


class Channel:

    def __init__(self, channel_id: int, channel_name: str, guild: Guild):
        self.id = channel_id
        self.name = channel_name
        self.guild = guild

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'guild': self.guild.as_dict()
        }
