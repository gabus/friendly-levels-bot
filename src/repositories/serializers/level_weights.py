from src.models.database.level_weights import LevelWeights as LevelWeightsModel
from src.models.database.guild import Guild as GuildModel


class LevelWeights:

    def __init__(self, level_weights: dict):
        self.level_weights = level_weights

    def serialize(self) -> LevelWeightsModel:
        g = GuildModel(self.level_weights['guild_id'], self.level_weights['guild_name'])
        lv = LevelWeightsModel(
            g,
            self.level_weights['message_weight'],
            self.level_weights['reaction_weight'],
            self.level_weights['voip_weight']
        )
        return lv
