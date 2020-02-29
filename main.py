import pygame
from pygame.locals import *
import random
from ui.config import Config
from ui.menu import Menu
from ui.spaceship import Spaceship
from ui.beam import Beam
from ui.alien import Alien


class Main:

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(0, 0)
        self.surface = pygame.display.set_mode((Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT))
        self.player_rect = Rect(0,
                                Config.DISPLAY_HEIGHT - Config.DISPLAY_HEIGHT // 4,
                                Config.DISPLAY_WIDTH,
                                Config.DISPLAY_HEIGHT // 4)
        self.enemy_rect = Rect(0, 0,
                               Config.DISPLAY_WIDTH,
                               Config.DISPLAY_HEIGHT // 2 + Config.DISPLAY_HEIGHT // 4)
        self.menu = Menu(self.surface, self.__handle_menu_start, self.__handle_menu_continue)
        self.player = pygame.sprite.Group()
        self.spaceship = None
        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.beam = None
        self.image = pygame.image.load(Config.MAIN_MENU_BACK)
        self.successtime = None
        self.__init_aliens()
        self.__game()

    def __init_aliens(self):
        for i in range(0, 10):
            alien = Alien(
                (random.randint(Alien.width // 2, self.enemy_rect.width - Alien.width),
                 random.choice(range(Alien.height // 2, self.enemy_rect.height - Alien.height // 2, Alien.height + 2))),
                random.randint(1, 4),
                random.randint(3, 7))
            self.enemies.add(alien)

    def __game(self):
        self.surface.blit(self.image, self.surface.get_rect())
        clock = pygame.time.Clock()
        while True:
            self.__handle_keys()
            self.__handle_lasers()
            self.__handle_enemies()
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    quit()
            self.menu.mainloop(events)

            if self.beam is not None:
                shots = pygame.sprite.spritecollide(self.beam, self.enemies, False)
                if len(shots) > 0:
                    self.beam.kill()
                    self.beam = None
                for dead in shots:
                    dead.hit()
                    dead.paint((random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255)))

            self.player.update()
            self.enemies.update()
            self.lasers.update()
            self.surface.blit(self.image, self.surface.get_rect())
            self.player.draw(self.surface)
            self.enemies.draw(self.surface)
            self.lasers.draw(self.surface)
            self.__handle_end()
            pygame.display.flip()
            clock.tick(60)

    def __handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.spaceship.paint((random.randint(0, 255),
                                  random.randint(0, 255),
                                  random.randint(0, 255)))
            if self.beam is None:
                self.beam = Beam(self.spaceship.rect.center)
                self.lasers.add(self.beam)
        if keys[pygame.K_ESCAPE] and self.menu.is_disabled():
            pygame.key.set_repeat(0, 0)
            self.menu.enable()
        if keys[pygame.K_DOWN]:
            self.spaceship.move_down(self.player_rect)
        if keys[pygame.K_LEFT]:
            self.spaceship.move_left(self.player_rect)
        if keys[pygame.K_RIGHT]:
            self.spaceship.move_right(self.player_rect)
        if keys[pygame.K_UP]:
            self.spaceship.move_up(self.player_rect)

    def __handle_lasers(self):
        if self.beam is None:
            return
        if not self.beam.move_up(self.surface.get_rect()):
            self.beam.kill()
            self.beam = None

    def __handle_enemies(self):
        for alien in self.enemies.sprites():
            if alien.is_moving_right():
                alien.move_right(self.enemy_rect)
            else:
                alien.move_left(self.enemy_rect)

    def __handle_end(self):
        if len(self.enemies.sprites()) == 0:
            if self.successtime is None:
                self.successtime = str(pygame.time.get_ticks() // 1000)
            font = pygame.font.Font(Config.FONT, Config.FONT_SIZE)
            textsurf = font.render("success time " + self.successtime + " sec", True, (255, 255, 255))
            textrect = textsurf.get_rect()
            textrect.center = self.enemy_rect.center
            self.surface.blit(textsurf, textrect)

    def __handle_menu_start(self):
        self.menu.disable()
        self.surface.blit(self.image, self.surface.get_rect())
        if self.spaceship is not None:
            self.spaceship.kill()
        self.spaceship = Spaceship(self.player_rect.center)
        self.player.add(self.spaceship)
        self.player.draw(self.surface)
        for sprite in self.enemies.sprites():
            sprite.kill()
        self.__init_aliens()
        self.enemies.draw(self.surface)
        pygame.key.set_repeat(1, 1)
        self.successtime = None

    def __handle_menu_continue(self):
        self.menu.disable()
        self.surface.blit(self.image, self.surface.get_rect())
        self.player.draw(self.surface)
        self.enemies.draw(self.surface)
        pygame.key.set_repeat(1, 1)


Main()
