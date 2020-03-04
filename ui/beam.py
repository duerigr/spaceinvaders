from pygame.sprite import Sprite
from pygame import Surface
from pygame import Rect
from pygame.mixer import Sound
from pygame.mixer import Channel

from ui.config import Config


class Beam(Sprite):

    width = 3
    height = 20
    color = (0, 255, 0)
    step = 35

    def __init__(self, startpos):
        Sprite.__init__(self)

        self.image = Surface([self.width, self.height])
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.midbottom = startpos

        self.sound = Sound(Config.SOUND_BEAM)
        self.sound.set_volume(0.4)
        self.sound_channel = Channel(2)
        self.sound_channel.play(self.sound)

    def move_up(self, outer_rect: Rect):
        new_pos = (self.rect.x, self.rect.y - self.step)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.y = new_pos[1]
            return True
        return False

    def noise(self):
        # self.sound_channel.play(self.sound)
        pass
