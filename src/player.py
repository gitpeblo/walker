import pygame

import glob

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
   

