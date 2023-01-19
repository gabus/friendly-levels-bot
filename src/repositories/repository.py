from src.repositories.guilds import Guild
from src.repositories.chennals import Channel
from src.repositories.members import Member
from src.repositories.messages import Message
from src.repositories.reaction import Reaction
from src.repositories.voip import Voip
from src.repositories.stats import Stats
from src.repositories.level_weights import LevelWeights
from psycopg import cursor


class Repository:

    def __init__(self, db: cursor):
        self.guild = Guild(db)
        self.channel = Channel(db)
        self.member = Member(db)
        self.message = Message(db)
        self.reaction = Reaction(db)
        self.voip = Voip(db)
        self.stats = Stats(db)
        self.level_weights = LevelWeights(db)
