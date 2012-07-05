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
npcs[0].name = 'John Doe'

up = False
down = False
left = False
right = False
no_key_yet = True
gameW = 640
gameH = 480
dialogues = []
font = pygame.font.Font(None, 20)
selected_phrase = 0
max_phrases = 0
confirm_phrase = False

while True:
	
	if no_key_yet:
		screen.blit(font.render('Press any key to continue', True, (255, 255, 255)), (50, 50))
		screen.blit(font.render('Controls:', True, (255, 255, 255)), (50, 80)) 
		screen.blit(font.render('- Arrow keys to move', True, (255, 255, 255)), (50, 110))
		screen.blit(font.render('- Space or enter to interact', True, (255, 255, 255)), (50, 130))
		
	else:

		screen.fill((0, 0, 0))

		if hero.moving:
			dx = 0
			dy = 0
			if hero.dir == 'n':
				dy = -2
			if hero.dir == 's':
				dy = 2
			if hero.dir == 'e':
				dx = 2
			if hero.dir == 'w':
				dx = -2
				
			hero.hittest(dx = dx, dy = dy, npcs = npcs)
				
		hero.draw_char(screen, gameW = gameW, gameH = gameH)
		for npc in npcs:
			npc.draw_char(screen, gameW = gameW, gameH = gameH)
			
		for dialogue in dialogues:
			
			if dialogue['phrase'] != '' and confirm_phrase:
				confirm_phrase = False
				
				if selected_phrase == 1:
					interaction = dialogue['speaker'].listen(speaker = hero, phrase = 'Hello.')
				if selected_phrase == 2:
					interaction = dialogue['speaker'].listen(speaker = hero, phrase = 'Jello.')
				
				dialogues.remove(dialogue)	
					
				if interaction[0]:
					if interaction[1] == 1:
						selected_phrase = 1
						dialogues.append({'speaker': interaction[2], 'phrase': interaction[3]})
				
				

			if dialogue['phrase'] == '':
				dialogues.remove(dialogue)
			else:
				
				pygame.draw.rect(screen, (255, 255, 255), (10, (gameH / 3 * 2 + 10), (gameW - 20), (gameH / 3 - 20)), 2)
				screen.blit(font.render(dialogue['phrase'], True, (255, 255, 255)), (15, (gameH / 3 * 2 + 15)))
				
				if dialogue['phrase'] == 'Hi there!' and dialogue['speaker'].name == 'John Doe':
					max_phrases = 2
					screen.blit(font.render('Hello.', True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 15)))
					screen.blit(font.render('Jello.', True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 35)))
					if selected_phrase == 1:
						pygame.draw.rect(screen, (255, 255, 0), (10, 410, (gameW - 20), 25), 2)
					if selected_phrase == 2:
						pygame.draw.rect(screen, (255, 255, 0), (10, 430, (gameW - 20), 25), 2)
		
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
				if event.key == K_KP8 and hero.talking and selected_phrase > 1:
					selected_phrase -= 1
				if event.key == K_KP2 and hero.talking and selected_phrase < max_phrases:
					selected_phrase += 1
				if event.key == K_RETURN or event.key == K_SPACE or event.key == K_KP_ENTER:
					if hero.talking:
						confirm_phrase = True
					else:
						interaction = hero.interact(npcs = npcs)
						if interaction[0]:
							if interaction[1] == 1:
								selected_phrase = 1
								dialogues.append({'speaker': interaction[2], 'phrase': interaction[3]})
						
			no_key_yet = False
		elif event.type == KEYUP:
			if (event.key == K_UP and hero.dir == 'n') or (event.key == K_DOWN and hero.dir == 's') or (event.key == K_RIGHT and hero.dir == 'e') or (event.key == K_LEFT and hero.dir == 'w'):
				hero.moving = False
	
	time.sleep((1.0 / 50))
