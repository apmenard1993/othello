def update(move_request, board):
    moves = board.get_valid_moves('X')
    if moves and moves[0]:
        return board.make_move('X', moves[0][0], moves[0][1])
