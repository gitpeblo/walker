import pygame
from pygame.locals import * # keys

import glob
import math
import numpy as np

# src:
from src.astar import astar

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
        self.waypoints = None
        # current waypoints list (only relevant when `status`=='moving_to')

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

    def move_to(self, x_target_map, y_target_map, speed=0.5):
        '''Moves the player from current position to the desired target, along
        a straight path.

        Parameters
        ----------
        x_target_map, y_target_map : float
            Target coordinates in map reference.
        speed : float
            Cruising speed.
        '''

        # Calculating direction of movement:
        dx = x_target_map - self.x_map
        dy = y_target_map - self.y_map
        d = (dx**2 + dy**2)**0.5
        # distance from current waypoint
        theta = math.atan2(dy, dx)

        print('\tmove_to:: (x, y): %.2f %.2f --> %.2f %.2f d=%.2f' % \
                (self.x_map, self.y_map, x_target_map, y_target_map, d))

        if d > speed:
        # NOTE: `d` and `speed` have the same units of space, here, because
        #        the speed is implictly multiplied by the clock tick.
            print('\tmove_to:: Taking a step')
            self.x_map += speed * math.cos(theta)
            self.y_map += speed * math.sin(theta)
            self.moving_status = 'moving_to'
        else:
            print('\tmove_to:: Target reached')
            # Centering exactly on target:
            self.x_map = x_target_map
            self.y_map = y_target_map
            self.moving_status = 'target_reached'

    def find_path(self, x_target_map, y_target_map,
                  map_data=None, method='AStar'):                  
        '''Seeks for a valid path from the current player position to the
        target position, via a list of waypoints.

        For AStar to work, the current position and the target position are
        approximated to the closest integer (i.e., tile center)
        
        Parameters
        ----------
        x_target_map, y_target_map : float
            Target coordinates in map reference.
            If method is 'AStar', the input coordinates get rounded to the
            closest integer (the algorithm works exclusively with integers).
        map_data : list of lists
            Map data in numerical form (0 = no tile).
        method : str (default is 'AStar')
            Path-finding method.
            Placeholder for future alternatives.          

        Returns
        -------
        waypoints : list, optional (default: [[0, 0]])
            List of tuples [x_map, y_map], where each tuple is an intermediate
            target to go through.
        '''
        if method == 'AStar':
        
            # Round target coords to closest tile center:
            x_target_map = int(x_target_map)
            y_target_map = int(y_target_map)

            # Check that target tile is not empty, or else AStar gets stuck:
            map_value = map_data[y_target_map][x_target_map]
            if map_value == 0:
                print('find_path:: Target tyle is empty')
                self.status = 'idle'
                return 1

            # Inverting map values, to conform AStar's expected input:
            map_astar = np.array(map_data, dtype=np.uint8).T
            # map's x and y get switched in numpy, hence the transpose
            map_astar = 1 - map_astar

            start = (int(self.x_map), int(self.y_map))
            goal  = (x_target_map, y_target_map)
            print('\tfind_path:: start %s | goal %s' % (start, goal))
            
            path = astar(map_astar, start, goal)[1:]
            # NOTE: The first element in the path is dropped, as it is the
            #       starting position.

            # Convert each tuple to a list:
            path = [list(tup) for tup in path]
            print('\tfind_path:: path\n\t\t%s' % path)

        return path

    def move_through(self, events, waypoints=[[0, 0]], speed=0.1):
        '''Moves the player through a list of waypoints.

        For AStar to work, the current position and the target position are
        approximated to the closest integer (i.e., tile center)
        
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
                    self.status = 'moving_through'

        if self.status == 'moving_through':
            
            # Initialize waypoints, if none is set:
            if self.waypoints is None: 
                self.waypoints = waypoints
            
            x_target_map, y_target_map = self.waypoints[0]
            # NOTE: The current waypoint is always the first in the list, and
            #       it gets dropped when it is reached.

            self.move_to(x_target_map, y_target_map, speed=speed)

            if self.moving_status == 'target_reached':
                # Drop first iteator element:
                self.waypoints.pop(0)

                if self.waypoints:
                    print('move_through:: Next waypoint: %s' %\
                          self.waypoints[0])

                else:
                    print('move_through:: Terminating movement')
                    self.status = 'idle'
                    return 0

            


    """
    def move_through(self, events, waypoints=[[0, 0]],
                     map_data=None, speed=0.5, method='AStar'):
        '''Moves the player through a list of waypoints.

        For AStar to work, the current position and the target position are
        approximated to the closest integer (i.e., tile center)
        
        Parameters
        ----------
        events : list
            List of events as returned by pygame.event.get()
        waypoints : list, optional (default: [[0, 0]])
            List of tuples [x_map, y_map], where each tuple is an intermediate
            target to go through.
        map_data : list of lists
            Map data in numerical form (0 = no tile).
        method : str (default is 'AStar')
            Pathfinding method.            
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
            
            # Initialize waypoints, if none is set:
            if self.waypoints is None: 
                self.waypoints = waypoints
            
            x_target_map, y_target_map = self.waypoints[0]
            # NOTE: The current waypoint is always the first in the list, and
            #       it gets dropped when it is reached.
            
            if method == 'AStar':
            
                # Round to closest tile center:
                x_target_map = int(x_target_map)
                y_target_map = int(y_target_map)

                # Check the target tile is not empty, or else AStar gets stuck:
                map_value = map_data[y_target_map][x_target_map]
                if map_value == 0:
                    print('move_to:: Target tyle is empty')
                    self.status = 'idle'

                # Inverting map values, to conform AStar's expected input:
                map_astar = np.array(map_data, dtype=np.uint8).T
                # map's x and y get switched in numpy, hence the transpose
                map_astar = 1 - map_astar

                start = (int(self.x_map), int(self.y_map))
                goal  = (x_target_map, y_target_map)
                print('\tmove_to:: start %s | goal %s' % (start, goal))
                
                path = astar(map_astar, start, goal)
                print('\tmove_to:: path', path)

            # Calculating direction of movement:
            dx = x_target_map - self.x_map
            dy = y_target_map - self.y_map
            d = (dx**2 + dy**2)**0.5
            # distance from current waypoint
            theta = math.atan2(dy, dx)

            print('\tmove_to:: (x, y): %.2f %.2f --> %.2f %.2f d=%.2f' % \
                  (self.x_map, self.y_map, x_target_map, y_target_map, d))

            if d > speed:
            # NOTE: `d` and `speed` have the same units of space, here, because
            #        the speed is implictly multiplied by the clock tick.
                print('\tmove_to:: Taking a step')
                self.x_map += speed * math.cos(theta)
                self.y_map += speed * math.sin(theta)
                self.status = 'moving_to'
            else:
                # Drop first iteator element:
                self.waypoints.pop(0)
                if self.waypoints:
                    print('move_to:: Next waypoint: %s' % self.waypoints[0])

                    # Check that next waypoint tile is not empty:
                    # (or else AStar will stuck at the next invocation)
                    x_target_map_next, y_target_map_next = self.waypoints[0]

                    if method == 'AStar':
                        # Round to closest tile center:
                        x_target_map_next = int(x_target_map_next)
                        y_target_map_next = int(y_target_map_next)
                    
                    if map_data[y_target_map_next][x_target_map_next] == 0:
                        print('move_to:: Next waypoint tyle is empty')
                        print('move_to:: Terminating movement')
                        self.status = 'idle'
                        return 1

                else:
                    print('move_to:: Terminating movement')
                    # Centering exactly on target:
                    self.x_map = x_target_map
                    self.y_map = y_target_map
                    self.status = 'idle'
                    return 0
    """;
