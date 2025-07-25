import pygame

def coords_map_to_screen(x_map, y_map, offset_x, offset_y, sprites_maps_meta,
                         type='tile', world=None, player=None):
    '''
    Converts map coordinates to screen coordinates.
    
    Player:
        When the map coordinates are integers, e.g. (2, 4), the player's sprite
        has to be centered over the top "surface" of a tile's sprite.

        Note that without such additional offset, the player's sprite top-left
        corner is aligned with a tile's top-left corner. 

    Parameters
    ----------
    x_map, y_map : float
        Position in map coordinates.
    offset_x, offset_y : int
        Offset of the isomatric map w/r to the screen origin.
    sprites_maps_meta : dict
        Dictionary containig the strides used to align contiguous sprites,
        in pixels.
    type : str, optional (default: 'tile')
        Type of object for which the conversion shall be performed.
        Can be 'tile' or 'player'.
    '''

    sprite_stride_dx = sprites_maps_meta['stride_dx']
    sprite_stride_dy = sprites_maps_meta['stride_dy']
    
    x = offset_x + x_map*sprite_stride_dx - y_map*sprite_stride_dx
    y = offset_y + x_map*sprite_stride_dy + y_map*sprite_stride_dy

    if type == 'player':
        # Offset to align player's sprite with the center of the "surface" of a
        # tile's sprite:
        player_offset_x = world.map_unit_dx/2 - player.width/2
        # == half tile sprite's width - half player sprite's width 
        player_offset_y = -player.height + sprite_stride_dy
        # == base of the player at a tile's stride from top of the tile

        # Applying player offset:
        x = x + player_offset_x
        y = y + player_offset_y

    return x, y

def coords_map_to_mini(x_map, y_map, box_dx_mini, box_dy_mini):
    '''
    Converts map coordinates to minimap coordinates.
    '''
    x_mini = (x_map+0.5)*box_dx_mini
    y_mini = (y_map+0.5)*box_dy_mini

    return x_mini, y_mini

def check_player_on_tile(player, world):
    '''Checks if player is on a tile (any tile).'''

    if player.z_map < 0: return False
    # player is already free-falling

    player_on_tile = False

    # Iterating over tiles, checking there is one under the player:
    for y_map, x_map in world.coordinates:
        
        if world.map_data[y_map][x_map]:
        # there is a "1" in the map

            #print('........', x_map, y_map)
            #print('........', player.x_map, player.y_map)

            # NOTE: Tile e.g. (0, 0) ranges between -0.5 and 0.5 in both axes 
            if x_map - 0.5 <= player.x_map < x_map + 0.5 and\
               y_map - 0.5 <= player.y_map < y_map + 0.5:
            # A tile has been found under the player! -- interrupting search
                player_on_tile = True
    
    if not player_on_tile:
        player.z_map = -999
        # setting player to free-fall
        # debug: print('Player off tile')
    # debug: if player_on_tile:
    #    print('Player on tile')

    return player_on_tile

"""
def coords_screen_to_map(x, y, offset_x, offset_y, sprite_stride_dx, sprite_stride_dy):    

    x_map = 0.5*( (x - offset_x)/sprite_stride_dx + (y - offset_y)/sprite_stride_dy )
    y_map = 0.5*( (y - offset_y)/sprite_stride_dy - (x - offset_x)/sprite_stride_dx )

    return x_map, y_map

def coords_map_to_screen_player(x_map, y_map, offset_x, offset_y,
                        sprite_stride_dx, sprite_stride_dy, world, player):
    '''
    Converts map coordinates to screen coordinates for the player sprite.
    
    When the map coordinates are integers, e.g. (2, 4), the player's sprite has
    to be centered over the top "surface" of a tile's sprite.

    Note that without such additional offset, the player's sprite top-left
    corner is aligned with a tile's top-left corner. 

    Parameters
    ----------
    x_map, y_map : float
        Position in map coordinates.
    '''
    
    # Map coordinates to top-left corner of corresponding tile:
    x = offset_x + x_map*sprite_stride_dx - y_map*sprite_stride_dx
    y = offset_y + x_map*sprite_stride_dy + y_map*sprite_stride_dy

    # Offset to align player's sprite with the center of the "surface" of a
    # tile's sprite:
    player_offset_x = world.map_unit_dx/2 - player.width/2
    # == half tile sprite's width - half player sprite's width 
    player_offset_y = -player.height + sprite_stride_dy
    # == base of the player at a tile's stride from top of the tile

    # Applying player offset:
    x = x + player_offset_x
    y = y + player_offset_y

    return x, y
"""