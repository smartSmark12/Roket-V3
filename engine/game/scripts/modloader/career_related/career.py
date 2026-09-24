import pygame as pg

class Career:
    def __init__(self, appInstance, displayName:str, icon:pg.Surface, levels:list[str], reqBeatenLevels:list[str], reqBeatenCareers:list[str], allowedShips:list[str], disallowedShips:list[str]):
        self.app = appInstance
        self.displayName = displayName
        self.icon = icon
        self.levels = levels
        self.requiredLevels = reqBeatenLevels
        self.requiredCareers = reqBeatenCareers
        self.allowedShips = allowedShips
        self.disallowedShips = disallowedShips

    def get_levels(self):
        return self.levels

    def get_required_levels(self):
        return self.requiredLevels

    def get_required_careers(self):
        return self.requiredCareers

    def get_allowed_ships(self):
        return self.allowedShips

    def get_disallowed_ships(self):
        return self.disallowedShips

    def get_icon(self):
        return self.icon