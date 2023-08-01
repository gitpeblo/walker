import pygame

import glob

class Player:

    def __init__(self, main, spawn_x=0, spawn_y=0):
        self.main = main
        # Current sprite:
        self.x = spawn_x
        self.y = spawn_y
        # position (initialized to spawn)
        self.sprite = None
        # object
        self.sprite_name = None
        # name of current sprite
        self.height = None
        self.width = None
        # size

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


    def move(self, keys, speed=2):

        if keys[pygame.K_UP]:
            self.y -= speed
        if keys[pygame.K_DOWN]:
            self.y += speed
        if keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_RIGHT]:
            self.x += speed

        WIDTH, HEIGHT = pygame.display.get_window_size()

        # Controlling the object such that it cannot leave the screen's viewpoint:
        if self.x > WIDTH:
            self.x = 0
        if self.y > HEIGHT - self.height:
            self.y = 0
        if self.x < self.width:
            self.x = WIDTH
        if self.y < 0:
            self.y = HEIGHT - self.height


