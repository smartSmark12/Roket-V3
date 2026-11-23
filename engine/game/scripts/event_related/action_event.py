class ActionEvent:
    def __init__(self, appInstance, actionCondition:float, actionType:int, actionParams:dict):
        self.app = appInstance
        self.condition = actionCondition
        self.atype = actionType
        self.params = actionParams

    def get_params(self):
        return self.params

    def get_param(self, paramName:str):
        if paramName in self.params.keys():
            return self.params.get(paramName)

        else:
            print(f"{__name__}: parameter {paramName} not found")

    def get_condition(self):
        return self.condition