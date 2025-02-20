import pygame
import numpy as np
from enum import Enum

class Animation(Enum):
    STAND = 0
    WALK = 1
    RUN = 2
    JUMP = 3
    ATTACK = 4
    JUMP_ATTACK = 5
    FALL = 6

class Player:
    def __init__(self, image, framesize=(8,2),size=(32, 32)):
        image = pygame.image.load(image)
        self.size = size
        self.width = size[0]
        self.height = size[1]
        
        self.frame_size = framesize
        self.current_animation = Animation.STAND
        self.anim_speed = 10
        self.direction = True
        self.status = Animation.STAND

        self.anim = []
        for i in range(0,framesize[0]):
            img = pygame.Surface(self.size, pygame.SRCALPHA)
            img.blit(image, (0, 0), (i * self.width, 0, *self.size))
            #print("copy from ",i * self.width ," ", *self.size)
            self.anim.append(img)
        
        self.rect = self.anim[0].get_rect()
        self.rect.left = 120
        self.rect.top = 50
        self.rect.width = 32
        self.rect.height = 32

        # Step animtation by tuple (start,end)
        # 0 = STAND, 1 = WALK, 2 = RUN, 3 = JUMP, 4 = ATTACK, 5 = JUMP_ATTACK, 6 = FALL
        #self.anim_step = [(2,3),(0,3),(5,5),(1,1),(1,1),(1,1),(6,6)] #list of frame by id, if 0 only frame 4 and 5 are used, if 1 frame 0 to 3 are used (WALK)   
        self.anim_step = [[1,2],[0,1,2,3,2,1],[5,5],[1,1],[1,1],[1,1],[6,6]] #list of frame by id, if 0 only frame 4 and 5 are used, if 1 frame 0 to 3 are used (WALK)   
        self.current_frame = 0

    def set_direction(self,direction):
        if (direction == 1 ): self.direction = True
        else: self.direction = False

    def set_status(self,status):
        if (self.status != Animation(status)): # reset frame counter if status change
            self.status = Animation(status)   
            self.current_frame = 0#self.anim_step[self.status.value][0] * self.anim_speed # take the first frame of the anim step list        

    def move(self, speed):
        self.rect = self.rect.move(speed)
    
    def render(self, screen):  
        # Check next iter
        if ((self.current_frame + 1) // self.anim_speed < len(self.anim_step[self.status.value])):
            self.current_frame += 1
        else:
            self.current_frame = 0#self.anim_step[self.status.value][0] * self.anim_speed

        #print(self.current_frame , " ",len(self.anim_step[self.status.value])," " ,self.current_frame // self.anim_speed)
        frame_to_show  = self.anim_step[self.status.value][self.current_frame // self.anim_speed]
        screen.blit(pygame.transform.flip(self.anim[frame_to_show], self.direction, False), self.rect)


        #print(self.current_frame // self.anim_speed , " ", self.anim_step[self.status.value][0] ," ", self.anim_step[self.status.value][1])