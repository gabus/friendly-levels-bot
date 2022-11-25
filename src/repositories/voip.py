from src.models.voip import Voip as VoipModel
from psycopg import cursor
from loguru import logger
from src.repositories.serializers.voip import Voip as VoipSerializer


class Voip:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, voip: VoipModel):
        q = "INSERT INTO voip (voip_channel_id, is_open, duration_time, member_id, guild_id) " \
            "VALUES ({voip_channel_id}, {is_open}, {duration_time}, {member_id}, {guild_id})"\
            .format(voip_channel_id=voip.voip_channel_id, is_open=voip.is_open, duration_time=voip.duration_time, member_id=voip.member.id, guild_id=voip.guild.id)
        self.db.execute(q)

    def update_is_open(self, voip: VoipModel, new_is_open: bool):

        q = "UPDATE voip SET is_open = {new_is_open} WHERE voip_channel_id={voip_channel_id} AND member_id={member_id} AND is_open={is_open}"\
            .format(new_is_open=new_is_open, voip_channel_id=voip.voip_channel_id, member_id=voip.member.id, is_open=voip.is_open)
        self.db.execute(q)

    def get(self, voip_channel_id: int, member_id: int, is_open: bool) -> VoipModel:
        q = """
            select v.voip_channel_id, v.is_open, v.duration_time, 
            g.id as guild_id, g.name as guild_name, 
            m.id as member_id, m.name as member_name 
            from voip v
            left join members m on m.id = v.member_id 
            left join guilds g on g.id = v.guild_id 
            where v.voip_channel_id = {voip_channel_id}
            and v.is_open = {is_open}
            and v.member_id = {member_id}
        """.format(voip_channel_id=voip_channel_id, member_id=member_id, is_open=is_open)

        self.db.execute(q)
        db_row = self.db.fetchone()
        return VoipSerializer(db_row).serialize()




