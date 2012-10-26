import os
import pygame
import sys
import time

# Python doesn't seem to allow clean imports
# from sibling folders.
sys.path.append('..')
from lib.char import char


pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Hero testing')
screen = pygame.display.get_surface()

hero = char(os.path.join('hero', 'main', 'main'), os.path.join('..', '..', ''))
#hero = char(os.path.join('npc', 'test_npc'), os.path.join('..', '..', ''))

up = False
down = False
left = False
right = False
no_key_yet = True
gameW = 640
gameH = 480
keys = []

while True:

	if no_key_yet:
		font = pygame.font.Font(None, 20)
		screen.blit(font.render('Press any key to continue', True, (255, 255, 255)), (50, 50))

	else:

		screen.fill((0, 0, 0))

		hero.moving = False
		dx = hero.x
		dy = hero.y
		for key in keys:
			if key == 273 or key == 274 or key == 275 or key == 276:
				hero.moving = True
			if key == 273:  # up
				hero.dir = 'n'
				hero.y = dy - 2
				hero.x = dx
			if key == 274:  # down
				hero.dir = 's'
				hero.y = dy + 2
				hero.x = dx
			if key == 275:  # right
				hero.dir = 'e'
				hero.x = dx + 2
				hero.y = dy
			if key == 276:  # left
				hero.dir = 'w'
				hero.x = dx - 2
				hero.y = dy

		hero.draw_char(screen, gameW=gameW, gameH=gameH)

		pygame.display.flip()

	for event in pygame.event.get():
		#print(event)
		if event.type == pygame.QUIT:
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			no_key_yet = False
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.append(event.key)

		elif event.type == pygame.KEYUP:
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.remove(event.key)

	time.sleep((1.0 / 50))
