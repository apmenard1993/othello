import pickle

from database import db


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    player_one_type = db.Column(db.String)
    player_two_type = db.Column(db.String)
    game_state = db.Column(db.LargeBinary)
    active_player = db.Column(db.Integer)

    def __init__(self, player_one_type, player_two_type, game_state, active_player=0):
        self.player_one_type = player_one_type
        self.player_two_type = player_two_type
        self.game_state = game_state
        self.active_player = 1 if active_player != 0 else 0

    def __repr__(self):
        return '<Game: id {}>'.format(self.id)

    def unpickle_board(self):
        if self.game_state is not None:
            return pickle.loads(self.game_state)
        return None
