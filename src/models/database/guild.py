class Guild:

    def __init__(self, guild_id: int, guild_name: str):
        self.id = guild_id
        self.name = guild_name

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
