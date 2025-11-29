import random

class VTileGenerator:

    @staticmethod
    def generateMap(mapSize:tuple|list, mapContent:list, generatorType:str, seedCount:int):
        size = mapSize
        content = mapContent
        gtype = generatorType
        seedCount = seedCount # pointless?

        match gtype:
            case "vk":
                eMap = VTileGenerator.createEmptyMap(size)

                eMap = VTileGenerator.placeStartingPoints(eMap, content, seedCount)

                eMap = VTileGenerator.propagateStartingPoints(eMap)

            case "square":
                eMap = VTileGenerator.createEmptyMap(size)

                eMap = VTileGenerator.placeStartingPoints(eMap, content, seedCount)

                eMap = VTileGenerator.propagateStartingPointsFullchance(eMap)


        return eMap
        
        """ VTileGenerator.printMap(eMap) """

    @staticmethod
    def createEmptyMap(size:tuple|list):
        eMap = []
        for y in range(size[1]):
            eMap.append([])
            for x in range(size[0]):
                eMap[y].append(-1)

        return eMap

    @staticmethod
    def placeStartingPoints(mapToUse, content:list, count:int):
        pointsPlaced = 0

        while pointsPlaced < count - 1:
            position = (random.randint(0, len(mapToUse) - 1), random.randint(0, len(mapToUse[0]) - 1))

            if mapToUse[position[0]][position[1]] == -1:

                seedRotationCounter = pointsPlaced
                while seedRotationCounter > len(content) - 1:
                    seedRotationCounter -= len(content)

                mapToUse[position[0]][position[1]] = content[seedRotationCounter]
                pointsPlaced += 1

        return mapToUse
    
    @staticmethod
    def propagateStartingPoints(mapToUse):

        foundEmptySlot = True

        while foundEmptySlot:

            mapToUse, foundEmptySlot = VTileGenerator.propagateNextStep(mapToUse)

            """ for y in mapToUse:
                if -1 in y:
                    foundEmptySlot = True
                    break
                else:
                    foundEmptySlot = False """

        return mapToUse
    
    @staticmethod
    def propagateNextStep(mapToUse):

        overlayMap = []

        emptySlotLock = False

        for y in range(len(mapToUse)):
                for x in range(len(mapToUse[y])):

                    if mapToUse[y][x] != -1:

                        if x > 0 and mapToUse[y][x-1] == -1 and round(random.random()) == 0:
                            overlayMap.append((y, x-1, mapToUse[y][x]))

                        if x < len(mapToUse[y]) - 1 and mapToUse[y][x+1] == -1 and round(random.random()) == 0:
                            overlayMap.append((y, x+1, mapToUse[y][x]))

                        if y > 0 and mapToUse[y-1][x] == -1 and round(random.random()) == 0:
                            overlayMap.append((y-1, x, mapToUse[y][x]))

                        if y < len(mapToUse) - 1 and mapToUse[y+1][x] == -1 and round(random.random()) == 0:
                            overlayMap.append((y+1, x, mapToUse[y][x]))


                        if not emptySlotLock:
                            foundEmptySlot = False
                    
                    else:
                        foundEmptySlot = True
                        emptySlotLock = True

        for rewrite in overlayMap:
            mapToUse[rewrite[0]][rewrite[1]] = rewrite[2]

        return mapToUse, foundEmptySlot

    @staticmethod
    def propagateStartingPointsFullchance(mapToUse):

        foundEmptySlot = True

        while foundEmptySlot:

            mapToUse, foundEmptySlot = VTileGenerator.propagateNextStepFullchance(mapToUse)

        return mapToUse

    @staticmethod
    def propagateNextStepFullchance(mapToUse):
        overlayMap = []

        emptySlotLock = False

        for y in range(len(mapToUse)):
                for x in range(len(mapToUse[y])):

                    if mapToUse[y][x] != -1:

                        if x > 0 and mapToUse[y][x-1] == -1:
                            overlayMap.append((y, x-1, mapToUse[y][x]))

                        if x < len(mapToUse[y]) - 1 and mapToUse[y][x+1] == -1:
                            overlayMap.append((y, x+1, mapToUse[y][x]))

                        if y > 0 and mapToUse[y-1][x] == -1:
                            overlayMap.append((y-1, x, mapToUse[y][x]))

                        if y < len(mapToUse) - 1 and mapToUse[y+1][x] == -1:
                            overlayMap.append((y+1, x, mapToUse[y][x]))


                        if not emptySlotLock:
                            foundEmptySlot = False
                    
                    else:
                        foundEmptySlot = True
                        emptySlotLock = True

        for rewrite in overlayMap:
            mapToUse[rewrite[0]][rewrite[1]] = rewrite[2]

        return mapToUse, foundEmptySlot


    @staticmethod
    def printMap(mapToUse):
        for i in mapToUse:
            print(i)