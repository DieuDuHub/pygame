import pygame
import numpy as np

class Player:
    def __init__(self, image, size=(16, 16)):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        self.width = size[0]
        self.height = size[1]
        self.rect = self.image.get_rect()
        self.rect.left = 400
        self.rect.top = 140

    def move(self, speed):
        self.rect = self.rect.move(speed)
    
    def render(self, screen):
        screen.blit(self.image, self.rect)