import pygame, sys, os, time
sys.path.append(os.path.join('..', 'lib', ''))
from pygame.locals import *
from char import *

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Dialogue testing')
screen = pygame.display.get_surface()

hero = char(os.path.join('hero', 'main', 'main'), os.path.join('..', '..', ''))

npcs = []
npcs.append(char(os.path.join('npc', 'test_npc'), os.path.join('..', '..', '')))
npcs[0].x = 30

up = False
down = False
left = False
right = False
no_key_yet = True
gameW = 640
gameH = 480

while True:
	
	if no_key_yet:
		font = pygame.font.Font(None, 20)
		text = font.render('Press any key to continue', True, (255, 255, 255))
		screen.blit(text, (50, 50))
		
	else:

		screen.fill((0, 0, 0))

		if hero.moving:
			if hero.dir == 'n':
				hero.y -= 2
			if hero.dir == 's':
				hero.y += 2
			if hero.dir == 'e':
				hero.x += 2
			if hero.dir == 'w':
				hero.x -= 2
				
		hero.draw_char(screen, gameW = gameW, gameH = gameH)
		for npc in npcs:
			npc.draw_char(screen, gameW = gameW, gameH = gameH)
		
		pygame.display.flip()
		
	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
		elif event.type == KEYDOWN:
			if not no_key_yet:
				if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
					hero.moving = True
				if event.key == K_UP: # up
					hero.dir = 'n'
				if event.key == K_DOWN: # down
					hero.dir = 's'
				if event.key == K_RIGHT: # right
					hero.dir = 'e'
				if event.key == K_LEFT: # left
					hero.dir = 'w'
				if event.key == K_RETURN or event.key == K_SPACE:
					hero.interact(npcs = npcs)
			no_key_yet = False
		elif event.type == KEYUP:
			if (event.key == K_UP and hero.dir == 'n') or (event.key == K_DOWN and hero.dir == 's') or (event.key == K_RIGHT and hero.dir == 'e') or (event.key == K_LEFT and hero.dir == 'w'):
				hero.moving = False
	
	time.sleep((1.0 / 50))
