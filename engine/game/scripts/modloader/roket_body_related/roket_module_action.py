class RoketModuleAction:
    def __init__(self, command:str, parameters:list):
        self.command = command
        self.parameters = self._parse_parameters(parameters)

    def _parse_parameters(self, parameters):
        match self.command:
            case "damage":
                return [int(parameters[0])] # just the amount of damage done

            case "heal":
                return [int(parameters[0])] # just the amount of ship healing done

            case "spawn":
                name = parameters[0] # name of the spawnable (has to be registered)
                position = parameters[1] # pos used for point, s_point etc. movement, where the starting position differs from ship position
                
                return [name, position]

            case "explode":
                pass