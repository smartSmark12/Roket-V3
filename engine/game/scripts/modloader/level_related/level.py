class Level:
    def __init__(self, appInstance, displayName:str, icon, stages:dict[str, any], requirements:dict, allowedShips:list[str], disallowedShips:list[str]):
        self.app = appInstance
        self.displayName = displayName
        self.icon = icon
        self.stages = stages
        self.requirements = requirements
        self.allowedShips = allowedShips
        self.disallowedShips = disallowedShips