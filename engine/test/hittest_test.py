import pygame, sys, os, time
sys.path.append(os.path.join('..', 'lib', ''))
from pygame.locals import *
from char import *
from map import *

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Hittest testing')
screen = pygame.display.get_surface()

hero = char(False)
map = map(False)

body = pygame.Surface((32, 32))
body.fill((255, 0, 0))

hero.frames[''] = {'n': {'s': ['rect'], 'm': ['rect']}, 'w': {'s': ['rect'], 'm': ['rect']}, 'e': {'s': ['rect'], 'm': ['rect']}, 's': {'s': ['rect'], 'm': ['rect']}}
hero.state = 'm'

#print(hero.frames)
hero.images['rect'] = body

rect = pygame.Surface((32, 32))
rect.fill((255, 255, 255))

map.images['rect'] = rect

map.tiles.append({'src': 'rect', 'pos_x': -50, 'pos_y': -50, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': 50, 'pos_y': 50, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': 50, 'pos_y': 82, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': 18, 'pos_y': 82, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': -14, 'pos_y': 114, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': -46, 'pos_y': 82, 'width': 32, 'height': 32, 'walkable': False})

up = False
down = False
left = False
right = False
gameW = 640
gameH = 480

while True:

	screen.fill((0, 0, 0))
	map.draw_map(screen, 0, 0)
	
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

	screen.blit(hero.images[hero.frames[hero.file][hero.dir]['s'][0]], ((hero.x + (gameW / 2)), (hero.y + (gameH / 2))))
	
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
