from game.scripts.event_related.action_event import ActionEvent

class EnvActionEvent(ActionEvent):
    def __init__(self, appInstance, actionCondition:float, actionPeriod:float, actionType:int, actionParams:dict):
        super().__init__(appInstance, actionCondition, actionType, actionParams)

        self.actionPeriod = actionPeriod

    def get_period(self):
        return self.actionPeriod