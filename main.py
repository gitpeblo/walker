import pygame
from pygame.locals import * # keys

import sys

# src:
import src.world as world
from src.player import Player

# The main game class that is intantiated on startup:
# see https://github.com/lukasz1985/SREM/blob/master/main.py
class Game:

    def __init__(self, w=900, h=900):
        # Initializing pygame modules:
        pygame.init()

        # Screen setup:
        self.screen = pygame.display.set_mode((w, h),0,32)
        pygame.display.set_caption("rampage")
        self.display = pygame.Surface((300, 300))
        
        # World creation:
        self.world = world.World(self)
        
        # Player control object:
        self.player = Player(self, spawn_x=150 + 2.5, spawn_y=100 - 5)

        # Utilities:
        self.done = False  # A flag for the game loop indicating if the game is done playing.
        self.clock = pygame.time.Clock() # Clock to control the framerate

    def loop(self):
        while not self.done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            if event.type == KEYDOWN:
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

        # Moving player:
        # Get all keys currently pressed, and move when an arrow key is held
        keys = pygame.key.get_pressed()
        self.player.move(keys)


    def draw(self):
        self.display.fill((35,35,35))

        for y, x in self.world.coordinates:
            if self.world.map_data[y][x]:
            # there is a "1" in the map
                pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(x * 10, y * 10, 10, 10), 1)
                self.display.blit(self.world.sprites_maps['grass'], (150 + x * 10 - y * 10, 100 + x * 5 + y * 5))
                #if random.randint(0, 1):
                #    display.blit(grass_img, (150 + x * 10 - y * 10, 100 + x * 5 + y * 5 - 14))
                self.display.blit(self.player.sprites['player_0'], (self.player.x, self.player.y))

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        #pygame.display.update()
        pygame.display.flip()
        # NOTE: Use "flip" over "update", as suggested here: https://www.pygame.org/docs/tut/newbieguide.html


def start():
    game = Game()
    game.loop()


if __name__ == "__main__":
    start()