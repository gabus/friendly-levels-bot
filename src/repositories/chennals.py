from src.models.database.channel import Channel as ChannelModel
from psycopg import cursor


class Channel:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, channel: ChannelModel):
        if not channel.name:
            q = "SELECT name FROM channels WHERE id = {}".format(channel.id)
            self.db.execute(q)
            channel_name = self.db.fetchone()
            channel.name = channel_name['name']

        q = "INSERT INTO channels (id, name, guild_id) VALUES ({id}, '{name}', {guild_id}) ON CONFLICT DO NOTHING"\
            .format(id=channel.id, name=channel.name, guild_id=channel.guild.id)
        self.db.execute(q)
