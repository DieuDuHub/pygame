import pygame
import numpy as np
import time

class Tilemap:
    def __init__(self, location,tileset, size=(10, 20), tile_tjs=None,rect=None):
        self.size = size
        self.tileset = tileset
        self.location = location
        #self.map = np.loadtxt(location, delimiter=',', dtype=int) #np.zeros(size, dtype=int)
        self.timer = time.time_ns() // 1_000_000 # for animation of tiles

        self.map = location
        self.tile_tjs = tile_tjs

        # Init tle_anim dict with key of tile and list array of animation and wait time
        self.tile_anim = {}
        if self.tile_tjs != None:
            for i in self.tile_tjs:
                anim =  []
                anim.append((0,100)) # First element is the realtime counter with frame and current ms spend
                for j in i["animation"]:
                    anim.append((j["tileid"],j["duration"]))
                self.tile_anim[i["id"]] = anim
        # Tile animation create a as a dict with :
        # key = tile number
        # value = list of tuple with (frame number, time spend in ms) . First value is 0,0 to keep track of current frame and time
        #print(self.tile_anim)

        w, h = self.size
        self.image = pygame.Surface((self.tileset.size[0]*w, self.tileset.size[1]*h), pygame.SRCALPHA)
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    # Function to update the tile following ms
    def render_animation(self):
        # Calcul time since last iteration
        current_time = (time.time_ns() // 1_000_000) - self.timer
        self.timer = time.time_ns() // 1_000_000
        
        for ta in self.tile_anim : # Loop over all tile animation
           # print(self.tile_anim[ta])
            if (self.tile_anim[ta][0][1] > 0): # if timer not reach
                self.tile_anim[ta][0] = (self.tile_anim[ta][0][0],self.tile_anim[ta][0][1] - current_time)
            else: 
                # Re init current first arraywith corrent value
                current_frame = self.tile_anim[ta][0][0] + 1 # Next frame
                if (current_frame >= len(self.tile_anim[ta])): # If end of animation
                    current_frame = 1 # Restart from 1
                current_time = self.tile_anim[ta][current_frame][1] # Get time of next frame
                self.tile_anim[ta][0] = (current_frame,current_time) # Update current frame and time
                # Manage image updated
                m, n = self.size[1], self.size[0] #INVERTED
                # for each tile in map, replace tile image by the new tile of the animation
                for j in range(m):
                    for i in range(n):   
                        
                        num_tile = self.map[i + self.size[0]* j]
                        num_tile = num_tile - 1

                        if (num_tile != ta):
                            continue
                        
                        #print(ta, " ", current_frame, " ", self.tile_anim[ta][current_frame][0])
                        tile = self.tileset.tiles[self.tile_anim[ta][current_frame][0]] #+1 because first tiles = -1
                        self.image.blit(tile, (i*self.tileset.size[0], j*self.tileset.size[1]))

    def render(self):
        m, n = self.size[1], self.size[0] #INVERTED
        #for i in range(m):
        #    for j in range(n):
                #if self.map[i, j] == -1:
                #    self.map[i, j] = 0
                #tile = self.tileset.tiles[self.map[i, j]] #+1 becasue first tiles = -1
        for j in range(m):
            for i in range(n):   
                num_tile = self.map[i + self.size[0]* j]
                num_tile = num_tile - 1
                if num_tile == -1: # No tile equals transparent part of the png, tile 0
                    num_tile = 0
               
                if num_tile & 0x80000000: is_mirror_v = True 
                else: is_mirror_v = False

                if num_tile & 0x40000000: is_mirror_h = True
                else: is_mirror_h = False

                num_tile = num_tile & 0x000000FF
                
                tile = self.tileset.tiles[num_tile] #+1 because first tiles = -1
                self.image.blit(pygame.transform.flip(tile, is_mirror_v, is_mirror_h), (i*self.tileset.size[0], j*self.tileset.size[1]))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        #print(self.map)
        #print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        #print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}' 

class Tileset:
    def __init__(self, file, size=(32, 32), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.width = self.size[0]
        self.height = self.size[1]
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0]
        dy = self.size[1]
        
        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.size, pygame.SRCALPHA)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'