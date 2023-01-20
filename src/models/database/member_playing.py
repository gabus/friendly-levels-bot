from src.models.database.member import Member
from src.models.database.game import Game


class MemberPlaying:

    def __init__(self, member: Member, game: Game, is_playing: bool, duration_time: int = 0):
        self.member = member
        self.game = game
        self.is_playing = is_playing
        self.duration_time = duration_time

    def as_dict(self) -> dict:
        return {
            'member': self.member.as_dict(),
            'game': self.game.as_dict(),
            'is_playing': self.is_playing,
            'duration_time': self.duration_time
        }
