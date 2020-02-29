from pygame.sprite import Sprite
from pygame import Surface
from pygame import Rect


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

    def move_up(self, outer_rect: Rect):
        new_pos = (self.rect.x, self.rect.y - self.step)
        if outer_rect.collidepoint(new_pos):
            self.rect.y = new_pos[1]
            return True
        return False
