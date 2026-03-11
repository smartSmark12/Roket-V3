from vuilib.vui_flatpane import flatpane
from game.scripts.spawnable_navigator import Navigator
import pygame as pg

class SpawnableObject:
    def __init__(self, name:str, displayName:str, collider:pg.Rect, sprites:flatpane, navigator:Navigator, actions:dict):
        self.name = name
        self.displayName = displayName
        self.collider = collider
        self.navigator = navigator
        self.sprites = sprites

        self.actions = actions

    def trigger(self, triggerName:str):
        if triggerName in self.actions:
            if self.actions[triggerName] is not None:
                return self.actions.get(triggerName)
        
        return False