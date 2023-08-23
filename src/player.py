import pygame
from pygame.locals import * # keys

import glob
import math

class Player:

    def __init__(self, main, spawn_x_map=0, spawn_y_map=0):
        self.main = main
        # Current sprite:
        self.x_map = spawn_x_map
        self.y_map = spawn_y_map
        self.z_map = 0
        # position (initialized to spawn)
        self.sprite = None
        # object
        self.sprite_name = None
        # name of current sprite
        self.height = None
        self.width = None
        # size
        self.on_tile = None
        # is player on a tile?
        self.status = 'idle'
        # either of ['idle', 'moving_to']

        # Loading all sprites:
        self.sprites = self.load_sprites_player('data/images/sprites/player')

        # Initializing sprite to the first sprite:
        self.sprite_name = list(self.sprites.keys())[0]
        self.sprite      = self.sprites[self.sprite_name]
        _, _, self.width, self.height = self.sprite.get_rect()
        # size of the initialized sprite

    def load_sprites_player(self, path_sprites_player):
        sprites = {}
        # Loading all available sprites and organizign them in a dictionary
        # indexed by sprite name:
        for filename in glob.glob(path_sprites_player + '/*.png'):
            sprite = pygame.image.load(filename).convert()
            sprite.set_colorkey((0, 0, 0))

            sprite_name = filename.split('/')[-1].split('.')[0]
            sprites[sprite_name] = sprite
        
        return sprites

    def move(self, keys, speed=0.1):

        if keys[pygame.K_UP]:
            self.x_map -= speed
            self.y_map -= speed
        if keys[pygame.K_DOWN]:
            self.x_map += speed
            self.y_map += speed
        if keys[pygame.K_LEFT]:
            self.x_map -= speed
            self.y_map += speed
        if keys[pygame.K_RIGHT]:
            self.x_map += speed
            self.y_map -= speed

    def drop(self, on_tile, speed=0.5):
        if not on_tile:
            self.x_map += speed
            self.y_map += speed
    
    def move_through(self, waypoints):
        #
        pass

    def move_to(self, events, waypoints=[[0, 0]], speed=0.1):
        '''Moves the player through a list of waypoints.
        
        Parameters
        ----------
        events : list
            List of events as returned by pygame.event.get()
        waypoints : list, optional (default: [[0, 0]])
            List of tuples [x_map, y_map], where each tuple is an intermediate
            target to go through.
        speed : float
            Cruising speed.
        '''

        # Checking wether to initiate a "move to":
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    print('move_to:: Initiating movement')
                    self.status = 'moving_to'

        if self.status == 'moving_to':
            for  [x_target_map, y_target_map] in waypoints:

                print('====', x_target_map, y_target_map)

                # Calculating direction of movement:
                dx = x_target_map - self.x_map
                dy = y_target_map - self.x_map
                d = (dx**2 + dy**2)**0.5
                theta = math.atan2(dy, dx)

                if self.status == 'moving_to':

                    if d > speed:
                    # NOTE: `d` and `speed` have the same units of space, here, because
                    #        the speed is implictly multiplied by the clock tick.
                        print('\tmove_to:: Taking a step')
                        self.x_map += speed * math.cos(theta)
                        self.y_map += speed * math.sin(theta)
                        self.status = 'moving_to'
                    else:
                        print('move_to:: Terminating movement')
                        self.x_map = x_target_map
                        self.y_map = y_target_map
                        self.status = 'idle'

