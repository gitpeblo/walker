import pygame
from pygame.locals import * # keys

import sys

# src:
import src.world as world
from src.player import Player
from src.utils import coords_map_to_screen, coords_map_to_mini
from src.utils import check_player_on_tile

# The main game class that is intantiated on startup:
# see https://github.com/lukasz1985/SREM/blob/master/main.py
class Game:

    def __init__(self, w=900, h=900):
        # Initializing pygame modules:
        pygame.init()

        # Screen setup:
        self.screen = pygame.display.set_mode((w, h),0,32)
        pygame.display.set_caption("walker")
        self.display = pygame.Surface((300, 300))
        self.offset_x = 150
        self.offset_y = 100
        # offset of layer not to overlap with minimap
        
        # World creation:
        self.world = world.World(self)
        
        # Player control object:
        #self.player_offset_x = self.world.map_unit_dx/2 - 14/2 # == half tile - half player
        #self.player_offset_y = -21 + 5 # == base of the player at a tile stride from top of tile
        # offset to align player with the center of the "surface" of a tile
        self.player = Player(self, spawn_x_map=0, spawn_y_map=0)

        # Utilities:
        self.done = False  # A flag for the game loop indicating if the game is done playing
        self.clock = pygame.time.Clock() # Clock to control the framerate

    def loop(self):
        while not self.done:

            self.events = pygame.event.get()
            for event in self.events:
               if event.type == pygame.QUIT:
                    self.done = True
            if event.type == KEYDOWN: # TODO: need an indent?
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            # LOGICAL UPDATES #################################################

            self.update()

            ###################################################################

            # RENDER GRAPHICS #################################################

            self.draw()
            
            ###################################################################

            #self.update(self.clock)
            self.clock.tick(60)

    def update(self):

        keys = pygame.key.get_pressed()

        # Check if a new map shall be generated:
        if keys[pygame.K_m]:
            self.world.generate_map(15, 15, type='traversable')
            # Add a small delay to prevent multiple press detections:
            pygame.time.delay(100)
            # delay in milliseconds

        # Moving player:
        self.player.move(keys)

        # TODO: Use key parser rather than allow decisions inside methods

        # Checking if the player has to be moved through waypoints:
        if check_player_on_tile(self.player, self.world):
        # skipping if player is free falling
            waypoints = self.player.find_path(6, 13,
                            map_data=self.world.map_data, method='AStar')
            self.player.move_through(self.events, waypoints)

        # Checking if the player is currently over a hole:
        self.player.on_tile = check_player_on_tile(self.player, self.world)
        self.player.drop(self.player.on_tile)

    def draw(self):
        self.display.fill((35,35,35))

        box_dx_mini, box_dy_mini = 7, 7
        # minimap box sizes
        # TODO: Move to external file

        for y_map, x_map in self.world.coordinates:

            if self.world.map_data[y_map][x_map]:
            # there is a "1" in the map

                # Minimap -----------------------------------------------------
                pygame.draw.rect(self.display, (255, 255, 255),\
                    pygame.Rect(x_map*box_dx_mini, y_map*box_dy_mini,\
                                box_dx_mini, box_dy_mini), 1)
                # displaying minimap boxes
                #--------------------------------------------------------------

                # Map ---------------------------------------------------------
                x_tile, y_tile = coords_map_to_screen(x_map, y_map,\
                    self.offset_x, self.offset_y, self.world.sprites_maps_meta['grass'])
                
                self.display.blit(self.world.sprites_maps['grass'],\
                                    (x_tile, y_tile))
                # debug : Show rectangle around each tile:
                #pygame.draw.rect(self.display, (255, 255, 255),\
                #    pygame.Rect(x_tile, y_tile, 20, 24), 1)
                #--------------------------------------------------------------

            # Player ----------------------------------------------------------
            player_x, player_y = coords_map_to_screen(\
                    self.player.x_map, self.player.y_map,\
                    self.offset_x, self.offset_y,\
                    self.world.sprites_maps_meta['grass'], type='player',\
                    world=self.world, player=self.player)

            # Displaying player location on minimap:
            player_x_mini, player_y_mini = coords_map_to_mini(\
                self.player.x_map, self.player.y_map, box_dx_mini, box_dy_mini)
            
            pygame.draw.circle(self.display, 'red',\
                                (player_x_mini, player_y_mini), 3, 1)
            
            self.display.blit(self.player.sprites['player_0'], (player_x, player_y))
            #------------------------------------------------------------------
                
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        #pygame.display.update()
        pygame.display.flip()
        # NOTE: Use "flip" over "update", as suggested here: https://www.pygame.org/docs/tut/newbieguide.html


def start():
    game = Game()
    game.loop()


if __name__ == "__main__":
    start()
