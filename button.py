import pygame.font

class Button:

    def __init__(self, ai_settings, screen, msg):
        """ initial button attributr """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set button size and others attribute
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # create object of button rect and set to center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # title of button
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ render front to image and set it to center of button """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # draw a button with color and draw text
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
