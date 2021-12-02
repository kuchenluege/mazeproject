import numpy as np
import multiprocessing as mp
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

def loc_neighbors(maze, shape, loc):
	up = -1
	down = 1
	left = -1 * shape[1]
	right = shape[1]
	neighbors = []
	for direction in [up, down, left, right]:
		neighbor = loc + direction
		if neighbor < 0 or neighbor >= shape[0] * shape[1]:
			continue
		val = maze[neighbor]
		if val != 0:
			continue
		neighbors.append(neighbor)
	return neighbors

def par_solver(maze, shape, q, stack, start, finish):
	curr_loc = start

	while curr_loc != finish:
		maze[curr_loc] = 3
		neighbors = loc_neighbors(maze, shape, curr_loc)
		if neighbors:
			stack.append(curr_loc)
			curr_loc = neighbors[0]
			for neighbor in neighbors[1:]:
				q.put((neighbor, stack.copy()))
		else:
			return
	maze[curr_loc] = 2
	for loc in stack:
		maze[loc] = 2
	q.put(-1)

if __name__ == '__main__':
	maze = np.loadtxt('maze.txt').astype(int)
	start = 1
	finish = maze.size - 2

	solution = mp.Array('i', maze.flatten(), lock=False)
	q = mp.Queue()
	p = mp.Process(target=par_solver, args=(solution, maze.shape, q, [], start, finish))
	p.start()
	running_processes = [p]

	while True:
		msg = q.get()
		if msg == -1:
			for p in running_processes:
				p.terminate()
			break
		else:
			(neighbor, stack) = msg
			p = mp.Process(target=par_solver, args=(solution, maze.shape, q, stack, neighbor, finish))
			p.start()
			running_processes.append(p)

	solution_2d = np.frombuffer(solution, dtype="int32").reshape(maze.shape)

	pg.init()
	screen = pg.display.set_mode((400, 400))
	clock = pg.time.Clock()

	colors = np.array([[255, 255, 255], [0, 0, 0], [0, 255, 0], [255, 0, 0]])

	surface = pg.surfarray.make_surface(colors[solution_2d])
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