import pygame
from engine.scripts.mplib.multiplayerNetwork import Network
""" from player import Player """

class mpClient:
    def __init__(self):
        self.network = self.getNetwork()
        self.id = self.getPlayerID()
        
    def getGameState(self, dataToSend): # return current game state whilst sending current player data to the server ## needs to run at fixed clock mby??
        return self.network.sendAndReceive(dataToSend) ## separate sending and receiving?! ## Nah, just limit the speed by sending/receiving after some limit (>0.016.7 dt - 60fps)

    def getPlayerID(self):
        return self.network.networkGetPlayerID()

    def getNetwork(self):
        return Network()
        

    """ def main():
        run = True
        n = Network()
        p = n.getP()
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            p2 = n.send(p)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            p.move()

    main() """