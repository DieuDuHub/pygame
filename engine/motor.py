import pygame
import numpy as np

class Motor:
    def __init__(self, player_object,colision_map,layer_map):
        self.player = player_object
        self.map = colision_map
        self.map_layer = layer_map
        self.targetrect = pygame.Rect(self.player.rect[0], self.player.rect[1], 640, 480)
        self.speed = [0, 0]

        self.is_jumping = False
        self.jump_speed = 10
        self.gravity = 0.1

    def collide_check(self,dx,dy):
        next_tile = self.map.map[
            ((self.player.rect.top + self.targetrect.top + dy)// 16), 
              ((self.player.rect.left + self.targetrect.left + dx) //16) 
            ]
       
        if (next_tile > 0):
            return True
        
        return False
    
    def set_speed(self,dx):
        self.speed[0] = dx

    def compensate_and_move(self):
        if (self.speed[0] < 0): # Move left
            if self.collide_check(0,8): #check left
                self.speed[0] = 0
            elif (self.player.rect[0] > 320): #if sprite was on right , let it move to middle
                self.player.rect[0] += self.speed[0]
                self.speed[0] = 0
            elif (self.targetrect[0] <= 0): # already block
                self.player.rect[0] += self.speed[0]
                self.speed[0] = 0
            

        elif (self.speed[0] > 0): # Move Right
            if (self.collide_check(16,8)): #check right
                self.speed[0] = 0
            elif (self.player.rect[0] < 320): #if sprite was on left , let it move to middle
                self.player.rect[0] += self.speed[0]
                self.speed[0] = 0
            elif (self.targetrect[0] >= self.map.size[1] * self.map.tileset.size[0] - 640): # already block 
                self.player.rect[0] += self.speed[0]
                self.speed[0] = 0

        
        speedy = self.speed[1] # self.speed[1] is huge for the global gravity so need speedy for temporary not applying it
        if (self.speed[1] < 0): # Move Up
            if (self.collide_check(8,0)): #check top
                self.speed[1] = speedy = 0
                self.is_jumping = False
            elif (self.player.rect[1] > 240): #if sprite was on bottopn , let it move to middle
                self.player.rect[1] += self.speed[1]
                speedy = 0
            elif (self.targetrect[1] <= 0): # already block
                self.player.rect[1] += self.speed[1]
                speedy = 0

        elif (self.speed[1] > 0): # Move Down
            if (self.collide_check(8,16)): #check bottom
                self.speed[1] = speedy = 0
                self.is_jumping = False
                self.targetrect[1] =  int(self.targetrect[1] / 16) * 16
            elif (self.player.rect[1] < 240): #if sprite was on bottopn , let it move to middle
                self.player.rect[1] += self.speed[1]
                speedy = 0
            elif (self.targetrect[1] >= self.map.size[0] * self.map.tileset.size[1] - 480):
                self.player.rect[1] += self.speed[1]
                speedy = 0

        self.targetrect = self.targetrect.move(
         self.speed[0],
         speedy)

    def move_and_collide(self):
        # Apply gravity if not jumping
        if not self.is_jumping:
            self.speed[1] += self.gravity
        #elif not self.is_jumping and self.collide_check(8,16):
        #    self.speed[1]  = 0
            #self.targetrect[1] =  int(self.targetrect[1] / 16) * 16
        elif self.is_jumping:
            self.speed[1] += self.gravity
            if self.speed[1] >= 0:
                self.is_jumping = False

        self.compensate_and_move()

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.speed[1] = -self.jump_speed

    def render(self, screen):
        #self.targetrect[0] = self.player.rect[0] - self.targetrect.right // 2
        #self.targetrect[1] = self.player.rect[1] - self.targetrect.bottom // 2
        for layer in self.map_layer:
            screen.blit(layer.image, (0, 0), area=self.targetrect)

        