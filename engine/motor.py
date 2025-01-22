import pygame
import numpy as np

class Motor:
    def __init__(self, player_object,colision_map,layer_map, screen_size=(1024,768)):
        self.player = player_object
        self.map = colision_map
        self.map_layer = layer_map
        self.targetrect = pygame.Rect(self.player.rect[0], self.player.rect[1], screen_size[0], screen_size[1])
        self.speed = [0, 0]
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]

        self.is_jumping = False
        self.jump_speed = 5
        self.gravity = 0.1

    def set_life_manager(self,lifemanager):
        self.life_manager = lifemanager

    def set_speed_and_gravity(self,speed,gravity):
        self.speed = speed
        self.gravity = gravity

    def collide_check(self,dx,dy):

        # Check if out of screen map so return no collide check or superior to map size
        if (self.player.rect.top + self.targetrect.top + dy < 0 or self.player.rect.left + self.targetrect.left + dx < 0 
            or self.player.rect.top + self.targetrect.top + dy > self.map.size[0] * self.map.tileset.height or self.player.rect.left + self.targetrect.left + dx > self.map.size[1] * self.map.tileset.width):
            return False

        map_number =(((self.player.rect.top + self.targetrect.top + dy)// self.map.tileset.height) * self.map.size[0]) + ((self.player.rect.left + self.targetrect.left + dx) // self.map.tileset.width) 
    
        # Supress MirrorV mirror H and rotate value from map_number
        map_number = map_number & 0x00FFFFFF

        # GRab tile number to check if it is a block or not
        next_tile = self.map.map[
            map_number
            ]
      
        if (next_tile > 1):#1 means no tiles 
            return True
        
        return False
    
    def set_speed(self,dx):
        self.speed[0] = dx

    # Manage the movement of the player and the sprite move or screen move following player location around 320/240
    def compensate_collide_and_move(self):
        
        # check how and if move Up or Down or Left or Right
        speedx  = self.speed[0]
        if (self.speed[0] < 0): # Move left
            self.player.set_direction(1)
            if self.collide_check(0,self.player.height // 2): #check left
                self.speed[0] = speedx = 0
                self.player.set_status(0)
            elif (self.player.rect[0] > self.screen_width / 2): #if sprite was on right , let it move to middle
                self.player.rect[0] += speedx
                speedx = 0
                self.player.set_status(1)
            elif (self.targetrect[0] <= 0): # already block
                self.player.rect[0] += speedx
                speedx = 0
                self.player.set_status(1)  
            else:
                self.player.set_status(1)  
        elif (self.speed[0] > 0): # Move Right
            self.player.set_direction(0)
            self.player.set_status(0)
            if (self.collide_check(self.player.width ,self.player.height // 2)): #check right
                self.speed[0] = speedx = 0
            elif (self.player.rect[0] < self.screen_width / 2): #if sprite was on left , let it move to middle
                self.player.rect[0] += self.speed[0]
                speedx = 0
                self.player.set_status(1)
            elif (self.targetrect[0] >= self.map.size[1] * self.map.tileset.size[0] - self.screen_width): # already block 
                self.player.rect[0] += self.speed[0]
                speedx = 0
                self.player.set_status(1)
            else:
                self.player.set_status(1)  #Default from frame move
        else:
            self.player.set_status(0)

        speedy = self.speed[1] # self.speed[1] is huge for the global gravity so need speedy for temporary not applying it
        if (self.speed[1] < 0): # Move Up
            if (self.collide_check(self.player.width // 2,0)): #check top
                self.speed[1] = speedy = 0
                self.is_jumping = False
            elif (self.player.rect[1] > self.screen_height / 2): #if sprite was on bottopn , let it move to middle
                self.player.rect[1] += self.speed[1]
                speedy = 0
            elif (self.targetrect[1] <= 0): # already block
                self.player.rect[1] += self.speed[1]
                speedy = 0

        elif (self.speed[1] > 0): # Move Down
            if (self.collide_check(self.player.width // 2,self.player.height)): #check bottom
                self.speed[1] = speedy = 0
                self.is_jumping = False
                self.targetrect[1] =  int(self.targetrect[1] / self.map.tileset.height) * self.map.tileset.height
                self.player.rect[1] = int(self.player.rect[1] / self.map.tileset.height) * self.map.tileset.height
            elif (self.player.rect[1] < self.screen_height / 2): #if sprite was on bottopn , let it move to middle
                self.player.rect[1] += self.speed[1]
                speedy = 0
            elif (self.targetrect[1] >= self.map.size[0] * self.map.tileset.size[1] - self.screen_height):
                self.player.rect[1] += self.speed[1]
                speedy = 0

        self.targetrect = self.targetrect.move(
         speedx,
         speedy)

        self.speed[0] = 0

    # Manage jump and gravity
    def move_and_collide(self):
        # Apply gravity if not jumping
        if not self.is_jumping:
            self.speed[1] += self.gravity
        # check if on top of jump so stop jumping
        elif self.is_jumping:
            self.speed[1] += self.gravity
            if self.speed[1] >= 0:
                self.is_jumping = False
        # Define screen or sprite movement and check collide
        self.compensate_collide_and_move()

        self.life_manager.update_life(self.targetrect)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.speed[1] = -self.jump_speed

    def render(self, screen):
        #self.targetrect[0] = self.player.rect[0] - self.targetrect.right // 2
        #self.targetrect[1] = self.player.rect[1] - self.targetrect.bottom // 2
        for layer in self.map_layer:
            screen.blit(layer.image, (0, 0), area=self.targetrect)

        