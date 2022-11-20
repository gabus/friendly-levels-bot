import enum
from src.utils import datetime_util


class StatsType(enum.Enum):
    chat = "CHAT"          # counter
    reaction = "REACTION"  # counter
    voip = "VOIP"          # in seconds
    playing = "PLAYING"    # in seconds


class Storage:

    def __init__(self):
        self.db = {}
        # database_example = {
        #     "723176453130420295:": {          # guild_id
        #         "2022-11-19": {               # date
        #             "471454507566366720:": {  # member_id
        #                 "CHAT": 46551,
        #                 "REACTION": 234525,
        #                 "VOIP": 234,
        #                 "PLAYING": 234,
        #             }
        #         }
        #     }
        # }

    def add_stats(self, guild: int, member: int, stat_type: StatsType, value: int):
        if guild not in self.db:
            self.db[guild] = {}

        today = str(datetime_util.today())
        if today not in self.db[guild]:
            self.db[guild][today] = {}

        if member not in self.db[guild][today]:
            self.db[guild][today][member] = {
                StatsType.chat.value: 0,
                StatsType.voip.value: 0,
                StatsType.reaction.value: 0,
                StatsType.playing.value: 0,
            }

        self.db[guild][today][member][stat_type.value] += value

    def get_stats_for_member(self, guild, member):
        ret = {
            guild: {
                member: {
                    StatsType.chat.value: 0,
                    StatsType.voip.value: 0,
                    StatsType.reaction.value: 0,
                    StatsType.playing.value: 0,
                }
            }
        }

        for day_string, obj in self.db[guild].items():
            if member in obj:
                ret[guild][member][StatsType.chat.value] += obj[member][StatsType.chat.value]
                ret[guild][member][StatsType.voip.value] += obj[member][StatsType.voip.value]
                ret[guild][member][StatsType.reaction.value] += obj[member][StatsType.reaction.value]
                ret[guild][member][StatsType.playing.value] += obj[member][StatsType.playing.value]

        return ret

    def get_stats_for_guild(self, guild):
        if guild not in self.db:
            return None

        return self.db[guild]


