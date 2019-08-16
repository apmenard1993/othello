from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from game.Board import Board, reset_board

app = Flask(__name__)
Bootstrap(app)
board = Board()
reset_board(board.boardArray)


def update(move_request):
    global board
    moves = board.get_valid_moves('X')
    if moves and moves[0]:
        board = board.make_move('X', moves[0][0], moves[0][1])


@app.route('/')
def index():
    # todo: save a UUID to a database (SQLite probably)
    # create a new board state for that UUID
    # render that board state
    return render_template('index.html', gameArray=board.boardArray)


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
