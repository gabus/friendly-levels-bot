from src.models.database.member_playing import MemberPlaying as MemberPlayingModel
from src.models.database.member import Member as MemberModel
from src.models.database.game import Game as GameModel
from discord.member import Member as DiscordMember
from discord import Activity as DiscordActivity


class MemberPlaying:

    def __init__(self, activity: DiscordActivity, member: DiscordMember, is_playing: bool):
        self.activity = activity
        self.member = member
        self.is_playing = is_playing

    def serialize(self) -> MemberPlayingModel:
        m = MemberModel(self.member.id, self.member.name)
        g = GameModel(self.activity.application_id, self.activity.name)
        mp = MemberPlayingModel(m, g, self.is_playing)
        return mp
