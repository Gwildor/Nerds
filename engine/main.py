debug = True

import pygame, sys, os, time
sys.path.append('engine/lib/')
sys.path.append('lib/')
from pygame.locals import *
from char import *
from map import *

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Nerds\' main screen')
screen = pygame.display.get_surface()

hero = char()
if debug:
	hero.debug = True
map = map()
if debug:
	map.debug = True

up = False
down = False
left = False
right = False
gameW = 640
gameH = 480
counter = 0
frame = 0

while True:

	screen.fill((0, 0, 0))
	
	counter += 1
	if (counter % 15) == 0:
		if frame == 0:
			frame = 1
		else:
			frame = 0
	
	if hero.moving:
		dx = 0
		dy = 0
		if hero.dir == 'n':
			dy = -4
		if hero.dir == 's':
			dy = 4
		if hero.dir == 'e':
			dx = 4
		if hero.dir == 'w':
			dx = -4
	
		hero.hittest(dx = dx, dy = dy, map = map)
	
	map.draw_map(screen, hero.x, hero.y)

	if hero.moving:
		screen.blit(hero.images[hero.frames[hero.state][hero.dir]['m'][frame]], ((gameW / 2), ((gameH / 2))))
	else:
		counter = 0
		screen.blit(hero.images[hero.frames[hero.state][hero.dir]['s'][0]], ((gameW / 2), ((gameH / 2))))
	
	pygame.display.flip()
		
	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
		elif event.type == KEYDOWN:
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				hero.moving = True
			if event.key == 273: # up
				hero.dir = 'n'
			if event.key == 274: # down
				hero.dir = 's'
			if event.key == 275: # right
				hero.dir = 'e'
			if event.key == 276: # left
				hero.dir = 'w'
		elif event.type == KEYUP:
			if (event.key == 273 and hero.dir == 'n') or (event.key == 274 and hero.dir == 's') or (event.key == 275 and hero.dir == 'e') or (event.key == 276 and hero.dir == 'w'):
				hero.moving = False
	
	time.sleep((1.0 / 50))
