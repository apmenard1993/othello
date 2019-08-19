import random

from game.Computer import Computer


class Random(Computer):

    def __repr__(self):
        return "<Random - tile: {}>".format(self.tile)

    def get_move(self, board, tile=None):
        if tile is None:
            tile = self.tile
        if not self.quick:
            print("Press enter to see the computer's move")
            input()
        possible_moves = board.get_valid_moves(tile)
        if not possible_moves:
            return None
        chosen_move = random.choice(possible_moves)
        return chosen_move
