import pygame

def set_end_point(surface):
    '''
    Waits for the user to left-click and returns the coordinates of the click.
    '''
    waiting_for_click = True
    print("set_end_point:: Waiting for mouse click...")
    
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse click coordinates
                mouse_x, mouse_y = event.pos
                print(f"set_end_point:: Mouse clicked at: ({mouse_x}, {mouse_y})")
                waiting_for_click = False  # Exit loop after click
                return mouse_x, mouse_y

        # Update the screen or show a text prompt
        font = pygame.font.Font(None, 32)
        prompt = font.render("Click anywhere to set the endpoint", True, (255, 255, 255))

        # Get the dimensions of the text and the screen
        text_width = prompt.get_width()
        text_height = prompt.get_height()
        surface_width = surface.get_width()

        # Calculate position to center the text horizontally at the top of the surface
        x_position = (surface_width - text_width) // 2  # Center horizontally
        y_position = 20  # Top padding

        # Blit the text onto the surface
        surface.blit(prompt, (x_position, y_position))
        pygame.display.flip()