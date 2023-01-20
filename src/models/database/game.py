class Game:

    def __init__(self, game_id: int, game_name: str):
        self.id = game_id
        self.name = game_name

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
