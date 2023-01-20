from src.models.database.level_weights import LevelWeights as LevelWeightsModel
from src.repositories.serializers.level_weights import LevelWeights as LevelWeightsSerializer
from psycopg import cursor


class LevelWeights:

    def __init__(self, db: cursor):
        self.db = db

    def create(self, guild_id) -> LevelWeightsModel:
        q = "INSERT INTO level_weights (guild_id) VALUES ({guild_id}) ON CONFLICT DO NOTHING".format(guild_id=guild_id)
        self.db.execute(q)
        return self.get(guild_id)

    def get(self, guild_id: int) -> LevelWeightsModel:
        q = """
            SELECT lw.message_weight, lw.reaction_weight, lw.voip_weight, lw.playing_weight,
            g.id as guild_id, g.name as guild_name  
            FROM level_weights lw 
            LEFT JOIN guilds g on g.id = lw.guild_id
            WHERE guild_id = {}
        """.format(guild_id)
        self.db.execute(q)

        self.db.execute(q)
        db_row = self.db.fetchone()

        return LevelWeightsSerializer(db_row).serialize()

    def set_message_weight(self, guild_id, weight):
        q = """
            UPDATE level_weights SET message_weight = {weight} WHERE guild_id={guild_id}
        """.format(guild_id=guild_id, weight=weight)
        self.db.execute(q)

    def set_reaction_weight(self, guild_id, weight):
        q = """
            UPDATE level_weights SET reaction_weight = {weight} WHERE guild_id={guild_id}
        """.format(guild_id=guild_id, weight=weight)
        self.db.execute(q)

    def set_voip_weight(self, guild_id, weight):
        q = """
            UPDATE level_weights SET voip_weight = {weight} WHERE guild_id={guild_id}
        """.format(guild_id=guild_id, weight=weight)
        self.db.execute(q)

    def set_playing_weight(self, guild_id, weight):
        q = """
            UPDATE level_weights SET playing_weight = {weight} WHERE guild_id={guild_id}
        """.format(guild_id=guild_id, weight=weight)
        self.db.execute(q)
