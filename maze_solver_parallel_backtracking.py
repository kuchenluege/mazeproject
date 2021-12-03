import numpy as np
import random
import multiprocessing as mp
import timeit
import queue
import os
'''
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
'''

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

def seq_solver(maze, start, finish, q):
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
	q.put('done')
	return maze_copy


def pool_manager(maze, start, finish, size):
	pool = mp.Pool(size)
	manager = mp.Manager()
	q = manager.Queue()
	results = [pool.apply_async(seq_solver, args=(maze, start, finish, q)) for _ in range(size)]

	q.get()
	solution = np.zeros(0)
	while not(solution.any()):
		for res in results:
			if res.ready():
				solution = res.get()
				pool.terminate()
				pool.join()
				break

	return solution

if __name__ == '__main__':
	f = open("results.txt", "x")
	for pool_size in [1, 3, 6, 12]:
		f.write('Pool Size: %d\n' % pool_size)
		print('Pool Size: %d' % pool_size)
		for size in [10, 30, 50, 100, 200, 300, 400, 500]:
			maze = np.loadtxt('maze_%dx%d.txt' % (size, size))
			start = (0, 1)
			finish = (maze.shape[0] - 1, maze.shape[1] - 2)
			f.write('%dx%d Maze\n' % (size, size))
			print('%dx%d Maze' % (size, size))
			num = 50
			res_time = timeit.timeit(stmt='solution = pool_manager(maze, start, finish, pool_size)', number=num, globals=globals()) / num
			f.write('Avg. parallel (w/ backtracking) execution time: %f\n' % res_time)
			f.write('\n')
			print('Avg. parallel (w/ backtracking) execution time: %f' % res_time)
			print('\n')

			'''
			solution = pool_manager(maze, start, finish, pool_size).astype(int)

			pg.init()
			screen = pg.display.set_mode((800, 800))
			clock = pg.time.Clock()

			colors = np.array([[255, 255, 255], [0, 0, 0], [0, 255, 0], [255, 0, 0]])
			surface = pg.surfarray.make_surface(colors[solution])

			running = True
			while running:
				for event in pg.event.get():if event.type == pg.QUIT:
					running = False

				screen.fill((30, 30, 30))
				screen.blit(surface, (0, 0))
				pg.display.flip()
				clock.tick(60)
			'''
