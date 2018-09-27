import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ response keydown """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """ response keyup """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ detect event of keyboard and mouse """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                    aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
  

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
        bullets, mouse_x, mouse_y):
    """ begin game when click the play button """
    button_cliked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_cliked and not stats.game_active:
        # hide mouse maker
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # clear aliens and bullets
        aliens.empty()
        bullets.empty()

        # create aliens and set to center-bottom of screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """ if not arrived limit then fire bullet """
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """ create an alien and compute how many aliens in a line """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """ compute how many line there are in screen """
    availabe_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(availabe_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ create an alien and add to the current line """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)   


def create_fleet(ai_settings, screen, ship, aliens):
    """ create alien fleet """
    # alien interval is width of alien
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # create the first line alien
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """ do something when aliens arrive edge of screen """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ take fleet drop and change direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check whether bullets shot aliens
    # if hitted then delete
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # delete all bullets, speed up game and create a fleet alien
        bullets.empty()
        ai_settings.increase_speed()

        # up level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """ check alien arrived bottom """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # as alien hit ship process
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """ check high score """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """ response aliens hit ship """
    if stats.ships_left > 0:
        # ships_left minus 1
        stats.ships_left -= 1
        print("ship left: " + str(stats.ships_left))

        # update scoreboard
        sb.prep_ships()

        # clear alien list and bullets list
        aliens.empty()
        bullets.empty()

        # create agroup of aliens, set the ship to center-bottom of screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        print("Game Over !!!")


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """ check fleet edge and update all alien position """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # check alien and ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # check alien arrived bottom of screen
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ update bullets position and delete disappeat bullets """
    # update bullets position
    bullets.update()

    # delete disapper bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """ update the images and switch to new screen """
    # redraw screen every loop
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # display score
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # Show the dispaly
    pygame.display.flip()


