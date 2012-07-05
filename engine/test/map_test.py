import pygame, sys, os, time
sys.path.append(os.path.join('..', 'lib', ''))
from pygame.locals import *
from map import *
	
pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Map view')
screen = pygame.display.get_surface()

map = map('main', os.path.join('..', '..', ''))

x = 0
y = 0
speed = 5
multiplier = 1
up = False
down = False
left = False
right = False
no_key_yet = True

while True:
	
	if no_key_yet:
		font = pygame.font.Font(None, 20)
		screen.blit(font.render('Press any key to continue', True, (255, 255, 255)), (50, 50))
		screen.blit(font.render('Controls:', True, (255, 255, 255)), (50, 80))
		screen.blit(font.render('- Arrow keys to move', True, (255, 255, 255)), (50, 110))
		screen.blit(font.render('- Plus and minus to increase move speed', True, (255, 255, 255)), (50, 130))
		screen.blit(font.render('- Page up and down to jump North and South', True, (255, 255, 255)), (50, 150))
		screen.blit(font.render('- F5 to reload the map from map file', True, (255, 255, 255)), (50, 170))
		
	else:
		screen.fill((0, 0, 0))
		map.draw_map(screen, x, y)
		pygame.display.flip()

	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
		elif event.type == KEYDOWN:
			no_key_yet = False
			if event.key == 273: # up
				up = True
			if event.key == 274: # down
				down = True
			if event.key == 275: # right
				right = True
			if event.key == 276: # left
				left = True
			if event.key == 270 or event.key == 61: # plus sign
				multiplier += 1
			if (event.key == 269 or event.key == 45) and multiplier > 1: # minus sign
				multiplier -= 1
			if event.key == 280: # page up
				y -= 400
			if event.key == 281: # page down
				y += 400
			if event.key == 286: # F5
				map.load_map('main', '../../')
		elif event.type == KEYUP:
			if event.key == 273: # up
				up = False
			if event.key == 274: # down
				down = False
			if event.key == 275: # right
				right = False
			if event.key == 276: # left
				left = False

	if up:
		y -= speed * multiplier
	if down:
		y += speed * multiplier
	if right:
		x += speed * multiplier
	if left:
		x -= speed * multiplier
	
	time.sleep((1.0 / 50))
