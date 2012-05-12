import pygame, sys, os, time
sys.path.append(os.path.join('..', 'lib', ''))
from pygame.locals import *
from char import *
from map import *

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('NPC AI moving testing')
screen = pygame.display.get_surface()

npc = char(os.path.join('npc', 'test_npc'), os.path.join('..', '..', ''))

gameW = 640
gameH = 480

targetX = 100
targetY = 100

while True:

	screen.fill((0, 0, 0))
	
	if npc.move_to(x = targetX, y = targetY):
		if targetX * targetY == 10000: # both -100 or both 100 -> nw or se corner
			targetX *= -1
		else: # sw or ne corner
			targetY *= -1
		
	npc.draw_char(screen, gameW = gameW, gameH = gameH)

	pygame.display.flip()
		
	for event in pygame.event.get():
		#print(event)
		if event.type == QUIT:
			sys.exit(0)
	
	time.sleep((1.0 / 50))
