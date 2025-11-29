from engine.scripts.mplib.multiplayerServer import mpServer
from engine.scripts.core.settings import *

def main():
    server = mpServer(SERVER_CONNECTIONS)

if __name__ == "__main__":
    main()