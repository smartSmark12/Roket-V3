## THIS EXECUTABLE IS TO BE RUN TO PLAY THE GAME/PROGRAM
## DO NOT USE mainEngine.py AS AN ENTRY POINT

import sys
sys.path.append('./engine')
from engine.scripts.core.mainEngine import runGame

def main():
    runGame()

if __name__ == "__main__":
    main()