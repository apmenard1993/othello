from flask import Blueprint, render_template, request

import gameService
from AI import AI
from Board import Board, reset_board
from Human import Human
from Random import Random

game_controller = Blueprint('game_controller', __name__, template_folder='templates')
board = Board()
reset_board(board.boardArray)
players = []
player_types = {
    "Human": Human,
    "Computer (Random)": Random,
    "Computer (AI)": AI,
}


@game_controller.route('/startGame', methods=['POST'])
def start_game():
    global players
    player_one_type = request.form['playerOneType']
    player_two_type = request.form['playerTwoType']

    for i, p_type in enumerate([player_one_type, player_two_type]):
        players.append(player_types.get(p_type))
    print(players)
    # todo: make this a UUID from/saved-to the database
    # create a new board state for that UUID
    # return the UUID
    return "THISISAUUID"


@game_controller.route('/playGame')
def render_game():
    game_id = request.args['id']
    # todo: fetch game state for this UUID and render that
    global board
    return render_template('playGame.html', gameArray=board.boardArray)


@game_controller.route('/submitMove', methods=['POST'])
def submit_move():
    # todo: get the game UUID from the request
    # fetch the game state from the database
    # update the game state and return control to the user
    global board
    move_request = (request.form['i'], request.form['j'])
    board = gameService.update(move_request, board)
    return 'blah'
