import pygame as pg
import sys
import random
sys.path.append('../engine')
from scripts.core.mainEngine import MainEngine
from scripts.renderItem import RenderItem
from scripts.core.settings import *
from scripts.colors import *

class VUILib:

    @staticmethod
    def create_static_vui(position: tuple, center: bool, size: tuple, elements: list, convert_alpha: bool, layer: int): # returns a complete RenderItem object in case you don't need the raw pygame surface; tldr: minimize your damn work
        vui_surface = VUILib.create_dynamic_vui(position, size, "temp_dynamic_vui_surface", elements, convert_alpha) ## the name doesn't matter here
        return VUILib.prepare_static_vui(position, center, vui_surface, layer)

    @staticmethod
    def create_dynamic_vui(position: tuple, size: tuple, name: str, elements: list, convert_alpha: bool): # returns a surface with given elements drawn onto
        vui_surface = pg.Surface(size) # btw the first element should be the background(color)
        for el in elements: # elements should be flatplane objects (at least for now)
            vui_surface.blit(el[0], el[1])

        if convert_alpha:
            vui_surface.convert_alpha()

        return [name, vui_surface, position]

    @staticmethod
    def prepare_static_vui(position: tuple, center: bool, dynamic_vui: list, layer: int): # prepares a complete RenderItem object, ready to be drawn onto screen
        if center: # True/False -> determines, if the input position should be taken as a center pos or TLCorner pos
            return RenderItem("sprite", layer, {"sprite":dynamic_vui[1], "rect":(position[0] - dynamic_vui.width // 2, position[1]- dynamic_vui.height // 2, dynamic_vui.width, dynamic_vui.height)})
        else:
            return RenderItem("sprite", layer, {"sprite":dynamic_vui[1], "rect":(position[0], position[1], dynamic_vui[1].get_width(), dynamic_vui[1].get_height())})