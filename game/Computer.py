class Computer:
    def __init__(self, tile=None, quick=True):
        self.tile = tile
        self.quick = quick

    def __repr__(self):
        return "<Computer - tile: {}>".format(self.tile)

    def get_move(self, board, tile=None):
        pass
