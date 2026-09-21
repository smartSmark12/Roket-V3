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
        """ self.pos = position """
        self.moduleSlots = moduleSlots

        self.properties = {
            "displayName":displayName,
            "position":position,
            "baseLives":baseLives, # essentially max lives
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

        self.superProperties = copy.deepcopy(self.properties) # deepcopy cause reasons

    def get_property(self, propertyName:str):
        if propertyName in self.superProperties:
            return self.superProperties[propertyName]
        else:
            pass # debug here todo

    def trigger_module_action(self, triggerId:int, actionName:str):
        actions:dict = self.get_property("module_actions")
        if triggerId in actions:
            module:RoketModuleSlot = actions.get(triggerId)
            action:RoketModuleAction = module.trigger_module(actionName) # returns RoketModuleAction if it exists, else False
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
        # reset current stats to the ship default
        #
        # go through every slot
        # add its module's stats to the super properties if it has a module
        #
        # needs to be expanded to support modded modifiers in the future :cries:
        # i sorta have to hardcode it rn to save time
        # also, hello not!kerry :3

        self.superProperties = copy.deepcopy(self.properties)

        for moduleSlotKey, moduleSlot in self.moduleSlots.items():
            if moduleSlot.has_module():
                module = moduleSlot.get_module()

                for modifierName, modifier in module.get_modifiers().items():
                    # hardcoded section begins
                    match modifierName:
                        case "move_speed_mod":
                            self.superProperties["move_speed"] += modifier
                        case "boost_upgrade":
                            pass
                        case "laser_upgrade":
                            pass
                        case "hull_strength_mod":
                            self.superProperties["baseLives"] += modifier # need to increment both max lives and actual lives
                            self.superProperties["lives"] += modifier
                        case "shield_upgrade":
                            pass
                        case "ghost_upgrade":
                            pass
                        case "heal_drone_upgrade":
                            pass
                        case _:
                            pass


    def move(self, targetPos:tuple):
        pass

    def get_pos(self):
        return self.get_property("position")

    def update_anim(self, dt:float):
        pass

    def add_module(self, slotId:int, module:RoketModule):
        pass

    def remove_module(self, slotId:int, moduleName:str):
        pass

    def get_module(self, moduleID:int):
        if moduleID in self.moduleSlots.keys():
            return self.moduleSlots.get(moduleID)
        
    def get_module_slots(self):
        return self.moduleSlots

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
