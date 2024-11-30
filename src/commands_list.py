import pygame
import time

class CommandsList:
    def __init__(self, screen):
        '''NOTE: We may use any flexible surface, not just the screen.
            However, if instantiated on e.g. the display, the text
            resolution will drop dramatically.'''

        self.surface = screen
        self.font = pygame.font.Font(None, 24)  # Default font
        self.screen_width  = screen.get_width()
        self.screen_height = screen.get_height()
        self.list_visible = False
        self.last_toggle_time = 0  # Track the last time Tab was pressed
        self.toggle_cooldown = 0.3  # Minimum time between toggles (in seconds)
        self.key_options = [
            "HOTKEYS", "", ""
            "Arrows: Move", "",
            "M: Random Map", "",
            "Enter: Auto-move to dest", "",
            "Esc: Quit", "",
        ]
        # NOTE: The extra "" are for carriage returns
        self.panel_color = (50, 50, 50)
        self.text_color = (255, 255, 255)

    def toggle_visibility(self):
        '''Switches visibility of the panel on and off, adding a check to make
        sure that the pressed key is not registered multiple times because of 
        the high refresh rate.'''
        current_time = time.time()
        if current_time - self.last_toggle_time >= self.toggle_cooldown:
            self.list_visible = not self.list_visible
            self.last_toggle_time = current_time

    def draw(self):
        if self.list_visible:
            panel_width = int(0.3 * self.screen_width)  # panel width = 0.3 surface width
            pygame.draw.rect(self.surface, self.panel_color, (0, 0, panel_width, self.screen_height))
            for index, option in enumerate(self.key_options):
                text_surface = self.font.render(option, True, self.text_color)
                self.surface.blit(text_surface, (10, 10 + index * 20))  # Adjust padding as needed