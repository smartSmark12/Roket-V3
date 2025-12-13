NGF_VERSION = "0.0.4s"
GAME_NAME = "Roket V3!"
GAME_VERSION = "0.1"
GAME_VERSION_HINT = "Hydrogen"

WIDTH = 1920
HEIGHT = 1080

RESOLUTION = (WIDTH, HEIGHT)
IN_FULLSCREEN = False

# rendering options
FPS_LOGIC_LIMIT:int = 400#120           # limits UPS ## TBA
FPS_RENDER_LIMIT:int = 0            # limits rendered FPS
SYNC_UPS_FPS:bool = 1               # should client synchronize UPS and FPS? (leads to better UPS-FPS ratio) - EXPERIMENTAL!!
RENDER_LAYERS:int = 10              # set how many layers your game uses; start from 0, empty layers usually don't impact performance much
MULTITHREADED_RENDERING:bool = True # use a newer multithreaded rendering method - EXPERIMENTAL

OGL_ENABLED:bool = 0                # opengl implementation for shader support (currently resource heavy)
DEFAULT_SHADER_PATH:str = "./engine/shaders/default" # adds '.vert' & '.frag' automatically

DEFAULT_SPRITE_PATH:str = "./engine/scripts/sprites_to_load.py"
DEFAULT_SPRITE_JSON_PATH:str = "./engine/scripts/json/sprites_to_load.json"
DEFAULT_ANIMATION_PATH:str = "./engine/scripts/animations_to_create.py"

# scene settings
DEFAULT_SCENE_NAME = "main_menu"         # the default rendered scene

## game settings cause me be lazy :33
DEFAULT_LOCALIZATION_CODE = "en"
LOCALIZATION_PATH = "./engine/game/localization/"
LOCALIZATION_POSTFIX = ".json"

DEFAULT_KEYBIND_PATH = "./engine/game/settings/roket_keybinds_template.json" # used if no other config is present as a copy source
ACTIVE_KEYBIND_PATH = "./engine/game/settings/roket_keybinds.json"

DEFAULT_FONT_PATH = "engine/game/assets/fonts/MinecraftRegular-Bmg3.otf"

BUTTON_FONT_SIZE = 36
H1_FONT_SIZE = 160
VERSION_FONT_SIZE = 20

TITLE_PLANET_SPAWNING_PERIOD = 10
TITLE_PLANET_SPAWNING_ANICHANCE = 20 # its more like 1/antichance is the chance, so

# server settings
SERVER_CONNECTIONS:int = 4          # max connections the server will expect at start
SERVER_DATA_SIZE:int = 1024*16      # max bytesize the client will send and accept
SERVER_UPS:int = 60
SERVER_DELTA:float = (1000/SERVER_UPS)/1000   # minimum time delay between sending packets
SERVER_TIMEOUT:int = 5              # max time of no response from server before kicking player

# server debug settings
SERVER_LOCAL_SERVER:bool = 1         # whether to connect to a local server or to an external one
SERVER_IP:str = None                # external server IP