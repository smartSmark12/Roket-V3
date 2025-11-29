import pygame as pg
from scripts.colors import *

class RenderItem:
    def __init__(self, item_type, layer, metadata):
        self.item_type = item_type # sprite, rect, circle, line, aaline, text
        self.layer = layer
        self.metadata = metadata

        if not "dont_repair" in self.metadata:
            self.auto_repair()

    def auto_repair(self):
        match self.item_type:
            case "sprite":
                if "sprite" not in self.metadata:
                    try: self.metadata["sprite"] = pg.Surface((self.metadata["rect"][2], self.metadata["rect"][3]))
                    except:
                        print("huhh???")
                        self.metadata["sprite"] = pg.Surface((100, 100))
                    self.metadata["sprite"].fill(white)
                if type(self.metadata["sprite"]) != pg.surface.Surface:
                    try: self.metadata["sprite"] = pg.Surface(self.metadata["sprite"])
                    except:
                        self.metadata["sprite"] = pg.Surface((100, 100))
                        self.metadata["sprite"].fill(white)
                        print("heh...")
                if "rect" not in self.metadata: self.metadata["rect"] = pg.Rect(10, 10, 100, 100) # posx, posy, scax, scay
                if type(self.metadata["rect"]) != pg.rect.Rect: 
                    try:
                        self.metadata["rect"] = pg.Rect(self.metadata["rect"])
                    except: 
                        self.metadata["rect"] = pg.Rect(10, 10, 100, 100)
                        print("wtf happened??")
            case "rect":
                if "color" not in self.metadata: self.metadata["color"] = white
                if "rect" not in self.metadata: self.metadata["rect"] = pg.Rect(10, 10, 100, 100)
                if type(self.metadata["rect"]) != pg.rect.Rect: 
                    try: self.metadata["rect"] = pg.Rect(self.metadata["rect"]) 
                    except: self.metadata["rect"] = pg.Rect(10, 10, 100, 100)
                if "width" not in self.metadata: self.metadata["width"] = 0
                if "radius" not in self.metadata: self.metadata["radius"] = 0
            case "circle":
                if "color" not in self.metadata: self.metadata["color"] = white
                if "center" not in self.metadata: self.metadata["center"] = (100, 100)
                if "radius" not in self.metadata: self.metadata["radius"] = 50
                if "width" not in self.metadata: self.metadata["width"] = 0
            case "line":
                if "color" not in self.metadata: self.metadata["color"] = white
                if "start" not in self.metadata: self.metadata["start"] = (0, 0)
                if "end" not in self.metadata: self.metadata["end"] = (100, 100)
                if "width" not in self.metadata: self.metadata["width"] = 10
            case "aaline":
                if "color" not in self.metadata: self.metadata["color"] = white
                if "start" not in self.metadata: self.metadata["start"] = (0, 0)
                if "end" not in self.metadata: self.metadata["end"] = (100, 100)
            case "poly":
                if "color" not in self.metadata: self.metadata["color"] = white
                if "points" not in self.metadata: self.metadata["points"] = [(100, 100), (200, 100), (200, 200), (100, 200)]
                if "width" not in self.metadata: self.metadata["width"] = 0
            case "text":
                if "font" not in self.metadata: self.metadata["font"] = pg.font.SysFont("Arial", 40)
                if type(self.metadata["font"]) != pg.font.Font: #type(self.metadata["font"]) != pg.font.SysFont ## not a class?
                    stop = False
                    try: 
                        self.metadata["font"] = pg.font.SysFont(self.metadata["font"][0], self.metadata["font"][1])
                        stop = True
                    except: 
                        self.metadata["font"] = pg.font.SysFont("Arial", 40)
                        stop = True
                    if not stop:
                        try:
                            self.metadata["font"] = pg.font.Font(self.metadata["font"][0], self.metadata["font"][1])
                        except: self.metadata["font"] = pg.font.SysFont("Arial", 40)
                if "text" not in self.metadata: self.metadata["text"] = "you forgor to set the text :>"
                if "antialias" not in self.metadata: self.metadata["antialias"] = False
                if "color" not in self.metadata: self.metadata["color"] = white
                if "bgcolor" not in self.metadata: self.metadata["bgcolor"] = black
                if "rect" not in self.metadata: self.metadata["rect"] = pg.Rect(10, 10, 100, 100)