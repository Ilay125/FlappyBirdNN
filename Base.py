import pygame


class Base:
    def __init__(self, source, win_height):
        self.img = pygame.image.load(source)
        self.y = win_height - self.img.get_height()
        self.xs = [0, self.img.get_width()]

    def draw(self, win, hit_box=False):
        for x in self.xs:
            win.blit(self.img, (x, self.y))

            if hit_box:
                pygame.draw.rect(win, (255, 255, 0), (x, self.y, self.img.get_width(), self.img.get_height()), 3)

    def move(self, vel):
        for i in range(len(self.xs)):
            self.xs[i] -= vel

            if self.xs[i] <= -self.img.get_width():
                self.xs[i] = self.img.get_width()


