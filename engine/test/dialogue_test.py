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
pygame.display.set_caption('Dialogue testing')
screen = pygame.display.get_surface()

hero = char(os.path.join('hero', 'main', 'main'), os.path.join('..', '..', ''))

npcs = []
npcs.append(char(os.path.join('npc', 'test_npc'), os.path.join('..', '..', '')))
npcs[0].x = 30
npcs[0].y = 0
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
dialogue_action = ''

while True:

	if no_key_yet:
		screen.blit(font.render('Press any key to continue', True, (255, 255, 255)), (50, 50))
		screen.blit(font.render('Controls:', True, (255, 255, 255)), (50, 80))
		screen.blit(font.render('- Arrow keys to move', True, (255, 255, 255)), (50, 110))
		screen.blit(font.render('- Space or enter to interact', True, (255, 255, 255)), (50, 130))
		screen.blit(font.render('- numpad 8 and 2 to select dialogue option', True, (255, 255, 255)), (50, 150))

	else:

		screen.fill((0, 0, 0))

		#screen.blit(font.render('Hero.x: '+str(hero.x)+', Hero.y: '+str(hero.y), True, (255, 255, 255)), (15, 15))
		#screen.blit(font.render('Npc.x: '+str(npcs[0].x)+', Npc.y: '+str(npcs[0].y), True, (255, 255, 255)), (15, 30))
		#screen.blit(font.render('Distance: '+str(pow( pow((hero.x-npcs[0].x), 2) + pow((hero.y-npcs[0].y), 2), 0.5) ), True, (255, 255, 255)), (15, 45))

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

			hero.hittest(dx=dx, dy=dy, npcs=npcs)

		hero.draw_char(screen, gameW=gameW, gameH=gameH)
		for npc in npcs:
			npc.draw_char(screen, gameW=gameW, gameH=gameH)

		for dialogue in dialogues:

			dialogue_tree = dialogue['speaker'].dialogue[''][dialogue['stage']]

			if 'min_option' not in dialogue or dialogue['min_option'] == -1:
				dialogue['min_option'] = dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][2]

			if 'option_count' not in dialogue or dialogue['option_count'] == -1:
				dialogue['option_count'] = len(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1])

			if dialogue['phrase'] != [] and dialogue_action != '':

				if dialogue_action == 'cancel' or (dialogue_action == 'confirm' and dialogue['option_count'] == 0):
					dialogue_action = 'remove'
				elif dialogue_action == 'confirm':

					try:
						dialogue['phrase'][0] += 1
						dialogue['phrase'][1] = dialogue['selected']
						dialogue['selected'] = dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][2]
						dialogue['min_option'] = dialogue['selected']
						dialogue['option_count'] = len(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1])
					except IndexError:
						dialogue_action = 'remove'

				elif dialogue_action == 'up' and dialogue['selected'] > dialogue['min_option']:
					dialogue['selected'] -= 1
				elif dialogue_action == 'down' and dialogue['selected'] < (dialogue['option_count'] + dialogue['min_option'] - 1):
					dialogue['selected'] += 1

				if dialogue_action != 'remove':
					dialogue_action = ''

			if dialogue['phrase'] == []:
				dialogues.remove(dialogue)
			elif pow(pow((hero.x - dialogue['speaker'].x), 2) + pow((hero.y - dialogue['speaker'].y), 2), 0.5) > 30 or dialogue_action == 'remove':
				dialogue['speaker'].toggle_dialogue(speaker=hero)
				dialogues.remove(dialogue)
				dialogue_action = ''
			else:

				if dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][3]:
					# Next dialogue will be another one, update stage
					dialogue['speaker'].dialogue_stages[''] = dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][3]

				pygame.draw.rect(screen, (255, 255, 255), (10, (gameH / 3 * 2 + 10), (gameW - 20), (gameH / 3 - 20)), 2)
				pygame.draw.rect(screen, (255, 255, 255), (10, (gameH / 3 * 2 - 20), 80, 31), 2)
				screen.blit(font.render(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][0], True, (255, 255, 255)), (15, (gameH / 3 * 2 + 15)))
				screen.blit(font.render(dialogue['speaker'].name, True, (255, 255, 255)), (15, (gameH / 3 * 2 - 15)))

				if (dialogue['option_count'] > 0):

					if dialogue['option_count'] <= 3 or (dialogue['selected'] - dialogue['min_option']) <= 1:
						pygame.draw.rect(screen, (255, 255, 0), (10, (405 + ((dialogue['selected'] - dialogue['min_option']) * 20)), (gameW - 20), 25), 2)
						for index, answer in enumerate(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1]):
							screen.blit(font.render(answer, True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 10 + (index * 20))))
							if index == 2:
								break
					else:

						if (dialogue['selected'] + 1) == dialogue['option_count']:
							pygame.draw.rect(screen, (255, 255, 0), (10, 445, (gameW - 20), 25), 2)
							screen.blit(font.render(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1][(dialogue['selected'] - 2)], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 10)))
							screen.blit(font.render(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1][(dialogue['selected'] - 1)], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 30)))
							screen.blit(font.render(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1][dialogue['selected']], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 50)))
						else:
							pygame.draw.rect(screen, (255, 255, 0), (10, 425, (gameW - 20), 25), 2)
							screen.blit(font.render(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1][(dialogue['selected'] - 1)], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 10)))
							screen.blit(font.render(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1][dialogue['selected']], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 30)))
							screen.blit(font.render(dialogue_tree[dialogue['phrase'][0]][dialogue['phrase'][1]][1][(dialogue['selected'] + 1)], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 50)))

		pygame.display.flip()

	for event in pygame.event.get():
		#print(event)
		if event.type == pygame.QUIT:
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			if not no_key_yet:
				if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
					hero.moving = True
				if event.key == pygame.K_UP:  # up
					hero.dir = 'n'
				if event.key == pygame.K_DOWN:  # down
					hero.dir = 's'
				if event.key == pygame.K_RIGHT:  # right
					hero.dir = 'e'
				if event.key == pygame.K_LEFT:  # left
					hero.dir = 'w'
				if event.key == pygame.K_KP8 and hero.talking:
					dialogue_action = 'up'
				if event.key == pygame.K_KP2 and hero.talking:
					dialogue_action = 'down'
				if event.key == pygame.K_DELETE and hero.talking:
					dialogue_action = 'cancel'
				if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
					if hero.talking:
						dialogue_action = 'confirm'
					else:
						interaction = hero.interact(npcs=npcs)
						if interaction[0]:
							if interaction[1] == 1:
								dialogues.append({
									'speaker': interaction[2],
									'phrase': interaction[3],
									'selected': 0,
									'stage': interaction[2].dialogue_stages.get('', 1)
								})

			no_key_yet = False
		elif event.type == pygame.KEYUP:
			if (event.key == pygame.K_UP and hero.dir == 'n') or (event.key == pygame.K_DOWN and hero.dir == 's') or (event.key == pygame.K_RIGHT and hero.dir == 'e') or (event.key == pygame.K_LEFT and hero.dir == 'w'):
				hero.moving = False

	time.sleep((1.0 / 50))
