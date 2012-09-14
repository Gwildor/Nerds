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

item = item('potion', os.path.join('..', '..', ''))
item.x = 25
item.y = 20

up = False
down = False
left = False
right = False
no_key_yet = True
gameW = 640
gameH = 480
font = pygame.font.Font(None, 20)
keys = []
notifications = []

#notifications.append({'type': 'text', 'text': 'Test!'}) # test notification

while True:
	
	if no_key_yet:
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
		
		if not item.owner:
			screen.blit(item.img, (item.x + gameW / 2, item.y + gameH / 2))
			
		for index, msg in enumerate(notifications):
			if 'time_elapsed' in msg:
				if ('remove_after' in msg and msg['time_elapsed'] > msg['remove_after']) or ('remove_after' not in msg and msg['time_elapsed'] > 5.0):
					notifications.remove(msg)
					continue
				else:
					msg['time_elapsed'] += 1.0 / 50
			else:
				msg['time_elapsed'] = 1.0 / 50


			
			if msg['type'] == 'text':
				screen.blit(font.render(msg['text'], True, (255, 255, 255)), (5, 5 + index * 15))
			
			if msg['type'] == 'pick_up_item':
				screen.blit(font.render('You picked up a '+msg['objects'][0].summary+'! Value: '+str(msg['objects'][0].value), True, (255, 255, 255)), (5, 5 + index * 15))

				# hero has walked away
				if pow( pow((hero.x - msg['objects'][0].x), 2) + pow((hero.y - msg['objects'][0].y), 2), 0.5) > 60:
					notifications.remove(msg)
					continue

			#print msg['time_elapsed']

		pygame.display.flip()
		
	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
		elif event.type == KEYDOWN:
			no_key_yet = False
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.append(event.key)
			if event.key == K_RETURN or event.key == K_SPACE or event.key == K_KP_ENTER:
				interaction = hero.interact(items = [item])
				if interaction[0]:
					if interaction[1] == 2 and interaction[2].msg:
						notifications.append({'type': 'pick_up_item', 'remove_after': 10.0, 'objects': [interaction[2]]})
			
		elif event.type == KEYUP:
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.remove(event.key)
	
	time.sleep((1.0 / 50))
