from game.scripts.roket_body_related.roket_module_type import RoketModuleType
from vuilib.vui_flatpane import flatpane

class RoketModule:
    def __init__(self, name:str, displayName:str, moduleType:str, moduleLevel:int, maxModuleLevel:int, moduleModifiers:dict[str,any], moduleSprites:flatpane):
        self.name = name
        self.displayName = displayName
        self.modType = moduleType
        self.modLevel = moduleLevel # possibly strength of the given modifier (lives added per level, etc.)
        self.modMaxLevel = maxModuleLevel
        self.modModifiers = moduleModifiers # check out the roket_mods.md!
        self.modSprites = moduleSprites

        self.triggers = {
            "on_activation":None,
            "on_collision":None,
            "on_timeout":None
        }

        # format
        # "trigger_name": ["spawn", "registeredSpawnableName"]

    def trigger(self, triggerName:str):
        if triggerName in self.triggers:
            if self.triggers[triggerName] is not None:
                return self.triggers.get(triggerName)
        
        return False