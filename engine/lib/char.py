import pygame, os
from pygame.locals import *

class char:
	x = 0
	y = 0
	dir = 's'
	moving = False
	debug = False
	images = {}
	general = {}
	frames = {}
	state = ''
	
	def __init__(self, file = os.path.join('hero', 'main', 'main'), prefix = os.path.join('..', '')):
		if file:
			self.load_file(file, prefix)
		
	def load_file(self, file, prefix = os.path.join('..', '')):

		self.frames[file] = {}
		self.general = {}
		self.state = file
		temp = {}
		
		curdir  = ''
		curmove = ''
		folder  = os.path.split(file)
		
		f = open(prefix+os.path.join('data', 'char', '')+file+'.char', 'r') # open file
		
		for line in f.readlines(): # loop through file
			if '#' in line: # comment found
				parts = line.split('#', 1)
				#print(parts)
				line = parts[0]
			line = line.strip()
			
			if line != '':
				#print(line, sep = '', end = '\n') # echo whole file
				
				if line == '~':
					pass
					
				elif line == '*' or line == '+':
					
					if curmove =='g':
						pass
					
					else:
						# frame savings etc. go here
					
						#
						# DEFAULTS
						#
						if 'pos_x' not in temp:
							temp['pos_x'] = self.general['def_pos_x']
							
						if 'pos_y' not in temp:
							temp['pos_y'] = self.general['def_pos_y']
							
						if 'width' not in temp:
							temp['width'] = self.general['def_w']
							
						if 'height' not in temp:
							temp['height'] = self.general['def_h']
							
						if 'src' not in temp:
							temp['src'] = self.general['def_src']
						#
						# END DEFAULTS
						#
						
						savestring = temp['src']+','+str(temp['pos_x'])+','+str(temp['pos_y'])+','+str(temp['width'])+','+str(temp['height'])
						
						if savestring not in self.images:
							if temp['src'] not in self.images:
								image = pygame.image.load(prefix+os.path.join('data', 'char', '')+folder[0]+os.sep+temp['src'])
								image.convert_alpha()
								self.images[temp['src']] = image
								
							self.images[savestring] = self.images[temp['src']].subsurface(Rect((temp['pos_x'], temp['pos_y']), (temp['width'], temp['height'])) )
							#pygame.Rect((left, top), (width, height)): return Rect
						
						self.frames[file][curdir][curmove].append(savestring)
					
						temp = {}
					
					if line == '*':
						if curmove == 'g':
							curmove = 's'
						elif curmove == 's':
							curmove = 'm'
						

				elif line == 'n:' or line == 's:' or line == 'w:' or line == 'e:':
					curdir  = line[:-1]
					curmove = 'g'
					self.frames[file][curdir] = {'s': [], 'm': []}
					
				else: # properties and values
					
					vals = line.split(':', 1)
					vals[0] = vals[0].strip()
					vals[1] = vals[1].strip()
					
					if vals[0] in ['def_w', 'def_h', 'def_pos_y', 'def_pos_x', 'pos_x', 'pos_y', 'width', 'height']:
						vals[1] = int(vals[1])
					elif vals[0] in ['']:
						if vals[1] == 'true':
							vals[1] = True
						else:
							vals[1] = False

					#print(vals)
					if curdir == '':
						self.general[vals[0]] = vals[1]
					else:
						temp[vals[0]] = vals[1]
		
		
		f.close()

	def hittest(self, **args):
		if not args.get('dx'):
			dx = 0
		else:
			dx = args.get('dx')
			
		if not args.get('dy'):
			dy = 0
		else:
			dy = args.get('dy')
			
		if not args.get('move'):
			move = True
		else:
			move = args.get('move')
		
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
		
		ori_x = self.x
		ori_y = self.y
		pos_x = ori_x
		pos_y = ori_y
		
		ax = 0
		while ax <= dx:
			#print('x: '+str(ax))
			
			ay = 0
			while ay <= dy:
				#print('y: '+str(ay))
				#print('x,y: '+str(ax)+','+str(ay)+' - pos_x,y: '+str(pos_x)+','+str(pos_y)+' - ori_x,y: '+str(ori_x)+','+str(ori_y))
				
				if move:
					self.x = pos_x
					self.y = pos_y
				
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
							if map.tile_within_square(tile, {'x': pos_x, 'y': pos_y}, {'x': (pos_x + self.images[self.frames[self.state][self.dir]['m'][0]].get_width()), 'y': (pos_y + self.images[self.frames[self.state][self.dir]['m'][0]].get_height())}, 1):
								if self.debug and args.get('screen'):
									pygame.draw.rect(args.get('screen'), (0, 0, 255), (((tile['pos_x'] + (args.get('gameW') / 2) - map.pos_x), (tile['pos_y'] + (args.get('gameH') / 2) - map.pos_y)), (tile['width'], tile['height'])), 2)
								return True
							
				ay += 1
				
			ax += 1
			
		#print('...')
		if move:
			self.x = pos_x
			self.y = pos_y
		
		return False
