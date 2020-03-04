from pygame.sprite import Sprite
from pygame import Surface
from pygame import Rect


class Spaceship(Sprite):

    width = 60
    height = 40
    color = (255, 255, 255)
    step = 10

    def __init__(self, center_pos):
        Sprite.__init__(self)

        self.image = Surface([self.width, self.height])
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.center = center_pos

    def move_down(self, outer_rect: Rect):
        new_pos = (self.rect.x, self.rect.y + self.step + self.height)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.y = new_pos[1] - self.height
            return True
        return False

    def move_up(self, outer_rect: Rect):
        new_pos = (self.rect.x, self.rect.y - self.step)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.y = new_pos[1]
            return True
        return False

    def move_right(self, outer_rect: Rect):
        new_pos = (self.rect.x + self.step + self.width, self.rect.y)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.x = new_pos[0] - self.width
            return True
        return False

    def move_left(self, outer_rect: Rect):
        new_pos = (self.rect.x - self.step, self.rect.y)
        if outer_rect.collidepoint(new_pos[0], new_pos[1]):
            self.rect.x = new_pos[0]
            return True
        return False

    def paint(self, color: (int, int, int)):
        self.color = color
        self.image.fill(self.color)
