import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """ init ship and set the start position """
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the ship image and get the rectange of outline
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # set the ship initial position at the bottom-center of screen
        # store float value in ship
        self.center = float(self.screen_rect.centerx)
        self.rect.bottom = self.screen_rect.bottom

        # moving flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ according moving_flag to move ship """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # use self.center to update ship position
        self.rect.centerx = self.center

    def blitme(self):
        """ draw the ship at special position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ set the ship at center-bottom """
        self.center = self.screen_rect.centerx
