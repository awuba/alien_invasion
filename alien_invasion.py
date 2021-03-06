import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    # initilize game and create screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # create a Play button
    play_button = Button(ai_settings, screen, "Play")
    # create a game states
    stats = GameStats(ai_settings)
    # create scoreboard
    sb = Scoreboard(ai_settings, screen, stats)
    # create a ship
    ship = Ship(ai_settings, screen)
    # create a group of bullet
    bullets = Group()
    # create a group of alien
    aliens = Group()

    # create aliens fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # begin game loop
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

        
run_game()
