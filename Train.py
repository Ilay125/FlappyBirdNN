import numpy as np
import pygame
import os

from Base import Base
from Pipe import Pipe
from Bird import Bird
from NN import NN

assets_dir = os.path.join(os.path.dirname("__file__"), "assets")
bg_IMG = pygame.image.load(os.path.join(assets_dir, "bg.png"))

WIDTH = bg_IMG.get_width()
HEIGHT = bg_IMG.get_height()

clock = pygame.time.Clock()

VEL = 3
GAP = 150

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Train")
pygame.init()


def write(txt, x, y, color=(255, 255, 255), size=50, aa=True, angle=0):
    temp = pygame.font.Font(os.path.join(assets_dir, "FlappyBird.ttf"), size)
    temp = temp.render(txt, aa, color)
    temp = pygame.transform.rotate(temp, angle)
    win.blit(temp, (x, y))


def button(x, y, w, h, color, in_color, text, size, action, args=None):
    mx, my = pygame.mouse.get_pos()
    if x < mx < x+w and y < my < y+h:
        pygame.draw.rect(win, color, (x, y, w, h))
        if pygame.mouse.get_pressed()[0]:
            if args is None:
                action()
            else:
                action(*args)
    else:
        pygame.draw.rect(win, in_color, (x, y, w, h))

    write(text, x, y, size=size)


def init_game(birds_num):
    new_base = Base(os.path.join(assets_dir, "base.png"), HEIGHT)
    new_pipes = [Pipe(os.path.join(assets_dir, "pipe.png"), GAP, WIDTH, HEIGHT // 5 * 3, HEIGHT // 5 * 2)]
    new_birds = [Bird([os.path.join(assets_dir, "birdUp.png"),
                       os.path.join(assets_dir, "birdMid.png"),
                       os.path.join(assets_dir, "birdDown.png")], WIDTH, HEIGHT) for _ in range(birds_num)]
    new_score = 0
    return new_base, new_pipes, new_birds, new_score


def game(nn, pop_size, gen, debug=False):
    base, pipes, birds, score = init_game(pop_size)
    dead = []

    while True:
        if len(dead) == pop_size:
            return

        win.blit(bg_IMG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        for i, bird in enumerate(birds):
            if i not in dead:
                bird.move()
                bird.draw(win, debug)
                if bird.y > 0:
                    nn.fitness[i] += .3

                x = np.array([bird.y, pipes[-1].x, pipes[-1].y])
                if nn.forward_prop(x, i):
                    bird.jump()

                for p in pipes:
                    if p.passed_point(bird.x):
                        nn.fitness[i] += 5

                    if bird.collide(p, base, debug):
                        nn.fitness[i] -= 10
                        dead.append(i)

        for p in pipes:
            p.move(VEL)
            p.draw(win, debug)
            if p.passed_point(birds[0].x):
                score += 1
                pipes.append(Pipe(os.path.join(assets_dir, "pipe.png"), GAP, WIDTH, HEIGHT // 5 * 3, HEIGHT // 5 * 2))

            if p.passed_point(0):
                pipes.remove(p)

        base.move(VEL)
        base.draw(win, debug)

        write(f"{score}", WIDTH // 2, 10, size=70)
        write(f"{gen}", 10, 10, size=50)
        write(f"{len(birds) - len(dead)}", 10, 50, size=50)

        button(10, 450, 100, 30, (255, 0, 0), (150, 0, 0), "save best", 30, nn.save_best)
        clock.tick()
        pygame.display.update()


def main():
    pop_size = 200
    parents_num = 20
    mutation_rate = 0.2
    max_gen = 10000

    nn = NN(pop_size, parents_num, mutation_rate)

    for gen in range(max_gen):
        game(nn, pop_size, gen)
        nn.optimize()
    nn.save_best()


main()
