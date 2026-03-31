from vuilib.vui_flatpane import flatpane
from game.scripts.roket_spawnable_related.spawnable_navigator import Navigator
import pygame as pg

class SpawnableObject:
    def __init__(self, appInstance, name:str, displayName:str, collider:pg.Rect, sprites:flatpane, navigator:Navigator, actions:dict, moveSpeed:int|float, targetPosition:tuple=None):
        self.app = appInstance
        self.name = name
        self.displayName = displayName
        self.collider = collider
        self.navigator = navigator
        self.sprites = sprites

        self.actions = actions

        self.navigator.set_object(self)

        self.speed = moveSpeed

        self.pos = None
        self.targetPos = targetPosition

        if self.targetPos is not None:
            self.navigator.set_target_pos(self.targetPos)

        self.pos = self.navigator.get_start_pos()

    def trigger(self, triggerName:str):
        if triggerName in self.actions:
            if self.actions[triggerName] is not None:
                return self.actions.get(triggerName)
        
        return False
    
    def die(self):
        pass