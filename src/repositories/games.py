from src.models.database.game import Game as GameModel
from psycopg import cursor


class Game:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, game: GameModel):
        q = "INSERT INTO games (id, name) VALUES ({id}, '{name}') ON CONFLICT DO NOTHING".format(id=game.id, name=game.name)
        self.db.execute(q)
