import pygame.font


class Button():

    def __init__(self, ai_settings, screen, msg):
        """Initialize the attributes of the button."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the size of the button and others attributes
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Create the object of the button rect, and let it be in the middle
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Only need build the tag of button once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """
        Make the rect render into images,
        and make the button on the top middle of it.
        """
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw a button filled in color and then draw the text
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

