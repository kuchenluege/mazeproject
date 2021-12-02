import numpy as np
import random
import timeit
#import os
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
#import pygame as pg

def rand_unv_neighbor(maze, loc):
	up = (0, -1)
	down = (0, 1)
	left = (-1, 0)
	right = (1, 0)
	neighbor = ()
	for direction in random.sample([up, down, left, right], 4):
		neighbor = tuple(map(sum, zip(loc, direction)))
		for ind, length in zip(neighbor, maze.shape):
			if ind < 0 or ind >= length:
				neighbor = ()
				break
		if not(neighbor):
			continue
		val = maze[neighbor]
		if val != 0:
			neighbor = ()
			continue
		return neighbor
	return neighbor

def seq_solver(maze, start, finish):
	curr_loc = start
	stack = []
	maze_copy = maze.copy()

	while curr_loc != finish:
		maze_copy[curr_loc] = 2
		neighbor = rand_unv_neighbor(maze_copy, curr_loc)
		if neighbor:
			stack.append(curr_loc)
			curr_loc = neighbor
		else:
			maze_copy[curr_loc] = 3
			curr_loc = stack.pop()
	maze_copy[curr_loc] = 2	
	return maze_copy

for size in [10, 30, 50, 100, 300, 500]:
	maze = np.loadtxt('maze_%dx%d.txt' % (size, size))
	start = (0, 1)
	finish = (maze.shape[0] - 1, maze.shape[1] - 2)

	print('%dx%d Maze' % (size, size))
	num = 10
	print('Avg. sequential execution time: ', timeit.timeit(globals=globals(), stmt='seq_solver(maze, start, finish)', number=num) / num)
	print()

'''
pg.init()
screen = pg.display.set_mode((400, 400))
clock = pg.time.Clock()

colors = np.array([[255, 255, 255], [0, 0, 0], [0, 255, 0], [255, 0, 0]])

surface = pg.surfarray.make_surface(colors[solution])
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
'''