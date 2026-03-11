""" from game.scripts.roket_module_type import RoketModuleType """
from game.scripts.roket_body_related.roket_module import RoketModule
from game.scripts.roket_body_related.roket_module_slot import RoketModuleSlot
from game.scripts.roket_body_related.roket_module_action import RoketModuleAction
from vuilib.vui_flatpane import flatpane

import copy
import pygame as pg

class RoketBody:
    def __init__(self, name:str, displayName:str, baseLives:int, baseSprites:flatpane, position:tuple[int|float], size:tuple[int], collisionRect:pg.Rect, moduleSlots:dict[int, RoketModuleSlot], lives=None):
        self.name = name
        self.sprites = baseSprites
        self.pos = position
        self.moduleSlots = moduleSlots

        self.properties = {
            "displayName":displayName,
            "baseLives":baseLives,
            "move_speed":1,
            "size":size,
            "collider":collisionRect,
            "size_scale":1,
            "lives":baseLives if lives == None else lives, # xd
            "module_actions":None, # dict gets created dynamically
        }

        # format
        # "module_actions":{
        # actionId-int: slot-RoketModuleSlot
        # }

        self.superProperties = copy.deepcopy(self.properties)

    def get_property(self, propertyName:str):
        if propertyName in self.superProperties:
            return self.superProperties[propertyName]
        else:
            pass # debug here todo

    def trigger_module_action(self, triggerId:int, actionName:str):
        actions = self.get_property("module_actions")
        if triggerId in actions:
            action = actions.get(triggerId).trigger_module(actionName) # returns RoketModuleAction if it exists, else False
            if action:
                self.do_action(action)

    def do_action(self, action:RoketModuleAction):
        match action.command: # have to change in RoketModuleAction._parse_parameters also!!!
            case "damage":
                pass

            case "heal":
                pass
            case "spawn":
                pass
            case "explode":
                pass

    def update_module_stats(self):
        pass

    def move(self, targetPos:tuple):
        pass

    def update_anim(self, dt:float):
        pass

    def add_module(self, slotId:int, module:RoketModule):
        pass

    def remove_module(self, slotId:int, moduleName:str):
        pass

    def clear_modules(self):
        pass

    def use_ability(self):
        pass # multiple abilities?

    def use_weapon(self):
        pass

    def hit(self, amount:int=1):
        pass

    def heal(self, amount:int=1):
        pass

    def die(self):
        pass

    def reset(self):
        pass
