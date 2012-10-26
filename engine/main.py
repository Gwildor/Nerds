import pygame
import sys
import time

# engine libs import
from lib.char import char
from lib.map import map
from lib.item import item


pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Nerds\' main screen')
screen = pygame.display.get_surface()

debug = False  # switch to True for quick debug visuals

hero = char()
if debug:
	hero.debug = True

objects = {'npcs': [], 'map': map(), 'hero': hero}

if debug:
	objects['map'].debug = True

hero.map = objects['map'].file

gameW = 640
gameH = 480
font = pygame.font.Font(None, 20)
dx = 0
dy = 0
keys = []
dialogues = []
dialogue_action = ''
frames_this_second = 0
fps = 0
fps_last_update = int(time.time())
last_cycle_time = 0.0
sleep_time = 1.0 / 50

while True:
	cycle_start = time.time()

	screen.fill((0, 0, 0))

	hero.moving = False
	dx = 0
	dy = 0
	for key in keys:  # loop through all keys currently pressed
		if key == 273 or key == 274 or key == 275 or key == 276:
			hero.moving = True
		if key == 273:  # up
			hero.dir = 'n'
			dy = -2
			dx = 0
		if key == 274:  # down
			hero.dir = 's'
			dy = 2
			dx = 0
		if key == 275:  # right
			hero.dir = 'e'
			dx = 2
			dy = 0
		if key == 276:  # left
			hero.dir = 'w'
			dx = -2
			dy = 0

	hero.hittest(dx=dx, dy=dy, objects=objects)

	objects['map'].draw_map(screen, hero.x, hero.y)
	if len(objects['map'].npc_files) > 0:  # load .char files from .map file
		for file in objects['map'].npc_files:
			objects['npcs'].append(char(file))
			objects['npcs'][-1].map = objects['map'].file
		objects['map'].npc_files = []

	hero.draw_char(screen, x=(gameW / 2), y=(gameH / 2))

	for npc in objects['npcs']:
		if npc.map == objects['map'].file:
			npc.move(objects=objects)
			npc.draw_char(screen, x=((npc.x - hero.x) + (gameW / 2)), y=((npc.y - hero.y) + (gameH / 2)))

	#
	# Dialogue handling.
	#
	# Later on this will be put in a function in a general game module,
	# so this code is here just temporary for testing purposes.
	#

	for dialogue in dialogues:

		if 'min_option' not in dialogue or dialogue['min_option'] == -1:
			dialogue['min_option'] = dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][2]

		if 'option_count' not in dialogue or dialogue['option_count'] == -1:
			dialogue['option_count'] = len(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1])

		if dialogue['phrase'] != [] and dialogue_action != '':

			if dialogue_action == 'cancel' or (dialogue_action == 'confirm' and dialogue['option_count'] == 0):
				dialogue_action = 'remove'
			elif dialogue_action == 'confirm':

				try:
					dialogue['phrase'][0] += 1
					dialogue['phrase'][1] = dialogue['selected']
					dialogue['selected'] = dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][2]
					dialogue['min_option'] = dialogue['selected']
					dialogue['option_count'] = len(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1])
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

		# calculate distance between hero and npc, and check if it hasn't become to big.
		elif pow(pow((hero.x - dialogue['speaker'].x), 2) + pow((hero.y - dialogue['speaker'].y), 2), 0.5) > 30 or dialogue_action == 'remove':
			dialogue['speaker'].toggle_dialogue(speaker=hero)
			dialogues.remove(dialogue)
			dialogue_action = ''
		else:

			pygame.draw.rect(screen, (255, 255, 255), (10, (gameH / 3 * 2 + 10), (gameW - 20), (gameH / 3 - 20)), 2)
			pygame.draw.rect(screen, (255, 255, 255), (10, (gameH / 3 * 2 - 20), 80, 31), 2)
			screen.blit(font.render(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][0], True, (255, 255, 255)), (15, (gameH / 3 * 2 + 15)))
			screen.blit(font.render(dialogue['speaker'].name, True, (255, 255, 255)), (15, (gameH / 3 * 2 - 15)))

			if (dialogue['option_count'] > 0):

				if dialogue['option_count'] <= 3 or (dialogue['selected'] - dialogue['min_option']) <= 1:
					pygame.draw.rect(screen, (255, 255, 0), (10, (405 + ((dialogue['selected'] - dialogue['min_option']) * 20)), (gameW - 20), 25), 2)
					for index, answer in enumerate(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1]):
						screen.blit(font.render(answer, True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 10 + (index * 20))))
						if index == 2:
							break
				else:

					if (dialogue['selected'] + 1) == dialogue['option_count']:
						pygame.draw.rect(screen, (255, 255, 0), (10, 445, (gameW - 20), 25), 2)
						screen.blit(font.render(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1][(dialogue['selected'] - 2)], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 10)))
						screen.blit(font.render(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1][(dialogue['selected'] - 1)], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 30)))
						screen.blit(font.render(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1][dialogue['selected']], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 50)))
					else:
						pygame.draw.rect(screen, (255, 255, 0), (10, 425, (gameW - 20), 25), 2)
						screen.blit(font.render(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1][(dialogue['selected'] - 1)], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 10)))
						screen.blit(font.render(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1][dialogue['selected']], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 30)))
						screen.blit(font.render(dialogue['speaker'].dialogue[''][dialogue['phrase'][0]][dialogue['phrase'][1]][1][(dialogue['selected'] + 1)], True, (255, 255, 255)), (15, ((gameH / 6 * 5) + 50)))

	#
	# End of dialogues.
	#

	if debug:
		if fps_last_update != int(time.time()):
			fps_last_update = int(time.time())
			fps = frames_this_second
			frames_this_second = 0

		screen.blit(font.render('FPS: ' + str(fps), True, (255, 255, 255)), ((gameW - 60), 15))
		screen.blit(font.render('Last cyle time: ' + str(round(last_cycle_time, 3)), True, (255, 255, 255)), ((gameW - 140), 30))

		screen.blit(font.render('Hero.x: ' + str(hero.x) + ', Hero.y: ' + str(hero.y), True, (255, 255, 255)), (15, 15))

	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.append(event.key)
			if event.key == pygame.K_KP8 and hero.talking:  # numpad 8
				dialogue_action = 'up'
			if event.key == pygame.K_KP2 and hero.talking:  # numpad 2
				dialogue_action = 'down'
			if event.key == pygame.K_DELETE and hero.talking:  # delete
				dialogue_action = 'cancel'
			if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:  # return/space
				if hero.talking:
					dialogue_action = 'confirm'
				else:
					interaction = hero.interact(npcs=objects['npcs'])
					if interaction[0]:  # valid interaction
						if interaction[1] == 1:  # interaction is dialogue with npc
							dialogues.append({'speaker': interaction[2], 'phrase': interaction[3], 'selected': 0})

		elif event.type == pygame.KEYUP:
			if event.key == 273 or event.key == 274 or event.key == 275 or event.key == 276:
				keys.remove(event.key)

	frames_this_second += 1
	cycle_end = time.time()
	last_cycle_time = cycle_end - cycle_start
	if last_cycle_time < sleep_time:
		time.sleep((sleep_time - last_cycle_time))
