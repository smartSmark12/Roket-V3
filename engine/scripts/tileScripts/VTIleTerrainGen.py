import random
""" from numba import jit """
from scripts.tileScripts.baseBiomeWeights import baseBiomeWeights
from scripts.tileScripts.biome import Biome

class VTileTerrainGenerator:

    @staticmethod
    def generateTerrainMap(mapSize:tuple|list, mapBiomes:list[Biome]|None, biomeSize:int, cleanupStability:int):
        size = mapSize
        biomes = mapBiomes

        if mapBiomes == None:
            biomes = VTileTerrainGenerator.loadBaseBiomes()

        eMap = VTileTerrainGenerator.createEmptyMap(size)

        eMap = VTileTerrainGenerator.placeStartingPoint(eMap, biomes[0]) # [biome.index for biome in biomes]

        eMap = VTileTerrainGenerator.buildMap(eMap, biomes, baseBiomeWeights, biomeSize)

        if cleanupStability > 0:
            eMap = VTileTerrainGenerator.runCleanup(eMap, cleanupStability, biomes, baseBiomeWeights, biomeSize)

        return eMap
    
    @staticmethod
    def loadBaseBiomes():
        baseBiomes = []
        baseBiomeNames = ["grass", "forest", "mountains", "desert", "ocean"]
        for i in range(len(baseBiomeWeights)):
            baseBiomes.append(Biome(baseBiomeNames[i], i))

        return baseBiomes

    @staticmethod
    def createEmptyMap(size:tuple|list):
        eMap = []
        for y in range(size[1]):
            eMap.append([])
            for x in range(size[0]):
                eMap[y].append(-1)

        return eMap

    @staticmethod
    def placeStartingPoint(mapToUse, startingBiome:Biome):
        
        mapToUse[len(mapToUse)//2][len(mapToUse[0])//2] = startingBiome.index

        return mapToUse
    
    @staticmethod
    def buildMap(mapToUse, biomesToUse:list[Biome], biomeWeights:list[int], biomeSize:int|float):

        foundEmptySlot = True

        while foundEmptySlot:

            mapToUse, foundEmptySlot, useless = VTileTerrainGenerator.propagateNextStep(mapToUse, biomesToUse, biomeWeights, biomeSize)

        return mapToUse
    
    @staticmethod
    def propagateNextStep(mapToUse, biomesToUse:list[Biome], biomeWeights:list[int], biomeSize:int|float):

        overlayMap = []

        emptySlotLock = False

        for y in range(len(mapToUse)):
                for x in range(len(mapToUse[y])):

                    if mapToUse[y][x] != -1:

                        nearBias = VTileTerrainGenerator.getBiomeBias(mapToUse, (y, x))

                        if x > 0 and mapToUse[y][x-1] == -1 and round(random.random()) == 0:
                            overlayMap.append((y, x-1, VTileTerrainGenerator.selectBiome(mapToUse[y][x], biomesToUse, biomeWeights, nearBias, biomeSize)))
                        if x < len(mapToUse[y]) - 1 and mapToUse[y][x+1] == -1 and round(random.random()) == 0:
                            overlayMap.append((y, x+1, VTileTerrainGenerator.selectBiome(mapToUse[y][x], biomesToUse, biomeWeights, nearBias, biomeSize)))
                        if y > 0 and mapToUse[y-1][x] == -1 and round(random.random()) == 0:
                            overlayMap.append((y-1, x, VTileTerrainGenerator.selectBiome(mapToUse[y][x], biomesToUse, biomeWeights, nearBias, biomeSize)))
                        if y < len(mapToUse) - 1 and mapToUse[y+1][x] == -1 and round(random.random()) == 0:
                            overlayMap.append((y+1, x, VTileTerrainGenerator.selectBiome(mapToUse[y][x], biomesToUse, biomeWeights, nearBias, biomeSize)))

                        if not emptySlotLock:
                            foundEmptySlot = False
                    
                    else:
                        foundEmptySlot = True
                        emptySlotLock = True

        for rewrite in overlayMap:
            mapToUse[rewrite[0]][rewrite[1]] = rewrite[2]

        return mapToUse, foundEmptySlot, overlayMap
    
    @staticmethod
    def selectBiome(mapValue:int, biomesToUse:list[Biome], biomeWeights:list[int], nearBias:int, biomeSize:int|float):
        biomeSelector = round(random.random() * 1000)
        if biomeSelector * ((nearBias + 1) / biomeSize) < biomeWeights[biomesToUse[mapValue].index][biomesToUse[mapValue].index]:
            return biomesToUse[mapValue].index
        else:
            selectedBiomeIndex = 0
            for i in range(len(biomeWeights[mapValue])):
                if i != biomesToUse[mapValue].index:
                    if biomeSelector/2 < biomeWeights[mapValue][i]:
                        selectedBiomeIndex = i
            
            return biomesToUse[selectedBiomeIndex].index
        
    @staticmethod
    def getBiomeBias(mapToUse, center):
        biases = []
        finalBias = 0

        try: biases.append(mapToUse[center[0]-1][center[1]-1])
        except: pass
        try: biases.append(mapToUse[center[0]][center[1]-1])
        except: pass
        try: biases.append(mapToUse[center[0]+1][center[1]-1])
        except: pass
        try: biases.append(mapToUse[center[0]-1][center[1]])
        except: pass
        try: biases.append(mapToUse[center[0]+1][center[1]])
        except: pass
        try: biases.append(mapToUse[center[0]-1][center[1]+1])
        except: pass
        try: biases.append(mapToUse[center[0]][center[1]+1])
        except: pass
        try: biases.append(mapToUse[center[0]-1][center[1]+1])
        except: pass

        for i in biases:
            if i == mapToUse[center[0]][center[1]]:
                finalBias += 1

        return finalBias
    
    @staticmethod
    def runCleanup(mapToUse, stability:int, biomesToUse:list[Biome], biomeWeights:list[int], biomeSize:int|float):
        cleanupRequired = True
        timesRan = 0
        tilesRemoved = 0

        while cleanupRequired:
            try:
                mapToUse = VTileTerrainGenerator.buildMap(mapToUse, biomesToUse, biomeWeights, biomeSize)
            except: pass
            mapToUse, cleanupRequired, tilesRemovedDelta = VTileTerrainGenerator.cleanupBiomes(mapToUse, stability)
            tilesRemoved += tilesRemovedDelta
            timesRan += 1

        print("cleanup ran ", timesRan, " times on stability of ", stability, " (replaced tiles: ", tilesRemoved, "/", len(mapToUse)*len(mapToUse[0]), ";", round(len(mapToUse)/len(mapToUse[0])*1000)/1000, "%", ")")

        return mapToUse
    
    @staticmethod
    def cleanupBiomes(mapToUse, stability:int):
        tilesRemoved = 0
        for y in range(len(mapToUse)):
            for x in range(len(mapToUse[y])):
                sameBiomeTypeFound = 0
                try:
                    if mapToUse[y-1][x-1] == mapToUse[y][x]: sameBiomeTypeFound += 1
                except: pass
                try:
                    if mapToUse[y-1][x] == mapToUse[y][x]: sameBiomeTypeFound += 1
                except: pass
                try:
                    if mapToUse[y-1][x+1] == mapToUse[y][x]: sameBiomeTypeFound += 1
                except: pass
                try:
                    if mapToUse[y][x-1] == mapToUse[y][x]: sameBiomeTypeFound += 1
                except: pass
                try:
                    if mapToUse[y][x+1] == mapToUse[y][x]: sameBiomeTypeFound += 1
                except: pass
                try:
                    if mapToUse[y+1][x-1] == mapToUse[y][x]: sameBiomeTypeFound += 1
                except: pass
                try:
                    if mapToUse[y+1][x] == mapToUse[y][x]: sameBiomeTypeFound += 1
                except: pass
                try:
                    if mapToUse[y+1][x+1] == mapToUse[y][x]: sameBiomeTypeFound += 1
                except: pass

                if sameBiomeTypeFound <= stability: mapToUse[y][x] = -1; tilesRemoved += 1

        if tilesRemoved > 0:
            return mapToUse, True, tilesRemoved
        else:
            return mapToUse, False, tilesRemoved