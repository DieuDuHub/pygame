import pygame
import numpy as np

class Tilemap:
    def __init__(self, location,tileset, size=(10, 20), rect=None):
        self.size = size
        self.tileset = tileset
        self.location = location
        self.map = np.loadtxt(location, delimiter=',', dtype=int) #np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((self.tileset.size[0]*w, self.tileset.size[1]*h), pygame.SRCALPHA)
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.size[1], self.size[0]
        for i in range(m):
            for j in range(n):
                if self.map[i, j] == -1:
                    self.map[i, j] = 0
                tile = self.tileset.tiles[self.map[i, j]] #+1 becasue first tiles = -1
                self.image.blit(tile, (j*self.tileset.size[0], i*self.tileset.size[1]))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}' 

class Tileset:
    def __init__(self, file, size=(32, 32), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.size, pygame.SRCALPHA)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'