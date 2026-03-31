from game.scripts.roket_body_related.roket_body import RoketBody
from game.scripts.roket_spawnable_related.spawnable_object import SpawnableObject
from game.scripts.obstacle_related.obstacle import Obstacle
from game.scripts.level_related.level import Level
from game.scripts.environment_related.environment import Environment

class GameState:
    def __init__(self):
        self.roket_body:RoketBody

        self.obstacles:list[Obstacle] = None # asteroids, etc
        self.spawnables:dict[int, SpawnableObject] = None # id and spawnable (body or enemy)

        self.static_levels:list[Level] = None # contains consequent levels with all their environments, obstacle rules, spawnable rules, etc
        self.environment:Environment = None # contains background, planets, stars, etc

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
    
    # ADDERS!!!

    def add_obstacle(self, obstacleToAdd:Obstacle) -> None:
        self.obstacles.append(obstacleToAdd)

    def add_spawnable(self, spawnableToAdd:SpawnableObject) -> int:
        self.spawnables[id(spawnableToAdd), spawnableToAdd]

    # SETTERS ???
    def set_something_on_fire(self):
        print("aaah it burns")