import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ initial aliens and set the begin position """
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load alien image and set rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # each alien at the top-left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # storage the alien float 
        self.x = float(self.rect.x) 

    def check_edges(self):
        """ return True, when the alien at the edge of screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        """ alien shift right """
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """ draw the alien at special position """
        self.screen.blit(self.image, self.rect)

