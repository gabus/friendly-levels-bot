from src.models.database.voip import Voip as VoipModel
from src.models.database.member import Member as MemberModel
from src.models.database.guild import Guild as GuildModel


class Voip:

    def __init__(self, db_voip: dict):
        self.db_voip = db_voip

    def serialize(self) -> VoipModel:
        m = MemberModel(self.db_voip['member_id'], self.db_voip['member_name'])
        g = GuildModel(self.db_voip['guild_id'], self.db_voip['guild_name'])
        v = VoipModel(self.db_voip['voip_channel_id'], self.db_voip['is_open'], m, g)
        return v
