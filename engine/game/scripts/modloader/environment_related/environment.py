from game.scripts.event_related.environment_action_event import EnvActionEvent

class Environment:
    def __init__(self, appInstance, backgroundColor:tuple|list, randomObjectEvents:dict[str,EnvActionEvent], forcedObjectEvents:dict[str,EnvActionEvent]): # contains background color and background objects
        self.app = appInstance
        self.backgroundColor = backgroundColor

        self.randomObjectEvents = randomObjectEvents
        self.forcedObjectEvents = forcedObjectEvents