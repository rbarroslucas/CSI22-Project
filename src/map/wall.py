from map.tile import Tile

class Wall(Tile):
    def __init__(self, path, pos, groups):
        super().__init__(path, pos, groups)
