from src.models.database.member_playing import MemberPlaying as MemberPlayingModel
from src.models.database.member import Member as MemberModel
from src.models.database.game import Game as GameModel
from discord.member import Member as DiscordMember
from discord import Activity as DiscordActivity
from discord import Game as DiscordGame


class MemberPlaying:

    def __init__(self, activity: DiscordActivity, member: DiscordMember, is_playing: bool):
        self.activity = activity
        self.member = member
        self.is_playing = is_playing

    def serialize(self) -> MemberPlayingModel:
        m = MemberModel(self.member.id, self.member.name)

        if type(self.activity) == DiscordActivity:
            application_id = self.activity.application_id
        else:
            # Mac case: Game object doesn't have ID. Generate one from the Name
            application_id = abs(hash(self.activity.name)) % (10 ** 16)

        g = GameModel(application_id, self.activity.name)
        mp = MemberPlayingModel(m, g, self.is_playing)
        return mp
