from game.Computer import Computer
from game.Display import get_other_player

CORNER_WEIGHT = 1000
TILE_WEIGHT = 10
MOVE_WEIGHT = 100


class AI(Computer):
    def __init__(self, tile=None, quick=True, depth=4):
        Computer.__init__(self, tile, quick)
        self.depth = depth

    def __repr__(self):
        return "<AI - tile: {} - quick: {} - depth: {}>".format(self.tile, self.quick, self.depth)

    def get_move(self, board, tile=None):
        if tile is None:
            tile = self.tile
        if not self.quick:
            print("Press enter to see the computer's move")
            input()
        return self.get_best_move(board, tile, self.depth)

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
            return self.evaluate_state(board, player)

        possible_moves = board.get_valid_moves(player)
        for x, y in possible_moves:
            new_board = board.make_move(player, x, y)
            current_alpha = -self.alpha_beta(new_board, -beta, -alpha, depth - 1, get_other_player(player))

            if current_alpha >= beta:
                return beta

            if current_alpha > alpha:
                alpha = current_alpha

        return alpha

    @staticmethod
    def evaluate_state(board, player):
        other_tile = get_other_player(player)

        # check corners, total number of tiles, number of available moves
        value = 0

        # check corners
        my_corners = 0
        opp_corners = 0
        for x, y in [[0, 0], [0, 7], [7, 0], [7, 7]]:
            if board.board_array[x][y] == player:
                my_corners += 1
            elif board.board_array[x][y] == other_tile:
                opp_corners += 1

        corners = (CORNER_WEIGHT * (my_corners - opp_corners))

        # check total number of tiles
        my_total = 0
        opp_total = 0
        for row in board.board_array:
            for space in row:
                if space == player:
                    my_total += 1
                elif space == other_tile:
                    opp_total += 1
        tiles = (TILE_WEIGHT * (my_total - opp_total))

        # check number of available next moves
        my_moves = len(board.get_valid_moves(player))
        opp_moves = len(board.get_valid_moves(other_tile))

        moves = (MOVE_WEIGHT * (my_moves - opp_moves))
        value = corners + tiles + moves
        return value
