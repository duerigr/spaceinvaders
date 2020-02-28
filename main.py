import pygame
from pygame.locals import *
import random
from ui.config import Config
from ui.menu import Menu
from ui.spaceship import Spaceship


class Main:

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(0, 0)
        self.surface = pygame.display.set_mode((Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT))
        self.menu = Menu(self.surface, self.__handle_menu_start, self.__handle_menu_continue)
        self.player = pygame.sprite.Group()
        self.spaceship = None
        self.enemies = pygame.sprite.Group()
        self.image = pygame.image.load(Config.MAIN_MENU_BACK)
        self.init()

    def init(self):
        self.surface.blit(self.image, self.surface.get_rect())
        clock = pygame.time.Clock()
        while True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.spaceship.paint((random.randint(0, 255),
                                      random.randint(0, 255),
                                      random.randint(0, 255)))
            if keys[pygame.K_ESCAPE] and self.menu.is_disabled():
                pygame.key.set_repeat(0, 0)
                self.menu.enable()
            if keys[pygame.K_DOWN]:
                self.spaceship.move_down(self.surface.get_rect())
            if keys[pygame.K_LEFT]:
                self.spaceship.move_left(self.surface.get_rect())
            if keys[pygame.K_RIGHT]:
                self.spaceship.move_right(self.surface.get_rect())
            if keys[pygame.K_UP]:
                self.spaceship.move_up(self.surface.get_rect())
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    quit()
            self.menu.mainloop(events)
            self.player.update()
            self.surface.blit(self.image, self.surface.get_rect())
            self.player.draw(self.surface)
            pygame.display.flip()
            clock.tick(60)

    def __handle_menu_start(self):
        self.menu.disable()
        self.surface.blit(self.image, self.surface.get_rect())
        if self.spaceship is not None:
            self.spaceship.kill()
        self.spaceship = Spaceship()
        self.player.add(self.spaceship)
        self.player.draw(self.surface)
        pygame.key.set_repeat(1, 1)

    def __handle_menu_continue(self):
        self.menu.disable()
        self.surface.blit(self.image, self.surface.get_rect())
        self.player.draw(self.surface)
        pygame.key.set_repeat(1, 1)


Main()
