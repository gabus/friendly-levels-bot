from src.models.database.message import Message as MessageModel
from psycopg import cursor


class Message:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, message: MessageModel):
        q = "INSERT INTO messages (message, member_id, channel_id) VALUES ('{message}', {member_id}, {channel_id})"\
            .format(message=message.message, member_id=message.member.id, channel_id=message.channel.id)
        self.db.execute(q)
