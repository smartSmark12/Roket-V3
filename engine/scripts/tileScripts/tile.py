import pygame as pg

class Tile:
    def __init__(self, position: tuple | list, size: tuple, rect: pg.Rect | None, texture) -> None:
        self.pos = position
        self.size = size
        self.rect = rect if not None else pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.texture = texture


Tile((0, 0), (100, 100), None)