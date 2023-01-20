from src.models.database.member_playing import MemberPlaying as MemberPlayingModel
from psycopg import cursor


class MemberPlaying:

    def __init__(self, db: cursor):
        self.db = db

    def start_game(self, member_playing: MemberPlayingModel):
        q = """
            INSERT INTO member_playing (member_id, game_id, duration_time, is_playing) 
            VALUES ({member_id}, {game_id}, {duration_time}, {is_playing}) 
            ON CONFLICT DO NOTHING
        """.format(
            member_id=member_playing.member.id,
            game_id=member_playing.game.id,
            duration_time=member_playing.duration_time,
            is_playing=member_playing.is_playing
        )
        self.db.execute(q)

    def stop_game(self, member_playing: MemberPlayingModel):
        q = """
            UPDATE member_playing SET is_playing = False 
            WHERE member_id = {member_id}
            AND game_id = {game_id}
            AND is_playing = True 
        """.format(
            member_id=member_playing.member.id,
            game_id=member_playing.game.id,
        )
        self.db.execute(q)

    def session_exits(self, member_playing: MemberPlayingModel) -> bool:
        q = """
            select *
            from member_playing
            WHERE member_id = {member_id}
            AND game_id = {game_id}
            AND is_playing = {is_playing} 
        """.format(
            member_id=member_playing.member.id,
            game_id=member_playing.game.id,
            is_playing=member_playing.is_playing
        )

        self.db.execute(q)
        db_row = self.db.fetchone()

        if not db_row:
            return False

        return True
