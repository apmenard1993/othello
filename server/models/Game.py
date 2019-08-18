from database import db


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    player_one_type = db.Column(db.String)
    player_two_type = db.Column(db.String)
    game_state = db.Column(db.LargeBinary)

    def __init__(self, player_one_type, player_two_type, game_state):
        self.player_one_type = player_one_type
        self.player_two_type = player_two_type
        self.game_state = game_state

    def __repr__(self):
        return '<Game: id {}>'.format(self.id)
