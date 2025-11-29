import socket
from _thread import *
import pickle

from scripts.core.settings import SERVER_DATA_SIZE

class mpServer:
    def __init__(self, numberOfConnections: int):
        hostname = socket.gethostname()
        self.serverAddress = socket.gethostbyname(hostname)#"10.11.250.207"
        self.serverPort = 5555
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.currentPlayerID = 0

        self.bindToAddress()
        self.reserveConnections(numberOfConnections)

        self.startMainThread()
        self.waitForConnections()

    def bindToAddress(self):
        try:
            self.serverSocket.bind((self.serverAddress, self.serverPort))
        except socket.error as e:
            str(e)
            print("Server can't be bound to this address/port")

    def reserveConnections(self, connections):
        self.serverSocket.listen(connections)
        print(f"Server started at address {self.serverAddress}:{self.serverPort}; waiting for connections (max: {connections})")

    def waitForConnections(self):
        while True:
            connection, address = self.serverSocket.accept()
            print(f"Client connected: {address}")

            start_new_thread(self.networkThread, (connection, self.currentPlayerID))
            self.currentPlayerID += 1

    def startMainThread(self):
        start_new_thread(self.mainThread, (1))

    def networkThread(connection, playerID):
        connection.send(pickle.dumps(playerID))
        reply = ""

        while True:
            try:
                receivedData = pickle.loads(connection.recv(SERVER_DATA_SIZE)) # change datablock size? (universal variables for sending, receiving etc.)
                # handle data - see below

                if not receivedData:
                    print(f"Client disconnected ({playerID})")
                    break

                else:
                    pass # handle sending of right server data for clients here by 'reply = {data}'

                connection.sendall(pickle.dumps(reply))

            except: break # failsafe when connection is lost

        # handle lost connection here
        print(f"Lost connection ({playerID})")
        connection.close()

    # server thread section - can change/edit
    def mainThread(self, status):
        pass