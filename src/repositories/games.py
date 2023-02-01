from src.models.database.game import Game as GameModel
from psycopg import cursor


class Game:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, game: GameModel):
        q = "INSERT INTO games (id, name) VALUES ({id}, %s) ON CONFLICT DO NOTHING".format(id=game.id)
        self.db.execute(q, (game.name,))
