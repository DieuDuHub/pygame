import pygame
import numpy as np
from enum import Enum

class MovementType(Enum):
    STATIC = 0
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3

class OptionType(Enum):
    ALLOW_NONE = 0
    ALLOW_JUMPING = 1
    ALLOW_FALLING = 2
    ALLOW_BOTH = 3

class Foe:
    def __init__(self, object,x,y,colision_map):

        for o in object:
            print(o)

            if (o["name"] == "image"):
                image = o["value"]
                size = (16,16)
            if (o["name"] == "movement_type"):
                movement_type = o["value"]
            if (o["name"] == "option_type"):
                option_type = o["value"]
            if (o["name"] == "jump_height"):
                jump_height = o["value"]

                                           
        self.name = image
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        self.width = size[0]
        self.height = size[1]
        self.rect = self.image.get_rect()
        # Init always out of screen
        self.rect.left = - size[0]
        self.rect.top = - size[1]
        # Keep origin location
        self.origin_x = int(x)
        self.origin_y = int(y)
        self.movement_type = MovementType(movement_type)
        self.direction = 0
        self.speedx = 1
        self.jump_speed = jump_height
        self.speedy = 0
        self.gravity = 0.1
        self.map = colision_map
        self.option_type = OptionType(option_type)
        self.is_jumping = False
        self.init = 1

    def move(self, x,y):
        self.rect.left = self.origin_x - x
        self.rect.top = self.origin_y - y

    def collide_check(self,dx,dy):

        map_number = ((self.origin_y + dy) // self.map.tileset.height) * self.map.size[0] + (self.origin_x + dx) // self.map.tileset.width
    
        # Supress MirrorV mirror H and rotate value from map_number
        map_number = int(map_number) & 0x00FFFFFF

        # GRab tile number to check if it is a block or not
        next_tile = self.map.map[
            map_number
            ]
        
        # print((self.origin_y + dy)," ",self.origin_x + dx," ",map_number, " " , next_tile)

        if (next_tile > 1):#1 means no tiles 
            return True
        
        return False    

    def interact(self):
        # gravity by default
        if (not self.is_jumping and not self.collide_check(self.width/2,self.height) and ((self.init == 1) or self.option_type == OptionType.ALLOW_FALLING or self.option_type == OptionType.ALLOW_BOTH)):
            self.speedy += self.gravity
            if (self.speedy >= 10):
                self.speedy = 10
            self.origin_y += self.speedy
        elif (self.init == 1 and self.collide_check(self.width/2,self.height)): #♥if init then let him touch the ground then check option_type
            self.init = 0
        elif (self.is_jumping):
            self.speedy += self.gravity
            self.origin_y += self.speedy
            if (self.collide_check(self.width/2,0) or self.speedy > 0):
                self.is_jumping = False
        else:
            self.speedy = 0
            self.origin_y = (self.origin_y // self.map.tileset.height) * self.map.tileset.height

        if (self.movement_type == MovementType.HORIZONTAL and not self.init == 1 ): # if move horizontal allow
            # Left / Right
            if (self.direction ==0): # Left
                self.origin_x -= self.speedx
                # check if collide left and not jumping and allow to jump
                if (self.collide_check(0,self.height/2) and not self.is_jumping and (self.option_type == OptionType.ALLOW_BOTH or self.option_type == OptionType.ALLOW_JUMPING)):# or not self.collide_check(0,16)): #if block left or there is an hole left
                    #self.direction = 1
                    # check if jump feasible 2 tiles up
                    if (not self.collide_check(0,-2 * self.height) and not self.collide_check(0,-3 * self.height)): # 2 next tiles free so jump
                        self.speedy -= self.jump_speed
                        self.is_jumping = True
                    else:
                        self.direction=1
                # check if block by left or empty tile in left bottom
                elif (not self.is_jumping and self.collide_check(0,self.height/2)) or ((self.option_type != OptionType.ALLOW_FALLING and self.option_type != OptionType.ALLOW_BOTH) and not self.collide_check(0,self.height)):
                    self.direction=1
            elif (self.direction ==1):
                self.origin_x += self.speedx
                if (self.collide_check(self.width,self.height/2) and not self.is_jumping and (self.option_type == OptionType.ALLOW_BOTH or self.option_type == OptionType.ALLOW_JUMPING)):# or not self.collide_check(0,16)): #if block left or there is an hole left
                    #self.direction = 1
                    # check if jump feasible
                    if (not self.collide_check(self.width,-2 * self.height) and not self.collide_check(self.width,-3 * self.height)): # 2 next tiles free so jump
                        self.speedy -= self.jump_speed
                        self.is_jumping = True
                    else:
                        self.direction=0
                # check if block right and empty tile for right bottom
                elif (not self.is_jumping and self.collide_check(self.width,self.height/2)) or ((self.option_type != OptionType.ALLOW_FALLING and self.option_type != OptionType.ALLOW_BOTH) and not self.collide_check(self.width,self.height)):
                    self.direction=0


    def render(self, screen):
        screen.blit(self.image, self.rect)
    
    def set_movement_type(self,movement_type: MovementType):
        self.movement_type = movement_type

    def debug(self):
        print("Foe : " , self.name," ",self.rect.top,"/",self.rect.left)