from psycopg import cursor


class Stats:

    def __init__(self, db: cursor):
        self.db = db

    def get_top_10_voip(self):
        # q = "INSERT INTO guilds (id, name) VALUES ({id}, {name})".format(id=guild.id, name=guild.name)
        # select
        # join
        # join
        # self.db.execute(q)
        pass
