import pygame


class Bird:
    def __init__(self, sources, win_width, win_height):
        self.imgs = []

        for s in sources:
            self.imgs.append(pygame.image.load(s))

        self.x = win_width // 2 - self.imgs[0].get_width() // 2
        self.y = win_height // 2 - self.imgs[0].get_height() // 23
        self.tick_count = 0
        self.img_tick = 0
        self.img_state = 0
        self.vel = 0

    def draw(self, win, hit_box=False):
        self.img_tick += 1

        if self.img_tick == 5:
            self.img_tick = 0
            self.img_state = (self.img_state + 1) % len(self.imgs)

        win.blit(self.imgs[self.img_state], (self.x, self.y))

        if hit_box:
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.imgs[self.img_state].get_width(),
                                                self.imgs[self.img_state].get_height()), 3)

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 10:
            d = 10

        if d < 0:
            d -= 2

        self.y += d

    def jump(self):
        self.vel = -8.5
        self.tick_count = 0

    def collide(self, pipe, base, debug=False):
        w, h = self.imgs[0].get_width(), self.imgs[0].get_height()

        if self.y > base.y:
            if debug:
                print(f"{self.y} > {base.y}")
            return True

        if self.x + w > pipe.x and self.x < pipe.x + pipe.img.get_width():
            if not (self.y + h < pipe.y and self.y > pipe.y - pipe.gap):
                if debug:
                    print(f"x: {pipe.x} < {self.x + w} & {self.x} < {pipe.x + pipe.img.get_width()}\t" +
                          f"y: {self.y} < {pipe.y - pipe.gap} | {pipe.y} < {self.y + h}")
                return True
        return False
