import pygame, sys, os, time
sys.path.append(os.path.join('..', 'lib', ''))
from pygame.locals import *
from char import *
from map import *

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('NPC AI moving testing')
screen = pygame.display.get_surface()

npc = char(os.path.join('npc', 'test_npc'), os.path.join('..', '..', ''))
npc.x = 0
npc.y = 0
npc.dir = 'e'
map = map(False)

rect = pygame.Surface((32, 32))
rect.fill((255, 255, 255))

map.images['rect'] = rect

map.tiles.append({'src': 'rect', 'pos_x': -50, 'pos_y': -50, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': 50, 'pos_y': 50, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': 50, 'pos_y': 82, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': 18, 'pos_y': 82, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': -14, 'pos_y': 114, 'width': 32, 'height': 32, 'walkable': False})
map.tiles.append({'src': 'rect', 'pos_x': -46, 'pos_y': 82, 'width': 32, 'height': 32, 'walkable': False})

gameW = 640
gameH = 480

targetX = 100
targetY = 100

while True:

	screen.fill((0, 0, 0))
	map.draw_map(screen, 0, 0)

	if npc.move_to(x = targetX, y = targetY, objects = {'map': map}):
		if targetX * targetY == 10000: # both -100 or both 100 -> nw or se corner
			targetX *= -1
		else: # sw or ne corner
			targetY *= -1

	npc.draw_char(screen, gameW = gameW, gameH = gameH)

	pygame.display.flip()
		
	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
	
	time.sleep((1.0 / 50))
