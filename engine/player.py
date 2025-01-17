import pygame
import numpy as np

class Player:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.left = 320
        self.rect.top = 200

    def move(self, speed):
        self.rect = self.rect.move(speed)
    
    def render(self, screen):
        screen.blit(self.image, self.rect)