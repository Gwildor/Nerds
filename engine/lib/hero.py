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
		if sheet:
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
		if not objects.get('map'):
			map = False
		else:
			map = objects.get('map')
			
		hero.x += dx
		hero.y += dy
		
		if dx < 0:
			x_negative = True
			dx *= -1
		else:
			x_negative = False
			
		if dy < 0:
			y_negative = True
			dy *= -1
		else:
			y_negative = False
		
		
		ax = 0
		ay = 0			
		while (ax - 1) < dx:
			#print('x: '+str(ax))
			
			while (ay - 1) < dy:
				#print('y: '+str(ay))
				
				if x_negative:
					pos_x = hero.x - ax
				else:
					pos_x = hero.x + ax
					
				if y_negative:
					pos_y = hero.y - ay
				else:
					pos_y = hero.y + ax
					
				if map:
					
					for tile in map.tiles:
						if map.tile_within_square(tile, {'x': pos_x, 'y': pos_y}, {'x': (pos_x + self.images['main'][self.dir]['m'][0].get_width()), 'y': (pos_y + self.images['main'][self.dir]['m'][0].get_height())}):
							hero.x = pos_x - 1
							hero.y = pos_y - 1
							return 0
							
				ay += 1
				
			ax += 1
				
				
		#print('...')
