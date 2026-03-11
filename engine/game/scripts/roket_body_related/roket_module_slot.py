from game.scripts.roket_body_related.roket_module import RoketModule

class RoketModuleSlot:
    def __init__(self, slotId:int, name:str, allowedModuleTypes:list[str], module:RoketModule|None=None):
        self.slotId = slotId
        self.name = name # essentially display name
        self.allowedModTypes = allowedModuleTypes
        self.module = None
        
        if module is not None: 
            if module.modType in self.allowedModTypes:
                self.module = module
            else:
                print(f"{__name__}: module {module.name} isn't allowed in module types ({[i for i in self.allowedModTypes]}) of slot {self.name} (id: {self.slotId})")

    def add_module(self, module:RoketModule) -> bool:
        if self.module is not None:
            print(f"{__name__}: module {module.name} cannot be added; slot already used")
            return False
        elif module.modType not in self.allowedModTypes:
            print(f"{__name__}: module {module.name} isn't allowed in module types ({[i for i in self.allowedModTypes]}) of slot {self.name} (id: {self.slotId})")
            return False
        else:
            print(f"Module {module.name} added to slot {self.name} (id: {self.slotId})")
            self.module = module
            return True
        
    def remove_module(self) -> bool|RoketModule:
        if self.module == None:
            print(f"{__name__}: cannot remove module from slot {self.name} (id: {self.slotId}) - no module present")
            return False
        else:
            print(f"Removed module {self.module.name} from slot {self.name} (id: {self.slotId})")
            module = self.module
            self.module = None
            return module # this fuckery is funny
        
    def trigger_module(self, triggerName:str):
        return self.module.trigger(triggerName)