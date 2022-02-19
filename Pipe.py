import pygame
import random


class Pipe:
    def __init__(self, source, gap, win_width, lower_bound, upper_bound):
        self.img = pygame.image.load(source)
        self.gap = gap
        self.x = win_width
        self.y = random.randint(upper_bound, lower_bound)

    def draw(self, win, hit_box=False):
        win.blit(self.img, (self.x, self.y))

        upper_pipe = pygame.transform.rotate(self.img, 180)
        win.blit(upper_pipe, (self.x, self.y - self.gap - self.img.get_height()))

        if hit_box:
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.img.get_width(), self.img.get_height()), 3)
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y - self.gap - self.img.get_height(), self.img.get_width(),
                                                self.img.get_height()), 3)

    def move(self, vel):
        self.x -= vel

    def passed_point(self, x):
        return self.x + self.img.get_width() == x

