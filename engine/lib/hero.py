import pygame
from pygame.locals import *

class hero:
	x = 0
	y = 0
	dir = 's'
	moving = False
	images = {}
	images['main'] = {}
	for val in ['s', 'n', 'e', 'w']:
		images['main'][val] = {}
		images['main'][val]['s'] = []
		images['main'][val]['m'] = []
	
	def __init__(self, sheet = 'main.png', prefix = '../'):
		self.load_sheet(sheet, prefix)
		
	def load_sheet(self, sheet, prefix = '../'):
		sheet_surface = pygame.image.load('../../data/chars/hero/'+sheet)
		sheet_surface.convert_alpha()
		
		#pygame.Rect((left, top), (width, height)): return Rect
		self.images['main']['s']['s'].append(sheet_surface.subsurface(Rect(((14 * 0), 0), (14, 21)) ))
		self.images['main']['s']['m'].append(sheet_surface.subsurface(Rect(((14 * 1), 0), (14, 21)) ))
		self.images['main']['s']['m'].append(sheet_surface.subsurface(Rect(((14 * 2), 0), (14, 21)) ))
		
		self.images['main']['n']['s'].append(sheet_surface.subsurface(Rect(((14 * 3), 0), (14, 21)) ))
		self.images['main']['n']['m'].append(sheet_surface.subsurface(Rect(((14 * 4), 0), (14, 21)) ))
		self.images['main']['n']['m'].append(sheet_surface.subsurface(Rect(((14 * 5), 0), (14, 21)) ))
		
		self.images['main']['e']['s'].append(sheet_surface.subsurface(Rect(((14 * 6), 0), (14, 21)) ))
		self.images['main']['e']['m'].append(sheet_surface.subsurface(Rect(((14 * 7), 0), (14, 21)) ))
		self.images['main']['e']['m'].append(sheet_surface.subsurface(Rect(((14 * 8), 0), (14, 21)) ))
		
		self.images['main']['w']['s'].append(sheet_surface.subsurface(Rect(((14 * 9), 0), (14, 21)) ))
		self.images['main']['w']['m'].append(sheet_surface.subsurface(Rect(((14 * 10), 0), (14, 21)) ))
		self.images['main']['w']['m'].append(sheet_surface.subsurface(Rect(((14 * 11), 0), (14, 21)) ))

	def hittest(self, dx, dy, **objects):
		if not options.get('map'):
			map = false
		else:
			map = options.get('map')
			
		
