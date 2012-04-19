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
		sheet_surface = pygame.image.load('../../data/char/hero/'+sheet)
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

	def hittest(self, **args):
		if not args.get('dx'):
			dx = 0
		else:
			dx = args.get('dx')
			
		if not args.get('dy'):
			dy = 0
		else:
			dy = args.get('dy')
		
		if not args.get('map'):
			map = False
		else:
			map = args.get('map')
		
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
		
		ori_x = hero.x
		ori_y = hero.y
		pos_x = ori_x
		pos_y = ori_y
		
		ax = 0
		while ax <= dx:
			#print('x: '+str(ax))
			
			ay = 0
			while ay <= dy:
				#print('y: '+str(ay))
				#print('x,y: '+str(ax)+','+str(ay)+' - pos_x,y: '+str(pos_x)+','+str(pos_y)+' - ori_x,y: '+str(ori_x)+','+str(ori_y))
				
				hero.x = pos_x
				hero.y = pos_y
				
				if x_negative:
					pos_x = ori_x - ax
				else:
					pos_x = ori_x + ax
					
				if y_negative:
					pos_y = ori_y - ay
				else:
					pos_y = ori_y + ay
					
				if map:
					
					for tile in map.tiles:
						if not tile['walkable']:
							if map.tile_within_square(tile, {'x': pos_x, 'y': pos_y}, {'x': (pos_x + self.images['main'][self.dir]['m'][0].get_width()), 'y': (pos_y + self.images['main'][self.dir]['m'][0].get_height())}, 1):
								return True
							
				ay += 1
				
			ax += 1
			
		#print('...')
		hero.x = pos_x
		hero.y = pos_y
		
		return False
