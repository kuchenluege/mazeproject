import numpy as np
import random
from mazelib.generate import BacktrackingGenerator as bg
import pygame as pg

maze_gen = bg.BacktrackingGenerator(15, 15)
grid = maze_gen.generate()
start = (0, 1)
finish = (grid.shape[0] - 1, grid.shape[1] - 2)

grid[start] = 0
grid[finish] = 0

np.savetxt('maze.txt', grid)


pg.init()
screen = pg.display.set_mode((400, 400))
clock = pg.time.Clock()

colors = np.array([[255, 255, 255], [0, 0, 0]])

surface = pg.surfarray.make_surface(colors[grid])
surface = pg.transform.scale(surface, (200, 200))

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((30, 30, 30))
    screen.blit(surface, (100, 100))
    pg.display.flip()
    clock.tick(60)
