class Member:

    def __init__(self, member_id: int, member_name: str):
        self.id = member_id
        self.name = member_name

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
