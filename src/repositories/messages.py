from src.models.database.message import Message as MessageModel
from psycopg import cursor


class Message:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, message: MessageModel):
        q = "INSERT INTO messages (message, member_id, channel_id) VALUES ('{message}', {member_id}, {channel_id})"\
            .format(message=message.message, member_id=message.member.id, channel_id=message.channel.id)
        self.db.execute(q)

    def get_top_chatters(self, guild_id: int, limit: int = 3) -> list:
        q = """
            select 
                count(*) as message_count, 
                member_id, 
                row_number() OVER (order by count(*) desc) as place
            from messages m
            left join channels c on c.id = m.channel_id 
            where c.guild_id  = {}
            group by member_id 
            order by count(*) desc
            limit {}
            ;
        """.format(guild_id, limit)

        self.db.execute(q)
        db_rows = self.db.fetchall()

        return db_rows
