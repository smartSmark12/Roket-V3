class Environment:
    def __init__(self, appInstance, backgroundColor:tuple|list, objectEvents:dict[dict[list]]): # contains background color and background objects
        self.app = appInstance
        self.backgroundColor = backgroundColor
        self.objectEvents = objectEvents