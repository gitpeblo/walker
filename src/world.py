import pygame

import numpy as np
import glob
import pandas as pd

class World:
    '''
    The world class, where everything visible in the view belongs.
    '''
    def __init__(self, main):
        self.main = main
        
        self.load_map('data/maps/map_test.txt')
        self.load_sprites_maps('data/images/sprites/maps')

        # Capturing tile unit sizes from first the sprite loaded:
        self.map_unit_dx, self.map_unit_dy = \
            list(self.sprites_maps.values())[0].get_size()
        # tile unit sizes in screen pixels

    def load_map(self, path_to_map):
        f = open(path_to_map)
        self.map_data = [[int(c) for c in row] for row in f.read().split('\n')]
        self.map_data = np.array(self.map_data)
        f.close()

        # Create the coordinate grid using meshgrid:
        y_map, x_map = np.indices(self.map_data.shape)

        # Converting to array of [x, y] coordinates:
        self.coordinates = np.stack((y_map.ravel(), x_map.ravel()), axis=1)

        # Map size:
        self.map_shape = self.map_data.shape

    def load_sprites_maps(self, path_sprites_maps):
        self.sprites_maps = {}
        self.sprites_maps_meta = {}
        
        for filename in glob.glob(path_sprites_maps + '/*.png'):
            sprite = pygame.image.load(filename).convert()
            sprite.set_colorkey((0, 0, 0))

            sprite_name = filename.split('/')[-1].split('.')[0]
            self.sprites_maps[sprite_name] = sprite

            filename_meta = filename.strip('png') + 'meta.csv'
            # name of file containing meta info related to map sprite

            df_meta = pd.read_csv(filename_meta, comment='#')

            self.sprites_maps_meta[sprite_name] = {
                'stride_dx': df_meta['stride_dx'].values[0],
                'stride_dy': df_meta['stride_dy'].values[0],
            }




