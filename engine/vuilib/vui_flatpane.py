import pygame as pg
from scripts.colors import *
""" from scripts.datablock import Datablock """

class flatpane: # just for displaying images or colors; for backgrounds/graphics/buttons of vui
    def __init__(self, dtype: str, sprite_list: dict, **kwargs): # display type (color, image), dictionary, from where sprites should be referenced, keyword args for sprite name/color
        self.dtype = dtype
        self.sprite = None # gets created later in code
        self.meta = {}
        
        # assign color or image reference
        for key, value in kwargs.items():
            self.meta[key] = value

        # assign position if given
        try:
            self.position = self.meta["position"]
        except:
            try:
                sprite_error_name = self.meta["sprite"]
                print(f"{__name__}: Warning: no positional arguments given ({sprite_error_name})") # self.app.ext_append_to_log
            except:
                print(f"{__name__}: Warning: no positional arguments given (no_sprite_name)")
                

        if self.dtype in ["color", "col", "c", "colour"]: # this is just some dumb shis i don't remember writing, so..
            if "size" in self.meta:
                self.sprite = pg.Surface(self.meta["size"])
            else:
                self.sprite = pg.Surface((100, 100))
            if "color" in self.meta:
                self.sprite.fill(self.meta["color"])
            else:
                self.sprite.fill(white)

        elif self.dtype in ["sprite", "image", "img"]:
            if "sprite" in self.meta:
                try:
                    self.sprite = sprite_list[self.meta["sprite"]]
                except:
                    # handle printing errors
                    sprite_error_name = self.meta["sprite"]
                    print(f"{__name__}: Couldn't find sprite '{sprite_error_name}'")

                    self.sprite = pg.Surface((100, 100))
                    self.sprite.fill(white)
            else:
                print(f"{__name__}: display-type set to 'sprite', but none was assigned")
                self.sprite = pg.Surface((100, 100))
                self.sprite.fill(white)