import pygame, sys, os
sys.path.append('../lib/')
from pygame.locals import *
from map import *

def draw_map(map_obj, x, y, gameW = 640, gameH = 480):
	nw = {'x': (x - (gameW / 2)), 'y': (y - (gameH / 2))}
	sw = {'x': (x - (gameW / 2)), 'y': (y + (gameH / 2))}
	se = {'x': (x + (gameW / 2)), 'y': (y + (gameH / 2))}
	ne = {'x': (x + (gameW / 2)), 'y': (y - (gameH / 2))}

	screen.fill(000)
	for tile in map_obj.tiles: # loop our tiles
		if map_obj.tile_within_square(tile, nw, se):
			#print(tile)
			if tile['src'] not in images:
				images[tile['src']] = pygame.image.load('../../data/tiles/'+tile['src'])
			screen.blit(images[tile['src']], (tile['pos_x'] + x + gameW / 2, tile['pos_y'] + y + gameH / 2))
	pygame.display.flip()

map = map('main', '../../')

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Map view') 
screen = pygame.display.get_surface()  

images = {}

x = 0

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit(0)
		else:
			print(event)
			draw_map(map, x, 0)
			x += 1
