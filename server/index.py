from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from game import Display
from game.AI import AI
from game.Board import Board, reset_board
from game.Human import Human
from game.Random import Random

app = Flask(__name__)
Bootstrap(app)
board = Board()
reset_board(board.boardArray)
players = []
player_types = {
    "Human": Human,
    "Computer (Random)": Random,
    "Computer (AI)": AI,
}


def update(move_request):
    global board
    moves = board.get_valid_moves('X')
    if moves and moves[0]:
        board = board.make_move('X', moves[0][0], moves[0][1])


@app.route('/')
def index():
    return render_template('index.html', title="Web Othello", welcomeText=Display.get_intro())


@app.route('/startGame', methods=['POST'])
def start_game():

    print(request.form)
    player_one_type = request.form['playerOneType']
    player_two_type = request.form['playerTwoType']
    global players
    for i, p_type in enumerate([player_one_type, player_two_type]):
        players.append(player_types.get(p_type))
    print(players)
    # todo: make this a UUID from/saved-to the database
    # create a new board state for that UUID
    # return the UUID
    return "THISISAUUID"


@app.route('/playGame')
def render_game():
    game_id = request.args['id']
    # todo: fetch game state for this UUID and render that
    global board
    return render_template('playGame.html', gameArray=board.boardArray)


@app.route('/submitMove', methods=['POST'])
def submit_move():
    # todo: get the game UUID from the request
    # fetch the game state from the database
    # update the game state and return control to the user
    move_request = (request.form['i'], request.form['j'])
    update(move_request)
    return 'blah'


if __name__ == '__main__':
    app.run(port=8080, debug=True)
