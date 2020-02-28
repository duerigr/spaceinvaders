import pygame
from pygame.locals import *
from ui.config import Config
from ui.menu import Menu


class Main:

    @classmethod
    def init(cls):
        pygame.init()

        screen = pygame.display.set_mode((Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT))

        menu = Menu(screen, cls.__handle_menu_start)

        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    quit()
            menu.mainloop(events)
            pygame.display.flip()

    @classmethod
    def __handle_menu_start(cls):
        pass


Main.init()
