""" from scripts.tileScripts.baseBiomeWeights import baseBiomeWeights """

class Biome:
    def __init__(self, biomeName:str, generatorIndex:int):
        self.name = biomeName
        self.index = generatorIndex