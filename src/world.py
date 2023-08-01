import pygame

import numpy as np
import glob

class World:
    '''
    The world class, where everything visible in the view belongs.
    '''
    def __init__(self, main):
        self.main = main
        
        self.load_map('data/maps/map_test.txt')
        self.load_sprites_maps('data/images/sprites/maps')
        self.load_sprites_player('data/images/sprites/player')

    def load_map(self, path_to_map):
        f = open(path_to_map)
        self.map_data = [[int(c) for c in row] for row in f.read().split('\n')]
        self.map_data = np.array(self.map_data)
        f.close()

        # Create the coordinate grid using meshgrid:
        y, x = np.indices(self.map_data.shape)

        # Converting to array of [x, y] coordinates:
        self.coordinates = np.stack((y.ravel(), x.ravel()), axis=1)

    def load_sprites_maps(self, path_sprites_maps):
        self.sprites_maps = {}
        for filename in glob.glob(path_sprites_maps + '/*.png'):
            sprite = pygame.image.load(filename).convert()
            sprite.set_colorkey((0, 0, 0))

            sprite_name = filename.split('/')[-1].split('.')[0]
            self.sprites_maps[sprite_name] = sprite

    def load_sprites_player(self, path_sprites_player):
        self.sprites_player = {}
        for filename in glob.glob(path_sprites_player + '/*.png'):
            sprite = pygame.image.load(filename).convert()
            sprite.set_colorkey((0, 0, 0))

            sprite_name = filename.split('/')[-1].split('.')[0]
            self.sprites_player[sprite_name] = sprite





