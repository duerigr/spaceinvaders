from pygame.sprite import Sprite
from pygame import Surface
from pygame import Rect
from pygame.mixer import Sound
from pygame.mixer import Channel

from ui.config import Config


class Alien(Sprite):

    width = 30
    height = 30
    color = (255, 0, 0)
    moving_right = True

    def __init__(self, center_pos, hp, speed):
        Sprite.__init__(self)

        self.image = Surface([self.width, self.height])
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.center = center_pos

        self.hp = hp

        self.speed = speed

        self.sound_die = Sound(Config.SOUND_DIE)
        self.sound_die.set_volume(1.0)
        self.sound_hit = Sound(Config.SOUND_HIT)
        self.sound_hit.set_volume(1.0)
        self.sound_channel = Channel(3)

    def move_down(self, outer_rect: Rect):
        new_pos = (self.rect.x, self.rect.y + self.speed + self.height)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.y = new_pos[1] - self.height
            return True
        return False

    def move_up(self, outer_rect: Rect):
        new_pos = (self.rect.x, self.rect.y - self.speed)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.y = new_pos[1]
            return True
        return False

    def move_right(self, outer_rect: Rect):
        new_pos = (self.rect.x + self.speed + self.width, self.rect.y)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.x = new_pos[0] - self.width
        else:
            self.moving_right = False

    def move_left(self, outer_rect: Rect):
        new_pos = (self.rect.x - self.speed, self.rect.y)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.x = new_pos[0]
        else:
            self.moving_right = True

    def is_moving_right(self):
        return self.moving_right

    def paint(self, color: (int, int, int)):
        self.color = color
        self.image.fill(self.color)

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.sound_channel.play(self.sound_die)
            self.kill()
        else:
            self.sound_channel.play(self.sound_hit)
