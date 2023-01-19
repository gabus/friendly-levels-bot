from src.models.database.reaction import Reaction as ReactionModel
from psycopg import cursor


class Reaction:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, reaction: ReactionModel):
        q = "INSERT INTO reactions (emoji, member_id, channel_id) VALUES ('{emoji}', {member_id}, {channel_id})"\
            .format(emoji=reaction.emoji, member_id=reaction.member.id, channel_id=reaction.channel.id)
        self.db.execute(q)
