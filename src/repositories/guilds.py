from src.models.guild import Guild as GuildModel
from psycopg import cursor


class Guild:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, guild: GuildModel):
        q = "INSERT INTO guilds (id, name) VALUES ({id}, '{name}') ON CONFLICT DO NOTHING".format(id=guild.id, name=guild.name)
        self.db.execute(q)
