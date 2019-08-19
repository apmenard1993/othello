import pickle

from database import db
from game.AI import AI
from game.Board import get_new_board, Board
from game.Human import Human
from game.Random import Random
from server.models.Game import Game

# todo: fix this - right now if both players are the same type things are weird with the tile
player_types = {
    "Human": Human(),
    "Computer (Random)": Random(),
    "Computer (AI)": AI(),
}


def update(game, move_request=None):
    active_turn = int(game.active_player)
    active_player_type = game.player_one_type if active_turn == 0 else game.player_two_type
    next_turn = int(not active_turn)
    next_player_type = game.player_one_type if next_turn == 0 else game.player_two_type

    active_player = player_types[active_player_type]
    active_player.tile = get_tile_for_player_turn(active_turn)
    next_player = player_types[next_player_type]
    next_player.tile = get_tile_for_player_turn(next_turn)

    board = Board(game.unpickle_board())
    active_valid_moves = board.get_valid_moves(active_player.tile)
    next_valid_moves = board.get_valid_moves(next_player.tile)

    print(active_turn, active_player_type, active_player, get_tile_for_player_turn(active_turn))
    print(next_turn, next_player_type, next_player, get_tile_for_player_turn(next_turn))
    if not active_valid_moves and not next_valid_moves:
        return 'GAME OVER'
    if active_valid_moves:
        board = make_move(active_player, board, move_request)
        if not board:
            return 'BAD INPUT'
    if isinstance(next_player, Human):
        update_game(game, board, next_turn)
        return 'NEED INPUT'
    update(update_game(game, board, next_turn))


def make_move(active_player, board, move_request):
    if isinstance(active_player, Human):
        board = board.make_move(active_player.tile, int(move_request[0]), int(move_request[1]))
    else:
        chosen_move = active_player.get_move(board)
        board = board.make_move(active_player.tile, chosen_move[0], chosen_move[1])
    return board


def create_new_game(player_one_type, player_two_type):
    initial_game_state = pickle.dumps(get_new_board(), protocol=4)
    new_game = Game(player_one_type, player_two_type, initial_game_state)
    db.session.add(new_game)
    db.session.commit()

    return new_game.id


def update_game(game, new_board=None, active_player=None):
    if new_board is not None:
        game.game_state = pickle.dumps(new_board.board_array, protocol=4)
    if active_player is not None:
        game.active_player = int(active_player)
    db.session.add(game)
    db.session.commit()
    return game


def get_game_by_id(game_id):
    return Game.query.filter_by(id=game_id).first()


def get_board_array_by_game_id(game_id):
    game = Game.query.filter_by(id=game_id).first()
    return game.unpickle_board()


def get_tile_for_player_turn(turn_int):
    return 'X' if turn_int == 0 else 'O'
