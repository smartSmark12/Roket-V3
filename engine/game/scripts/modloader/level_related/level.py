import pygame as pg

class Level:
    def __init__(self, appInstance, displayName:str, icon:pg.Surface, stages:dict[str, any], requirements:dict, allowedShips:list[str], disallowedShips:list[str]):
        self.app = appInstance
        self.displayName = displayName
        self.icon = icon if icon is not None else self.app.sprites["level_icon_default"] # fallback if no icon is specified
        self.stages = stages
        self.requirements = requirements
        self.allowedShips = allowedShips
        self.disallowedShips = disallowedShips