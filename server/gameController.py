from flask import Blueprint, render_template, request

import server.gameService as gameService
# set up blueprint for endpoints
from game.Board import Board

game_controller = Blueprint('game_controller', __name__, template_folder='templates')


# endpoints
@game_controller.route('/startGame', methods=['POST'])
def start_game():
    player_one_type = request.form['playerOneType']
    player_two_type = request.form['playerTwoType']
    game_id = gameService.create_new_game(player_one_type, player_two_type)
    return str(game_id)


@game_controller.route('/playGame/<game_id>')
def render_game(game_id):
    game = gameService.get_game_by_id(int(game_id))
    current_turn = game.active_player
    game_board = Board(game.unpickle_board())
    if not game_board:
        raise FileNotFoundError("Unable to find game with id {}".format(game_id))
    score = game_board.get_score()
    return render_template('playGame.html',
                           gameArray=game_board.board_array,
                           score=score,
                           activePlayer="{} ({})".format(current_turn + 1, 'X' if current_turn == 0 else 'O'))


@game_controller.route('/playGame/<game_id>/submitMove', methods=['POST'])
def submit_move(game_id):
    move_request = (request.form['i'], request.form['j'])
    game = gameService.get_game_by_id(int(game_id))
    if not game:
        raise FileNotFoundError("Unable to find game with id {}".format(game_id))
    update_response = gameService.update(game, move_request)
    if update_response == 'GAME OVER':
        return 'false'
    return 'true'
