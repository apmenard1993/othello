from Display import get_other_player


class AI:
    def __init__(self, tile, quick, num_moves=4):
        self.tile = tile
        self.depth = num_moves
        self.quick = quick

    def get_move(self, board):
        if not self.quick:
            print "Press enter to see the computer's move"
            raw_input()
        return self.get_best_move(board, self.tile, self.depth)

    def get_best_move(self, board, tile, depth):
        best_move = None
        max_eval = float('-infinity')

        player = tile
        possible_moves = board.get_valid_moves(player)
        if possible_moves:
            best_move = possible_moves[0]
        alpha = float('infinity')

        for x, y in possible_moves:
            new_board = board.make_move(player, x, y)
            alpha = -self.alpha_beta(new_board, float('-infinity'), alpha, depth - 1, get_other_player(player))

            if alpha > max_eval:
                max_eval = alpha
                best_move = (x, y)

        return best_move

    def alpha_beta(self, board, alpha, beta, depth, player):
        if depth == 0:
            return board.evaluate_state(player)

        possible_moves = board.get_valid_moves(player)
        for x, y in possible_moves:
            new_board = board.make_move(player, x, y)
            current_alpha = -self.alpha_beta(new_board, -beta, -alpha, depth - 1, get_other_player(player))

            if current_alpha >= beta:
                return beta

            if current_alpha > alpha:
                alpha = current_alpha

        return alpha
