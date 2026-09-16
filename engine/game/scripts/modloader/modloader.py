# Roket V3 modloader
# WIP

from scripts.json_loader import JsonLoader

from game.scripts.modloader.roket_body_related.roket_body               import RoketBody
from game.scripts.modloader.roket_body_related.roket_module_type        import RoketModuleType
from game.scripts.modloader.roket_body_related.roket_module             import RoketModule
from game.scripts.modloader.roket_spawnable_related.spawnable_prefab    import SpawnablePrefab
from game.scripts.modloader.career_related.career                       import Career
from game.scripts.modloader.level_related.level                         import Level
from game.scripts.modloader.environment_related.environment             import Environment
from game.scripts.modloader.localization_related.localizationResource   import LocalizationResource

class ModLoader:
    def __init__(self, appInstance):
        self.app = appInstance

        # feature memory
        self.mod_bodies         :dict[RoketBody]            = {}
        self.mod_module_types   :list[RoketModuleType]      = [] # !list
        self.mod_modules        :dict[RoketModule]          = {}
        self.mod_spawnables     :dict[SpawnablePrefab]      = {}
        self.mod_careers        :dict[Career]               = {}
        self.mod_levels         :dict[Level]                = {}
        self.mod_environments   :dict[Environment]          = {}
        self.mod_localizations  :list[LocalizationResource] = [] # !list

    def reload_mods(self):
        pass
    
        self._validate_loaded_mods()

    def use_localization(self, localizationCode:str="en"):
        pass

    # LOADING SHIS
    def load_mod(self, modPath:str):
        
        # loading
        modInfo = JsonLoader.load_from_file(modPath + "mod_info.json")

        # debug
        print("--------\nLoading mod file:\n")
        print(f"{modInfo['mod_name']} ({modInfo['mod_id']}) by {modInfo['mod_author']} (v:{modInfo['mod_version']})")

        # feature loading
        features = modInfo['mod_features']
        
        for feature in features:
            if type(features[feature]) == str:
                featurePath = modPath + features[feature]
            elif type(features[feature]) == list:
                featurePath = [modPath + i for i in features[feature]]

            match feature:
                
                case "ships":
                    self._load_bodies(featurePath)
                
                case "module_types":
                    self._load_module_types(featurePath)
                    
                case "modules":
                    self._load_roket_modules(featurePath)
                    
                case "spawnables":
                    self._load_spawnables(featurePath)
                    
                case "environment_objects":
                    pass
                
                case "environments":
                    self._load_environments(featurePath)
                    
                case "levels": 
                    self._load_levels(featurePath)
                    
                case "careers": 
                    pass
                
                case "localization":
                    self._load_localization_resource(featurePath)
                    
                    
        # debug too
        self.show_info_popup(f"loaded mod: {modInfo['mod_name']} ({modInfo['mod_id']}) by {modInfo['mod_author']} (v:{modInfo['mod_version']})")
                    

        # SANITY mod check here; until then, load everything upon a promise
        # only now will the mod references (level->environments->environment_objects) be checked
        # cause else it just does fucking whatever it wants and its not good

    def _load_bodies(self, source:str):
        pass
    
    def _load_module_types(self, source:str):
        pass

    # VALIDATION

    def _validate_loaded_mods(self):
        pass