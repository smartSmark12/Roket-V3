from time import time

from engine.game.scripts.modloader.roket_body_related.roket_body import RoketBody
from engine.game.scripts.modloader.roket_spawnable_related.spawnable_object import SpawnableObject
from engine.game.scripts.modloader.obstacle_related.obstacle import Obstacle
from engine.game.scripts.modloader.level_related.level import Level
from engine.game.scripts.modloader.environment_related.environment import Environment

class GameState:
    def __init__(self, app, body:RoketBody, level:Level):
        self.roket_body:RoketBody = body

        self.obstacles:list[Obstacle] = None # asteroids, etc
        self.spawnables:dict[int, SpawnableObject] = None # id and spawnable (body or enemy)

        self.static_levels:list[Level] = None # contains consequent levels with all their environments, obstacle rules, spawnable rules, etc
        self.environment:Environment = None # contains background, planets, stars, etc

        self._start_time = 0
        self._last_game_time = 0
        self._game_time = 0

        self._time_paused = False
        self.unpause_time()

        # environment
        self.environment_objects = []

    def _get_time_paused(self):
        return self._time_paused

    def _update_game_time(self):
        self._game_time = time() - self._start_time + self._last_game_time

    def pause_time(self):
        self._time_paused = True

        self._last_game_time = self._game_time + self._last_game_time
        self._game_time = self._last_game_time

    def unpause_time(self):
        self._time_paused = False

        self._start_time = time()

    def _update_env_objects(self):
        for env_object_index in self.environment_objects:
            env_object:SpawnableObject = self.environment_objects[env_object_index]

            env_object.move()

    def update(self):
        self._update_game_time()
        self._update_env_objects()


    # GETTERS

    def get_roket_body(self):
        return self.roket_body
    
    def get_obstacles(self):
        return self.obstacles
    
    def get_spawnables(self):
        return self.spawnables
    
    def get_static_levels(self):
        return self.static_levels
    
    def get_environment(self):
        return self.environment

    def get_game_time(self):
        return self._game_time
    
    # ADDERS!!!

    def spawn_env_object(self, objectToAdd:SpawnableObject):
        self.environment_objects.append(objectToAdd)

    def add_obstacle(self, obstacleToAdd:Obstacle) -> None:
        self.obstacles.append(obstacleToAdd)

    def add_spawnable(self, spawnableToAdd:SpawnableObject) -> int:
        self.spawnables[id(spawnableToAdd), spawnableToAdd]

        return id(spawnableToAdd)

    # SETTERS ???
    def set_something_on_fire(self):
        print("aaah it burns")