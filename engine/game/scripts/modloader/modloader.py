# Roket V3 modloader
# WIP

import pygame as pg

from scripts.json_loader                                                import JsonLoader
from scripts.core.settings                                              import *
from game.scripts.modloader.modloader_definitions                       import ModDefinitions as md
from vuilib.vui_flatpane                                                import flatpane # this whole flatpane vuilib system is fucking stupid; should redo it with NRS
from vuilib.vui_flatpane_autoconvert                                    import convert_to_flatpane

from game.scripts.modloader.roket_body_related.roket_body               import RoketBody
from game.scripts.modloader.roket_body_related.roket_module_type        import RoketModuleType
from game.scripts.modloader.roket_body_related.roket_module             import RoketModule
from game.scripts.modloader.roket_body_related.roket_module_slot        import RoketModuleSlot
from game.scripts.modloader.roket_spawnable_related.spawnable_prefab    import SpawnablePrefab
from game.scripts.modloader.roket_spawnable_related.spawnable_navigator import Navigator
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
                featurePath = [modPath + features[feature]]
            elif type(features[feature]) == list:
                featurePath = [modPath + i for i in features[feature]]

            match feature:
                
                case md.MOD_FEATURE_SHIP:
                    self._load_bodies(featurePath)
                
                case md.MOD_FEATURE_MODULE_TYPE:
                    self._load_module_types(featurePath)
                    
                case md.MOD_FEATURE_MODULE:
                    self._load_modules(featurePath)
                    
                case md.MOD_FEATURE_SPAWNABLE:
                    self._load_spawnables(featurePath)
                    
                case md.MOD_FEATURE_ENV_OBJECT:
                    pass
                
                case md.MOD_FEATURE_ENV:
                    self._load_environments(featurePath)
                    
                case md.MOD_FEATURE_LEVEL: 
                    self._load_levels(featurePath)
                    
                case md.MOD_FEATURE_CAREER:
                    self._load_careers(featurePath)
                
                case md.MOD_FEATURE_LOCALIZATION:
                    self._load_localization_resource(featurePath)
                    
                    
        # debug too
        self.app.show_info_popup(f"loaded mod: {modInfo['mod_name']} ({modInfo['mod_id']}) by {modInfo['mod_author']} (v:{modInfo['mod_version']})")
                    

        # SANITY mod check here; until then, load everything upon a promise
        # only now will the mod references (level->environments->environment_objects) be checked
        # cause else it just does fucking whatever it wants and its not good

    def _load_bodies(self, source:list):

        for single_source in source:
            data = JsonLoader.load_from_file(single_source)
            for body_name in data[md.MOD_FEATURE_SHIP]:
                body = data[md.MOD_FEATURE_SHIP][body_name]

                # prepare sprites
                loaded_sprite_paths = body["animation_sprites"]

                # prepare prefix
                sprite_path_prefix = None

                if body["sprite_source"] == "internal":
                    sprite_path_prefix = INTERNAL_SPRITE_PATH
                elif body["sprite_source"] == "external":
                    sprite_path_prefix = EXTERNAL_SPRITE_PATH
                else:
                    sprite_path_prefix = "" # when using fully custom paths

                # output sprite dict
                sprite_dict = {}

                # load sprites
                for sprite_index in range(len(loaded_sprite_paths)):
                    sprite_path = sprite_path_prefix + loaded_sprite_paths[sprite_index]

                    # generate sprite name
                    sprite_name = f"{body_name}_anim_{sprite_index}"

                    sprite_dict[sprite_index] = self.app.sprite_handler.load_sprite(sprite_name, sprite_path, body["size"], "ca")


                # create final flatpane
                body_sprite = flatpane("sprite", sprite_dict, sprite=0)

                # load module slots
                loaded_slots = body["module_slots"]

                # prepare module slots
                module_slots = {}

                # create modules
                for slot_id_str in loaded_slots:
                    loaded_slot = loaded_slots[slot_id_str]
                    slot_id = None
                    try:
                        slot_id = int(slot_id_str)
                    except:
                        print("smula ig")
                        continue
                    
                    slot = None

                    try:
                        slot = RoketModuleSlot(
                                                slotId=slot_id,
                                                name=loaded_slot["name"],
                                                position=loaded_slot["position"],
                                                allowedModuleTypes=loaded_slot["allowed_module_types"]
                                            ) # modules have to be loaded later from a save
                        
                        module_slots[slot_id] = slot

                    except:
                        print("bad luck ~ Yoru")
                        continue

                # create collider
                collision_rect = pg.Rect(
                    0,
                    0,
                    body["collider_size"][0],
                    body["collider_size"][1]
                )

                collision_rect.center = body["collider_offset"]

                # build final ship body ## BODIES DO NOT EXPLICITLY SAVE ACTIVE MODULES IN SLOTS - saved in game/hangar saves
                self.mod_bodies[body_name] = RoketBody(
                                                        name=body_name,
                                                        displayName=body["display_name"],
                                                        baseLives=body["base_lives"],
                                                        baseSprites=body_sprite,
                                                        position=(0, 0),
                                                        size=body["size"],
                                                        collisionRect=collision_rect,
                                                        moduleSlots=module_slots
                                                        )

        # debug
        print("--------\nLoaded ships:\n")

        for ship_name, ship in self.mod_bodies.items():
            print(f"{ship.get_property('displayName')} ({ship.name})")

        print("")
    
    def _load_module_types(self, source:list):

        for single_souce in source:
            data = JsonLoader.load_from_file(single_souce)
            for module_type in data[md.MOD_FEATURE_MODULE_TYPE]:
                if module_type not in self.mod_module_types:
                    self.mod_module_types.append(module_type)
                else:
                    print(f"{__name__}:module_type_loader: module type {module_type} already loaded; skipping")

        # debug
        print("--------\nLoaded module types:\n")

        for module_type in self.mod_module_types:
            print(module_type)

        print("")
    
    def _load_modules(self, source:list):
    
        for single_source in source:
            data = JsonLoader.load_from_file(single_source)
            for module_name, module in data[md.MOD_FEATURE_MODULE].items():

                # prepare sprites
                loaded_sprite_path = module["sprite"]

                # prepare prefix
                sprite_path_prefix = None

                if module["sprite_source"] == "internal":
                    sprite_path_prefix = INTERNAL_SPRITE_PATH
                elif module["sprite_source"] == "external":
                    sprite_path_prefix = EXTERNAL_SPRITE_PATH
                else:
                    sprite_path_prefix = "" # when using fully custom paths

                sprite_path = sprite_path_prefix + loaded_sprite_path

                # generate sprite name
                sprite_name = f"{module_name}_module"

                sprite = self.app.sprite_handler.load_sprite(sprite_name, sprite_path, (100,100), "ca")

                module_sprite = flatpane("sprite", {"main":sprite}, sprite="main")

                self.mod_modules[module_name] = RoketModule(
                                                                module_name,
                                                                module["display_name"],
                                                                module["module_type"],
                                                                1,
                                                                1,
                                                                module["modifiers"],
                                                                module_sprite
                                                            )
            
        # debug
        print("--------\nLoaded modules:\n")

        for module_name, module in self.mod_modules.items():
            print(f"{module.displayName} ({module.name}; {module.modType})")

        print("")

    def _load_spawnables(self, source:list):
    
        for single_source in source:
            data = JsonLoader.load_from_file(single_source)
            for spawnable_name, spawnable in data[md.MOD_FEATURE_SPAWNABLE].items():

                # prepare sprites
                loaded_sprite_paths = spawnable["animation_sprites"]

                # prepare prefix
                sprite_path_prefix = None

                if spawnable["sprite_source"] == "internal":
                    sprite_path_prefix = INTERNAL_SPRITE_PATH
                elif spawnable["sprite_source"] == "external":
                    sprite_path_prefix = EXTERNAL_SPRITE_PATH
                else:
                    sprite_path_prefix = "" # when using fully custom paths

                # output sprite dict
                sprite_dict = {}

                # load sprites
                for sprite_index in range(len(loaded_sprite_paths)):
                    sprite_path = sprite_path_prefix + loaded_sprite_paths[sprite_index]

                    # generate sprite name
                    sprite_name = f"{spawnable_name}_anim_{sprite_index}"

                    sprite_dict[sprite_index] = self.app.sprite_handler.load_sprite(sprite_name, sprite_path, (100,100), "ca")


                # create final flatpane
                spawnable_sprite = flatpane("sprite", sprite_dict, sprite=0)

                # collider
                collision_rect = pg.Rect(
                    0,
                    0,
                    spawnable["collider_size"][0],
                    spawnable["collider_size"][1]
                )

                navigator = Navigator(self, spawnable["navigator"])

                # spawnable
                self.mod_spawnables[spawnable_name] = SpawnablePrefab( # the spawnable prefab is used ## yeah its late 
                    appInstance=self.app,
                    name=spawnable_name,
                    displayName=spawnable["display_name"],
                    collider=collision_rect,
                    sprites=spawnable_sprite,
                    navigator=navigator,
                    actions=spawnable["actions"],
                    moveSpeed=spawnable["speed"]
                )

        # debug
        print("--------\nLoaded spawnables:\n")

        for spawnable_name, spawnable in self.mod_spawnables.items():
            print(f"{spawnable.spawnableDisplayName} ({spawnable.spawnableName})")

        print("")

    def _load_environments(self, source:list):

        for single_source in source:
            data = JsonLoader.load_from_file(single_source)
            for environment_name, environment in data[md.MOD_FEATURE_ENV].items():
                env = Environment(
                    appInstance=self.app,
                    backgroundColor=environment["background_color"],
                    objectEvents=environment["environment_object_events"]
                )

                self.mod_environments[environment_name] = env

        # debug
        print("--------\nLoaded environments:\n")
        
        for environment_name, environment in self.mod_environments.items():
            print(f"{environment_name}, with {len(environment.objectEvents["random"]) + len(environment.objectEvents["forced"])} events")

        print("") # sep

    def _load_levels(self, source:list):
        
        for single_source in source:
            data = JsonLoader.load_from_file(single_source)
            for level_name, level in data[md.MOD_FEATURE_LEVEL].items():
                lev = Level(
                    appInstance=self.app,
                    displayName=level["display_name"],
                    icon=level["icon"], # needs to be loaded and scaled actually or use the image frame idk
                    stages=level["stages"],
                    requirements=level["requirements"],
                    allowedShips=level["allowed_ships"],
                    disallowedShips=level["disallowed_ships"]
                )

                self.mod_levels[level_name] = lev

        # debug
        print("--------\nLoaded levels:\n")

        for level_name, level in self.mod_levels.items():
            print(f"{level.displayName} ({level_name})")

        print("") # sep

    def _load_careers(self, source:list):

        for single_source in source:
            data = JsonLoader.load_from_file(single_source)
            for career_name, career_data in data[md.MOD_FEATURE_CAREER].items():
                career = Career(
                    appInstance         =self.app,
                    displayName         =career_data["display_name"],
                    icon                =career_data["icon"], # needs to be loaded and scaled actually or use the image frame idk
                    levels              =career_data["levels"],
                    reqBeatenLevels     =career_data["requirements"]["beaten_levels"],
                    reqBeatenCareers    =career_data["requirements"]["beaten_careers"],
                    allowedShips        =career_data["allowed_ships"],
                    disallowedShips     =career_data["disallowed_ships"]
                )

                self.mod_careers[career_name] = career

        # debug
        print("--------\nLoaded careers:\n")

        for career_name, career in self.mod_careers.items():
            print(f"{career.displayName} ({career_name})")

        print("") # sep

    # localization shenanigans
    def _load_localization_resource(self, path:str|list[str]):
        paths = []
        
        code = None
        name = None

        if type(path) == str:
            paths.append(path)
        else:
            paths = path

        for path in paths:

            loaded_localization = JsonLoader.load_from_file(path)

            code = loaded_localization['code']
            name = loaded_localization['name']
            path = path

            self._create_localization_resource(code, name, path)
        
        # debug
        print("--------\nLoaded localization resource:\n")

        print(f"{name} ({code})")

        print("") # sep
    
    def _create_localization_resource(self, localizationCode:str, localizationName:str, localizationPath:str): # dont yell at me, i get it. this whole thing sucks ass (but it works haha)
        if localizationCode in [r.get_code() for r in self.mod_localizations]:
            [r for r in self.mod_localizations if r.get_code() == localizationCode][0].add_path(localizationPath)
        else:
            self.mod_localizations.append(LocalizationResource(localizationCode, localizationName, [localizationPath]))

    def _load_default_localization(self):
        # load default localization
        loaded_localization = JsonLoader.load_from_file(DEFAULT_LOCALIZATION_PATH)

        self.app.texts = loaded_localization["texts"]

    def use_localization(self, localizationCode:str="en"):

        # load default localization
        loaded_localization = JsonLoader.load_from_file(DEFAULT_LOCALIZATION_PATH)

        self.app.texts = loaded_localization["texts"]

        # load new localization
        localization_res = [r for r in self.mod_localizations if r.get_code() == localizationCode][0] #self.localization_code][0]

        for path in localization_res.get_paths():
            loaded_localization = JsonLoader.load_from_file(path)

            # replace default localization
            for text in loaded_localization["texts"]:
                self.app.texts[text] = loaded_localization["texts"][text]

        # debug
        print(f"{__name__}: applied localization: {localization_res.get_code()} ({localization_res.get_name()})")

    # VALIDATION

    def _validate_loaded_mods(self):
        pass