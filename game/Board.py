import copy


class Board:
    def __init__(self, board_array=None):
        self.boardArray = board_array if board_array is not None else self.get_new_board()

    def get_new_board(self):
        board_array = []
        for i in range(8):
            board_array.append([' '] * 8)

        board_array = self.reset_board(board_array)
        return board_array

    def test_board(self):
        board = []

        eighth = ['X', 'X', 'X', 'X', 'X', 'X', 'O', 'X']
        seventh = ['X', 'X', 'X', 'X', 'X', 'O', 'O', 'X']
        sixth = ['X', 'O', 'X', 'X', 'O', 'X', 'O', ' ']
        fifth = ['X', 'O', 'O', 'X', 'X', 'X', 'O', ' ']
        fourth = ['X', 'O', 'O', 'O', 'X', 'X', 'O', ' ']
        third = ['X', 'X', 'O', 'X', 'O', 'O', 'X', 'X']
        second = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
        first = ['X', 'X', 'X', 'X', 'X', 'X', ' ', 'X']

        first_column = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
        second_column = ['X', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
        third_column = ['X', 'X', 'O', 'O', 'O', 'X', 'X', 'X']
        fourth_column = ['X', 'X', 'X', 'O', 'X', 'X', 'X', 'X']
        fifth_column = ['X', 'X', 'O', 'X', 'X', 'O', 'X', 'X']
        sixth_column = ['X', 'X', 'O', 'X', 'X', 'X', 'O', 'X']
        seventh_column = [' ', 'X', 'X', 'O', 'O', 'O', 'O', 'O']
        eighth_column = ['X', 'X', 'X', ' ', ' ', ' ', 'X', 'X']

        board.append(first_column)
        board.append(second_column)
        board.append(third_column)
        board.append(fourth_column)
        board.append(fifth_column)
        board.append(sixth_column)
        board.append(seventh_column)
        board.append(eighth_column)
        # board.reverse()
        # for row in board:
        #    row.reverse()
        return Board(board)

    def reset_board(self, old_board):
        for x in range(8):
            for y in range(8):
                old_board[x][y] = ' '

        old_board[3][3] = 'O'
        old_board[3][4] = 'X'
        old_board[4][3] = 'X'
        old_board[4][4] = 'O'
        return old_board

    def get_score(self):
        score = 0
        for row in self.boardArray:
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
            board_copy.boardArray[x][y] = '.'
        return board_copy

    def draw_board(self):
        h_line = '  +---+---+---+---+---+---+---+---+'
        print(h_line)
        for y in range(8):
            print "%d" % (y + 1),
            for x in range(8):
                print('| %s' % self.boardArray[x][y]),
            print('|')
            print(h_line)
        print('    1   2   3   4   5   6   7   8')

    def copy_board(self):
        return copy.deepcopy(self.boardArray)

    def check_valid_move_with_flips(self, tile, x_start, y_start):
        """Checks from a starting position every possible space near it with an enemy tile
           and returns a list of tiles to be flipped along all lines of enemy tiles, if any."""
        board = self.copy_board()
        if self.boardArray[x_start][y_start] != " " or not self.on_board(x_start, y_start):
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
            if self.on_board(x, y) and board[x][y] == other_tile:
                x += x_dir
                y += y_dir
                if not self.on_board(x, y):
                    continue
                while board[x][y] == other_tile:
                    x += x_dir
                    y += y_dir
                    if not self.on_board(x, y):
                        break
                if not self.on_board(x, y):
                    continue
                if board[x][y] == tile:
                    while True:
                        x -= x_dir
                        y -= y_dir
                        if x == x_start and y == y_start:
                            break
                        tiles_to_flip.append([x, y])
        return tiles_to_flip

    def on_board(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

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

        copy_board.boardArray[x_start][y_start] = tile
        for x, y in flip_tiles:
            copy_board.boardArray[x][y] = tile
        return copy_board

