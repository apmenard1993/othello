import random


class Random:
    def __init__(self, tile, quick):
        self.tile = tile
        self.quick = quick

    def get_move(self, board):
        if not self.quick:
            print "Press enter to see the computer's move"
            raw_input()
        possible_moves = []
        for x, y in board.get_valid_moves(self.tile):
            possible_moves.append((x, y))

        if not possible_moves:
            return None
        chosen_move = random.choice(possible_moves)
        return chosen_move
