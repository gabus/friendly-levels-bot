from src.models.database.guild import Guild


class LevelWeights:

    def __init__(self, guild: Guild, message_weight: float, reaction_weight: float, voip_weight: float):
        self.guild = guild
        self.message_weight = message_weight
        self.reaction_weight = reaction_weight
        self.voip_weight = voip_weight

    def as_dict(self) -> dict:
        return {
            "guild": self.guild.as_dict(),
            "message_weight": self.message_weight,
            "reaction_weight": self.reaction_weight,
            "voip_weight": self.voip_weight
        }
