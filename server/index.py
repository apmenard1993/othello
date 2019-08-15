from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from game import Display
from game.Board import Board

app = Flask(__name__)
Bootstrap(app)
board = Board()
board.reset_board(board.boardArray)

#todo: make submit_move
def update():
    moves = board.get_valid_moves('X')
    board.boardArray = board.make_move('X', moves[0][0], moves[0][1]).boardArray


@app.route('/')
def index():
    return render_template('index.html', gameArray=board.boardArray)


@app.route('/submitMove', methods=['POST'])
def submit_move():
    update()
    return 'blah'


if __name__ == '__main__':
    app.run(port=8080, debug=True)
