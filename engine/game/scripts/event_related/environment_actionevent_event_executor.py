from game.scripts.event_related.event_executor import EventExecutor
from game.scripts.event_related.action_event import ActionEvent
from game.scripts.modloader.roket_spawnable_related.spawnable_prefab import SpawnablePrefab
from game.scripts.modloader.roket_spawnable_related.spawnable_object import SpawnableObject

class EnvironmentActioneventExecutor(EventExecutor):
    def __init__(self, appInstance, actionList):
        super().__init__(appInstance, actionList)

        self.loaded_prefabs = {}

    def add_prefab(self, objectPrefab:SpawnablePrefab) -> None:
        if not objectPrefab.spawnableName in self.loaded_prefabs.keys():
            self.loaded_prefabs[objectPrefab.spawnableName] = objectPrefab

        else:
            print(f"{__name__}: spawnable prefab '{objectPrefab.spawnableName}' has already been added to this level's env event executor")

    def get_prefab(self, prefabName:str) -> SpawnablePrefab | None:
        if prefabName in self.loaded_prefabs.keys():
            return self.loaded_prefabs.get(prefabName)

        else:
            print(f"{__name__}: couldn't find spawnable prefab '{prefabName}'")


    def _execute_event(self, event:ActionEvent):
        match event.atype:
            case self.action_type.ACTION_ENV_SPAWN:
                try:
                    spawnable_name = event.get_param("name")
                    spawnable_pos = event.get_param("position")

                    prefab = self.get_prefab(spawnable_name)

                    spawnable = prefab.create_spawnable(spawnable_pos)

                    self.app.get_gamestate().spawn_env_object(
                        spawnable
                    )

                except Exception as e:
                    print(f"{__name__}: couldn't spawn environment object. Error: {e}")
