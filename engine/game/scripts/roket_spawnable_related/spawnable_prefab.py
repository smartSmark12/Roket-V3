from engine.game.scripts.roket_spawnable_related.spawnable_object import SpawnableObject
from game.scripts.roket_spawnable_related.spawnable_navigator import Navigator
from vuilib.vui_flatpane import flatpane

import pygame as pg

class SpawnablePrefab:
    def __init__(self, appInstance, name:str, displayName:str, collider:pg.Rect, sprites:flatpane, navigator:Navigator, actions:dict, moveSpeed:int|float):
        self.app = appInstance
        self.spawnableName = name
        self.spawnableDisplayName = displayName
        self.spawnableCollider = collider
        self.spawnableSprites = sprites
        self.spawnableNavigator = navigator
        self.spawnableActions = actions
        self.spawnableMoveSpeed = moveSpeed

    def create_spawnable(self, targetPos:tuple):
        spawnable = SpawnableObject(
            self.app,
            self.spawnableName,
            self.spawnableDisplayName,
            self.spawnableCollider,
            self.spawnableSprites,
            self.spawnableNavigator,
            self.spawnableActions,
            self.spawnableMoveSpeed,
            targetPos
        )

        return spawnable