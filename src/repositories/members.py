from src.models.member import Member as MemberModel
from psycopg import cursor


class Member:

    def __init__(self, db: cursor):
        self.db = db

    def save(self, member: MemberModel):
        q = "INSERT INTO members (id, name) VALUES ({id}, '{name}') ON CONFLICT DO NOTHING".format(id=member.id, name=member.name)
        self.db.execute(q)
