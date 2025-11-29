import pygame as pg
from scripts.colors import *

class RenderItem:

    __allowed = ("sprite",
                 "rect",
                 "color",
                 "width",
                 "radius",
                 "center",
                 "start",
                 "end",
                 "text",
                 "font",
                 "antialias",
                 "bgcolor",
                 "points")

    def __init__(self, item_type, layer, **kwargs): # metadata passed as a dict instead of **kwargs
        self.item_type = item_type # sprite, rect, circle, line, aaline, text
        self.layer = layer
    
        for key, value in kwargs.iteritems():
            if key in self.__class__.__allowed:
                setattr(self, key, value)
            else:
                print("wrong key attribute, old pal")

        if not hasattr(self, "dont_repair"):
            self.auto_repair()

    def auto_repair(self):
        match self.item_type:
            case "sprite":
                if not hasattr(self, "sprite"):
                    try: self.sprite = pg.Surface((self.rect[2], self.rect[3]))
                    except:
                        print("huhh???")
                        self.sprite = pg.Surface((100, 100))
                    self.sprite.fill(white)
                if type(self.sprite) != pg.surface.Surface:
                    try: self.sprite = pg.Surface(self.sprite)
                    except:
                        self.sprite = pg.Surface((100, 100))
                        self.sprite.fill(white)
                        print("heh...")
                if not hasattr(self, "rect"): self.rect = pg.Rect(10, 10, 100, 100) # posx, posy, scax, scay
                if type(self.rect) != pg.rect.Rect: 
                    try:
                        self.rect = pg.Rect(self.rect)
                    except: 
                        self.rect = pg.Rect(10, 10, 100, 100)
                        print("wtf happened??")
            case "rect":
                if not hasattr(self, "color"): self.color = white
                if not hasattr(self, "rect"): self.rect = pg.Rect(10, 10, 100, 100)
                if type(self.rect) != pg.rect.Rect: 
                    try: self.rect = pg.Rect(self.rect) 
                    except: self.rect = pg.Rect(10, 10, 100, 100)
                if not hasattr(self, "width"): self.width = 0
                if not hasattr(self, "radius"): self.radius = 0
            case "circle":
                if not hasattr(self, "color"): self.color = white
                if not hasattr(self, "center"): self.center = (100, 100)
                if not hasattr(self, "radius"): self.radius = 50
                if not hasattr(self, "width"): self.width = 0
            case "line":
                if not hasattr(self, "color"): self.color = white
                if not hasattr(self, "start"): self.start = (0, 0)
                if not hasattr(self, "end"): self.end = (100, 100)
                if not hasattr(self, "width"): self.width = 10
            case "aaline":
                if not hasattr(self, "color"): self.color = white
                if not hasattr(self, "start"): self.start = (0, 0)
                if not hasattr(self, "end"): self.end = (100, 100)
            case "poly":
                if not hasattr(self, "color"): self.color = white
                if not hasattr(self, "points"): self.points = [(100, 100), (200, 100), (200, 200), (100, 200)]
                if not hasattr(self, "width"): self.width = 0
            case "text":
                if not hasattr(self, "font"): self.font = pg.font.SysFont("Arial", 40)
                if type(self.font) != pg.font.SysFont or type(self.font) != pg.font.Font:
                    self.stop = False
                    try: 
                        self.font = pg.font.SysFont(self.font[0], self.font[1])
                        self.stop = True
                    except: 
                        self.font = pg.font.SysFont("Arial", 40)
                        self.stop = True
                    if not self.stop:
                        try:
                            self.font = pg.font.Font(self.font[0], self.font[1])
                        except: self.font = pg.font.SysFont("Arial", 40)
                if not hasattr(self, "text"): self.text = "default_text"
                if not hasattr(self, "antialias"): self.antialias = False
                if not hasattr(self, "color"): self.color = white
                if not hasattr(self, "bgcolor"): self.bgcolor = black
                if not hasattr(self, "rect"): self.rect = pg.Rect(10, 10, 100, 100)