class SpawnableAction:
    def __init__(self, command:str, parameters:list):
        self.command = command
        self.parameters = self._parse_parameters(parameters)

    def _parse_parameters(self, parameters):
        match self.command:
            case "spawn":
                return [str(parameters[0]), parameters[1]] # name and pos for spawnable
            case "explode":
                pass
            case "heal":
                return [parameters[0]]
            case "damage":
                return [parameters[0]]
            case "param": # still related to ship param and not spawnable param
                return [parameters[0], parameters[1]] # name and value of set property