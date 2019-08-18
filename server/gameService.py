import pickle

from database import db
from game.Board import get_new_board
from server.models.Game import Game


def update(move_request, board):
    moves = board.get_valid_moves('X')
    if moves and moves[0]:
        return board.make_move('X', moves[0][0], moves[0][1])


def create_new_game(player_one_type, player_two_type):
    initial_game_state = pickle.dumps(get_new_board(), protocol=4)
    new_game = Game(player_one_type, player_two_type, initial_game_state)
    db.session.add(new_game)
    db.session.commit()

    return new_game.id


def get_game_by_id(game_id):
    game = Game.query.filter_by(id=game_id).first()
    return pickle.loads(game.game_state)
