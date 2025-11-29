from scripts.tileScripts.tile import Tile

class Region: # region is 3x3 tiles; a bit like chunk in MC
    def __init__(self, position: tuple, tiles: list) -> None:
        self.position = position
        self.tiles = tiles
        self.get_size()

    def get_size(self):
        self.size = 0
        for i in range(3):
            self.size += self.tiles[i].size