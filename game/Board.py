import copy


def reset_board(old_board):
    for x in range(8):
        for y in range(8):
            old_board[x][y] = ' '

    old_board[3][3] = 'O'
    old_board[3][4] = 'X'
    old_board[4][3] = 'X'
    old_board[4][4] = 'O'
    return old_board


def get_new_board():
    board_array = []
    for i in range(8):
        board_array.append([' '] * 8)

    board_array = reset_board(board_array)
    return board_array


def on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


class Board:
    def __init__(self, board_array=None):
        self.board_array = board_array if board_array is not None else get_new_board()

    def get_score(self):
        score = 0
        for row in self.board_array:
            for item in row:
                if item == 'X':
                    score += 1
                elif item == 'O':
                    score -= 1
        return score

    def get_board_with_hints(self, tile):
        board_copy = self.copy_board()
        board_copy = Board(board_copy)
        for x, y in board_copy.get_valid_moves(tile):
            board_copy.board_array[x][y] = '.'
        return board_copy

    def draw_board(self):
        h_line = '  +---+---+---+---+---+---+---+---+'
        print(h_line)
        for y in range(8):
            print("%d" % (y + 1), end=' ')
            for x in range(8):
                print('| %s' % self.board_array[x][y]),
            print('|')
            print(h_line)
        print('    1   2   3   4   5   6   7   8')

    def copy_board(self):
        return copy.deepcopy(self.board_array)

    def check_valid_move_with_flips(self, tile, x_start, y_start):
        """Checks from a starting position every possible space near it with an enemy tile
           and returns a list of tiles to be flipped along all lines of enemy tiles, if any."""
        board = self.copy_board()
        if self.board_array[x_start][y_start] != " " or not on_board(x_start, y_start):
            return False
        board[x_start][y_start] = tile

        if tile == 'X':
            other_tile = 'O'
        else:
            other_tile = 'X'

        tiles_to_flip = []
        for x_dir, y_dir in [[0, 1], [1, 0], [1, 1], [1, -1], [0, -1], [-1, 0], [-1, -1], [-1, 1]]:
            x, y = x_start, y_start
            x += x_dir
            y += y_dir
            if on_board(x, y) and board[x][y] == other_tile:
                x += x_dir
                y += y_dir
                if not on_board(x, y):
                    continue
                while board[x][y] == other_tile:
                    x += x_dir
                    y += y_dir
                    if not on_board(x, y):
                        break
                if not on_board(x, y):
                    continue
                if board[x][y] == tile:
                    while True:
                        x -= x_dir
                        y -= y_dir
                        if x == x_start and y == y_start:
                            break
                        tiles_to_flip.append([x, y])
        return tiles_to_flip

    def get_valid_moves(self, tile):
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.check_valid_move_with_flips(tile, x, y):
                    valid_moves.append([x, y])
        return valid_moves

    def get_board_with_valid_moves(self, tile):
        board_copy = self.copy_board()

        for x, y in self.get_valid_moves(tile):
            board_copy[x][y] = '.'
        return Board(board_copy)

    def make_move(self, tile, x_start, y_start):
        copy_board = Board(self.copy_board())
        flip_tiles = copy_board.check_valid_move_with_flips(tile, x_start, y_start)

        if not flip_tiles:
            return False

        copy_board.board_array[x_start][y_start] = tile
        for x, y in flip_tiles:
            copy_board.board_array[x][y] = tile
        return copy_board
