import pygame, os, re
from pygame.locals import *

class item:
	x = 0
	y = 0
	w = 0
	h = 0
	map = ''
	file = ''
	debug = False
	owner = False
	value = 0
	power = 0
	burden = 0
	src = False
	img = False
	msg = False
	summary = ''
	instant = False

	def __init__(self, file, prefix = os.path.join('..', '')):
		if file:
			self.load_file(file, prefix)
			
	def load_file(self, file, prefix = os.path.join('..', '')):
		pass
