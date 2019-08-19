class Human:
    def __init__(self, tile=None):
        self.tile = tile

    def get_move(self, board, tile=None):
        if tile is None:
            tile = self.tile
        one_through_eight = '1 2 3 4 5 6 7 8'.split()
        possible_moves = []
        for x, y in board.get_valid_moves(tile):
            possible_moves.append((x, y))

        if not possible_moves:
            return None

        while True:

            print("Enter your move's x coordinate, or type quit to end the game.")
            move_x = input().lower()

            if move_x == 'quit':
                return 'quit'

            print("Enter your move's y coordinate.")
            move_y = input().lower()
            if move_x in one_through_eight and move_y in one_through_eight:
                x = int(move_x) - 1
                y = int(move_y) - 1

                if not board.check_valid_move_with_flips(tile, x, y):
                    print("You can't move there, try again")
                    continue
                else:
                    break

            else:
                print("That is not a valid move. Type just the x digit (or quit) followed by a return, and just the"
                      " y digit followed by a return")
                print("Example: 8\n1\nwill result in the very top right corner.")

        return x, y
