import pygame, sys, os
from pygame.locals import *

class map:
	tiles = []
	general = {}
	images = {}
	debug = False
	pos_x = 0
	pos_y = 0
	
	def __init__(self, name = 'main', prefix = os.path.join('..', '')):
		#print(name)
		if name:
			self.load_map(name, prefix)

	def load_map(self, name, prefix = os.path.join('..', '')):
		#print(name)
		self.tiles = []
		self.general = {}
		tile_mode = False
		f = open(prefix+os.path.join('data', 'maps', '')+name+'.map', 'r') # open map
		k = 0
		
		for line in f.readlines(): # loop through file
			if '#' in line: # comment found
				parts = line.split('#', 1)
				#print(parts)
				line = parts[0]
			line = line.strip()
			
			if line != '':
				#print(line, sep = '', end = '\n') # echo whole file
				if line[0:1] == '~':
					
					if not tile_mode:
						#print(self.general)
						tile_mode = True
					else:
						#print(str(k), self.tiles[k])
						
						if self.tiles[k]['src'] not in self.images:
							self.images[self.tiles[k]['src']] = pygame.image.load(prefix+os.path.join('data', 'tiles', '')+self.tiles[k]['src'])
							
						#
						# DEFAULT VALUES
						#
						
						if 'width' not in self.tiles[k]:
							self.tiles[k]['width'] = self.images[self.tiles[k]['src']].get_width()
							
						if 'height' not in self.tiles[k]:
							self.tiles[k]['height'] = self.images[self.tiles[k]['src']].get_height()
							
						if 'walkable' not in self.tiles[k]:
							self.tiles[k]['walkable'] = True
							
							
							
						#
						# repeat_x and repeat_y
						#
						
						if 'repeat_x' in self.tiles[k] or 'repeat_y' in self.tiles[k]:
							if 'repeat_x' in self.tiles[k]:
								repeat_x = self.tiles[k]['repeat_x']
								del self.tiles[k]['repeat_x'] # not needed to have those in memory anymore
							else:
								repeat_x = 1
							if 'repeat_y' in self.tiles[k]:
								repeat_y = self.tiles[k]['repeat_y']
								del self.tiles[k]['repeat_y']
							else:
								repeat_y = 1
							
							original = self.tiles[k]
							#print(original)
							for i in range(repeat_x):
								for j in range(repeat_y):
									if i == 0 and j == 0: # tile we already have
										continue
									k += 1
									new = original.copy()
									new['pos_x'] = original['pos_x'] + (i * original['width'])
									new['pos_y'] = original['pos_y'] + (j * original['height'])
									self.tiles.append(new)
									#print(str(i)+', '+str(j)+', '+str(k), self.tiles[k])
						
						k += 1
						
					self.tiles.append({})
					
				else: # settings
					vals = line.split(':', 1)
					vals[0] = vals[0].strip()
					vals[1] = vals[1].strip()
					
					if vals[0] in ['pos_x', 'pos_y', 'width', 'height', 'repeat_x', 'repeat_y']:
						vals[1] = int(vals[1])
					elif vals[0] in ['assume_center_pos', 'walkable']:
						if vals[1] == 'true':
							vals[1] = True
						else:
							vals[1] = False

					#print(vals)
					if tile_mode:
						self.tiles[k][vals[0]] = vals[1]
					else:
						self.general[vals[0]] = vals[1]


		f.close()
		self.tiles.pop()
		#print(self.tiles)
		
	def tile_within_square(self, tile, nw, se, offset = 0):
		if (tile['pos_y'] + tile['height']) >= (nw['y'] + offset) and tile['pos_y'] <= (se['y'] - offset) and (tile['pos_x'] + tile['width']) >= (nw['x'] + offset) and tile['pos_x'] <= (se['x'] - offset):
			#if offset > 0:
				#print(tile, nw, se)
			return True
		else:
			return False
			
	def draw_map(self, screen, x, y, gameW = 640, gameH = 480):
		self.pos_x = x
		self.pos_y = y

		nw = {'x': (x - (gameW / 2)), 'y': (y - (gameH / 2))}
		sw = {'x': (x - (gameW / 2)), 'y': (y + (gameH / 2))}
		se = {'x': (x + (gameW / 2)), 'y': (y + (gameH / 2))}
		ne = {'x': (x + (gameW / 2)), 'y': (y - (gameH / 2))}

		for tile in self.tiles: # loop our tiles
			if self.tile_within_square(tile, nw, se):
				#print(tile)
				screen.blit(self.images[tile['src']], ((tile['pos_x'] + (gameW / 2) - x), (tile['pos_y'] + (gameH / 2) - y)))
				if self.debug:
					pygame.draw.rect(screen, (255, 0, 0), (((tile['pos_x'] + (gameW / 2) - x), (tile['pos_y'] + (gameH / 2) - y)), (tile['width'], tile['height'])), 2)
