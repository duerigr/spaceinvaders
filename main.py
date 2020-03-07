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
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=128)
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
        self.enemy_lasers = pygame.sprite.Group()
        self.beam = None
        self.image = pygame.image.load(Config.MAIN_MENU_BACK)
        self.successtime = None
        pygame.mixer.music.load(Config.SOUND_MUSIC)
        pygame.mixer.music.set_volume(0.3)
        self.ticks = 0
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
            self.__handle__enemy_lasers()
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
            self.enemy_lasers.update()
            self.surface.blit(self.image, self.surface.get_rect())
            self.player.draw(self.surface)
            self.enemies.draw(self.surface)
            self.lasers.draw(self.surface)
            self.enemy_lasers.draw(self.surface)
            self.__handle_end()
            pygame.display.flip()
            self.ticks += 60
            clock.tick(60)

    def __handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.beam is None:
                self.beam = Beam(self.spaceship.rect.center)
                self.lasers.add(self.beam)
        if keys[pygame.K_ESCAPE] and self.menu.is_disabled():
            pygame.key.set_repeat(0, 0)
            pygame.mixer.music.pause()
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

    def __handle__enemy_lasers(self):
        if self.spaceship is not None and len(self.enemies.sprites()) > 0:
            shoot_prob = random.random()
            if shoot_prob > 0.95 and len(self.enemy_lasers.sprites()) < 5:
                enemy = random.choice(self.enemies.sprites())
                startpos = enemy.rect.center
                self.enemy_lasers.add(Beam(startpos, 10))
            for laser in self.enemy_lasers.sprites():
                if not laser.move_down(self.enemy_rect.union(self.player_rect)):
                    laser.kill()
            shots = pygame.sprite.spritecollide(self.spaceship, self.enemy_lasers, False)
            for laser in shots:
                laser.kill()
            if len(shots) > 0:
                self.spaceship.hit()
                self.spaceship.paint((random.randint(0, 255),
                                      random.randint(0, 255),
                                      random.randint(0, 255)))

    def __handle_enemies(self):
        for alien in self.enemies.sprites():
            if alien.is_moving_right():
                alien.move_right(self.enemy_rect)
            else:
                alien.move_left(self.enemy_rect)

    def __handle_end(self):
        if self.spaceship.hp <= 0:
            self.enemies.empty()
        if len(self.enemies.sprites()) == 0:
            self.enemy_lasers.empty()
            if self.successtime is None:
                self.successtime = str(self.ticks // 1000)
            font = pygame.font.Font(Config.FONT, Config.FONT_SIZE)
            text = "you dead - time " if self.spaceship.hp <= 0 else "success - time "
            textsurf = font.render(text + self.successtime + " sec", True, (255, 255, 255))
            textrect = textsurf.get_rect()
            textrect.center = self.enemy_rect.center
            self.surface.blit(textsurf, textrect)

    def __handle_menu_start(self):
        self.menu.disable()
        pygame.mixer.music.play(loops=-1)
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
        self.ticks = 0

    def __handle_menu_continue(self):
        self.menu.disable()
        pygame.mixer.music.unpause()
        self.surface.blit(self.image, self.surface.get_rect())
        self.player.draw(self.surface)
        self.enemies.draw(self.surface)
        pygame.key.set_repeat(1, 1)


Main()
