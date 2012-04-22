import pygame, sys, os, time
sys.path.append('../lib/')
from pygame.locals import *
from char import *

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Hero testing')
screen = pygame.display.get_surface()

hero = char('hero/main/main', '../../')

up = False
down = False
left = False
right = False
no_key_yet = True
gameW = 640
gameH = 480
counter = 0
frame = 0

while True:
	
	if no_key_yet:
		font = pygame.font.Font(None, 20)
		text = font.render('Press any key to continue', True, (255, 255, 255))
		screen.blit(text, (50, 50))
		
	else:

		screen.fill((0, 0, 0))
		counter += 1
		if (counter % 20) == 0:
			if frame == 0:
				frame = 1
			else:
				frame = 0
		
		if hero.moving:
			if hero.dir == 'n':
				hero.y -= 2
			if hero.dir == 's':
				hero.y += 2
			if hero.dir == 'e':
				hero.x += 2
			if hero.dir == 'w':
				hero.x -= 2
				
			screen.blit(hero.images[hero.frames['main'][hero.dir]['m'][frame]], ((hero.x + (gameW / 2)), (hero.y + (gameH / 2))))
		else:
			counter = 0
			screen.blit(hero.images[hero.frames['main'][hero.dir]['s'][0]], ((hero.x + (gameW / 2)), (hero.y + (gameH / 2))))
			
		pygame.display.flip()
		
	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
		elif event.type == KEYDOWN:
			no_key_yet = False
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
