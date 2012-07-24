debug = False

import pygame, sys, os, time
sys.path.append(os.path.join('engine', 'lib', ''))
sys.path.append(os.path.join('lib', ''))
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
	
objects = {'npcs': [], 'map': map(), 'hero': hero}

if debug:
	objects['map'].debug = True

#objects['npcs'].append(char(os.path.join('npc', 'test_npc')))

#for npc in objects['npcs']:
#	npc.map = objects['map'].file
hero.map = objects['map'].file

up = False
down = False
left = False
right = False
gameW = 640
gameH = 480
font = pygame.font.Font(None, 20)
dx = 0
dy = 0
keys = []

while True:

	screen.fill((0, 0, 0))

	hero.moving = False
	dx = 0
	dy = 0
	for key in keys:
		if key == 273 or key == 274 or key == 275 or key == 276:
			hero.moving = True
		if key == 273: # up
			hero.dir = 'n'
			dy = -4
			dx = 0
		if key == 274: # down
			hero.dir = 's'
			dy = 4
			dx = 0
		if key == 275: # right
			hero.dir = 'e'
			dx = 4
			dy = 0
		if key == 276: # left
			hero.dir = 'w'
			dx = -4
			dy = 0
			
	hero.hittest(dx = dx, dy = dy, objects = objects)

	objects['map'].draw_map(screen, hero.x, hero.y)
	if len(objects['map'].npc_files) > 0:
		for file in objects['map'].npc_files:
			objects['npcs'].append(char(file))
			objects['npcs'][-1].map = objects['map'].file
		objects['map'].npc_files = []
	
	hero.draw_char(screen, x = (gameW / 2), y = (gameH / 2))
	
	for npc in objects['npcs']:
		if npc.map == objects['map'].file:
			npc.move(objects = objects)
			npc.draw_char(screen, x = ((npc.x - hero.x) + (gameW / 2)), y = ((npc.y - hero.y) + (gameH / 2)))
	
	if debug:
		screen.blit(font.render('Hero.x: '+str(hero.x)+', Hero.y: '+str(hero.y), True, (255, 255, 255)), (15, 15))
	
	pygame.display.flip()
		
	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
		elif event.type == KEYDOWN:
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.append(event.key)
			
		elif event.type == KEYUP:
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.remove(event.key)
	
	time.sleep((1.0 / 50))
