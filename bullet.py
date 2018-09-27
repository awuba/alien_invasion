import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ manage bullet speed """

    def __init__(self, ai_settings, screen, ship):
        """ create a bullet object at ship """
        super(Bullet, self).__init__()
        self.screen = screen

        # create a bullet rect at (0,0) and set the correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # storage bullet position by float
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """ move up """
        # update bullet position
        self.y -= self.speed_factor
        # update bullet rect
        self.rect.y = self.y

    def draw_bullet(self):
        """ draw bullet at screen """
        pygame.draw.rect(self.screen, self.color, self.rect)
