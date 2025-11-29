import pygame as pg
""" from scripts.colors import * """
from vuilib.vui_flatpane import flatpane
""" from scripts.datablock import Datablock """

def convert_to_flatpane(imgs: dict):
    flatpanes = {}
    for i in imgs:
        flatpanes[i] = (flatpane("sprite", imgs, sprite=i))

    return flatpanes