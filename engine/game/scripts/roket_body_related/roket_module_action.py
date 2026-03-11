class RoketModuleAction:
    def __init__(self, command:str, parameters:list):
        self.command = command
        self.parameters = self._parse_parameters(parameters)

    def _parse_parameters(self, parameters):
        match self.command:
            case "damage":
                return [int(parameters[0])]

            case "heal":
                return [int(parameters[0])]

            case "spawn":
                print("implement me pls")
                pass

            case "explode":
                pass