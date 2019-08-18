from flask import Blueprint, render_template, request

import server.gameService as gameService
from game.AI import AI
from game.Board import Board, reset_board
from game.Human import Human
from game.Random import Random

# set up blueprint for endpoints
game_controller = Blueprint('game_controller', __name__, template_folder='templates')

# globals
board = Board()
reset_board(board.boardArray)
players = []
player_types = {
    "Human": Human,
    "Computer (Random)": Random,
    "Computer (AI)": AI,
}


# endpoints
@game_controller.route('/startGame', methods=['POST'])
def start_game():
    player_one_type = request.form['playerOneType']
    player_two_type = request.form['playerTwoType']
    game_id = gameService.create_new_game(player_one_type, player_two_type)
    return str(game_id)


@game_controller.route('/playGame')
def render_game():
    game_id = request.args['id']
    game_board = gameService.get_game_by_id(game_id)
    return render_template('playGame.html', gameArray=game_board)


@game_controller.route('/submitMove', methods=['POST'])
def submit_move():
    # todo: get the game UUID from the request
    # fetch the game state from the database
    # update the game state and return control to the user
    global board
    move_request = (request.form['i'], request.form['j'])
    board = gameService.update(move_request, board)
    return 'blah'
