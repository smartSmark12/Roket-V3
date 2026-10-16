import pygame as pg

class Level:
    def __init__(self, appInstance, name:str, displayName:str, icon:pg.Surface, importance:int, stages:dict[str, any], requirements:dict, allowedShips:list[str], disallowedShips:list[str]):
        self.app = appInstance
        self.name = name
        self.displayName = displayName
        self.icon = icon if icon is not "" else self.app.sprites["level_icon_default"] # fallback if no icon is specified
        self.importance = importance
        self.stages = stages
        self.requirements = requirements
        self.allowedShips = allowedShips
        self.disallowedShips = disallowedShips

        self._load_icon()

    def _load_icon(self):
        icon = self.icon = self.app.sprite_handler.load_sprite("_level_icon_"+self.name, self.icon, (100, 100), "c", False)

        if icon is None:
            self.icon = self.app.sprites["level_icon_default"]
            print(f"failed to load icon for level {self.displayName} ({self.name})")