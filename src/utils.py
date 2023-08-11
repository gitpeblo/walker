import pygame

def coords_world_to_screen(x, y, offset_x, offset_y,
                        sprite_stride_dx, sprite_stride_dy):
    '''
    Parameters
    ----------
    x, y : float
        Position in world coordinates.
    '''
    
    x_screen = offset_x + x*sprite_stride_dx - y*sprite_stride_dx
    y_screen = offset_y + x*sprite_stride_dy + y*sprite_stride_dy

    return x_screen, y_screen

def coords_screen_to_world(x_screen, y_screen, offset_x, offset_y, sprite_stride_dx, sprite_stride_dy):    

    x = 0.5*( (x_screen - offset_x)/sprite_stride_dx + (y_screen - offset_y)/sprite_stride_dy )
    y = 0.5*( (y_screen - offset_y)/sprite_stride_dy - (x_screen - offset_x)/sprite_stride_dx )

    return x, y