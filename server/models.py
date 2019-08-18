from app import db
from sqlalchemy.dialects.postgresql import UUID


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    player_one_type = db.Column(db.String)
    player_two_type = db.Column(db.String)

    def __init__(self, player_one_type, player_two_type):
        self.player_one_type = player_one_type
        self.player_two_type = player_two_type

    def __repr__(self):
        return '<Game: id {} - UUID {}>'.format(self.id, self.uuid)
