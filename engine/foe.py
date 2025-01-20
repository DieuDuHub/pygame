import pygame
import numpy as np
from enum import Enum

class MovementType(Enum):
    STATIC = 0
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3

class Foe:
    def __init__(self, image, size=(16, 16)):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        self.width = size[0]
        self.height = size[1]
        self.rect = self.image.get_rect()
        # Init always out of screen
        self.rect.left = - size[0]
        self.rect.top = - size[1]
        self.movement_type = MovementType.STATIC

    def move(self, speed):
        self.rect = self.rect.move(speed)
    
    def render(self, screen):
        screen.blit(self.image, self.rect)
    
    def set_movement_type(self,movement_type: MovementType):
        self.movement_type = movement_type