import pygame, sys, os, time
sys.path.append(os.path.join('..', 'lib', ''))
from pygame.locals import *
from char import *
from item import *

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Item testing')
screen = pygame.display.get_surface()

hero = char(os.path.join('hero', 'main', 'main'), os.path.join('..', '..', ''))
item = item(False)
item.x = 25
item.y = 20
item.summary = 'Potion (+50hp)'
item.msg = True
item.src = 'potion.png'
item.img = pygame.image.load(os.path.join('..', '..', 'data', 'items', '')+item.src)
item.img.convert_alpha()
item.h = item.img.get_height()
item.w = item.img.get_width()


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
		dx = 0
		dy = 0
		for key in keys:
			if key == 273 or key == 274 or key == 275 or key == 276:
				hero.moving = True
			if key == 273: # up
				hero.dir = 'n'
				dy = -2
				dx = 0
			if key == 274: # down
				hero.dir = 's'
				dy = 2
				dx = 0
			if key == 275: # right
				hero.dir = 'e'
				dx = 2
				dy = 0
			if key == 276: # left
				hero.dir = 'w'
				dx = -2
				dy = 0
				
		hero.hittest(dx = dx, dy = dy, items = [item])
		hero.draw_char(screen, gameW = gameW, gameH = gameH)
		
		screen.blit(item.img, (item.x + gameW / 2, item.y + gameH / 2))
		
		pygame.display.flip()
		
	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
		elif event.type == KEYDOWN:
			no_key_yet = False
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.append(event.key)
			
		elif event.type == KEYUP:
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.remove(event.key)
	
	time.sleep((1.0 / 50))
