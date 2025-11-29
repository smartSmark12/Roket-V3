import socket
import pickle

from scripts.core.settings import SERVER_DATA_SIZE

class Network:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.11.250.207"
        self.port = 5555
        self.serverAddress = (self.server, self.port)
        self.playerID = self.connectToServer()

    def networkGetPlayerID(self):
        return self.playerID

    def connectToServer(self):
        try:
            self.clientSocket.connect(self.serverAddress)
            return pickle.loads(self.clientSocket.recv(SERVER_DATA_SIZE)) # returns first connection data - player ID
        except:
            pass

    def sendAndReceive(self, data):
        try:
            self.clientSocket.send(pickle.dumps(data))
            return pickle.loads(self.clientSocket.recv(SERVER_DATA_SIZE))
        except socket.error as e:
            print(e)