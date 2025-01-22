import pygame
import numpy as np
from enum import Enum
from engine import foe

class LifeManager:
    def __init__(self, object_layer,colision_map, size=(16, 16)):
        self.foes = []
        for obj in object_layer:
            print(obj)
            # 1 properties = name of foe
            foe_object = obj["properties"]
            x = obj["x"]
            y = obj["y"]
            self.foes.append(foe.Foe(foe_object,x,y,colision_map))

    def update_life(self,screen_rect):
        for obj in self.foes:
            obj.interact()
            obj.move(screen_rect.left,screen_rect.top)

    def render(self,screen):
        for obj in self.foes:
            #obj.debug()
            obj.render(screen)

