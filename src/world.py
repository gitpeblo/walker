import pygame

import numpy as np
import glob
import pandas as pd
import os

# src:
from src.map_generators import create_simple_map, create_traversable_map,\
                               write_map_to_file

class World:
    '''
    The world class, where everything visible in the view belongs.
    '''
    def __init__(self, main):
        self.main = main
        
        self.path_tmp = 'data/tmp'
        if not os.path.exists(self.path_tmp): os.makedirs(self.path_tmp) 

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

    def generate_map(self, width, height, type='simple', load=True):
        '''
        Invokes a map generator and stores the map in the relevant folder.
        
        Pramaters
        ---------
        width : int
            Desired map width in pixels.
        height : int
            Desired map height in pixels.
        type : str (default: 'simple')
            Type of map to be generated, used to invoke different generators:
            - 'simple': `create_simple_map`
            - 'traversable': `create_traversable_map`
        load : bool (default: True)
            If True, loads the generated map and replaces the existing one.
        '''
        
        self.path_tmp_maps = self.path_tmp + '/maps'
        if not os.path.exists(self.path_tmp_maps):
            print('generate_map:: %s created' % self.path_tmp_maps)
            os.makedirs(self.path_tmp_maps) 

        if type == 'simple':
            map_data = create_simple_map(width, height, p_hole=0.5)
        if type == 'traversable':
            map_data = create_traversable_map(width, height, p_tile=0.5)

        # Write map to file:
        path_to_basename = self.path_tmp_maps+'/map.txt'
        # path to basename file: it will be renamed with sequential integers
        # (i.e., ..._0.txt, ..._1.txt, etc.), according to the already existing
        # maps in the target folder.
        path_to_map = write_map_to_file(map_data, path_to_basename)

        if load: self.load_map(path_to_map)