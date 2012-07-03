import pygame, os
from pygame.locals import *

class char:
	x = 0
	y = 0
	speed = 2
	dir = 's'
	olddir = 's'
	ticks = 0
	frame = 0
	moving = False
	talking = False
	debug = False
	images = {}
	general = {}
	frames = {}
	framecount = {}
	file = ''
	state = ''
	
	def __init__(self, file = os.path.join('hero', 'main', 'main'), prefix = os.path.join('..', '')):
		if file:
			self.load_file(file, prefix)
		
	def load_file(self, file, prefix = os.path.join('..', '')):

		self.frames[file] = {}
		self.framecount[file] = {}
		self.general = {}
		self.file = file
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
						self.framecount[file][curdir][curmove] += 1
					
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
					self.framecount[file][curdir] = {'s': 0, 'm': 0}
					
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
		
	def draw_char(self, screen, **args):
		if 'x' in args:
			x = args['x']
		else:
			if 'gameW' in args:
				x = self.x + (args['gameW'] / 2)
			else:
				x = self.x
			
		if 'y' in args:
			y = args['y']
		else:
			if 'gameH' in args:
				y = self.y + (args['gameH'] / 2)
			else:
				y = self.y

			
		if (self.moving and self.state == 's') or (not self.moving and self.state == 'm') or (self.dir != self.olddir):
			self.frame = 0
			self.ticks = 0
			
		if self.moving:
			self.state = 'm'
		else:
			self.state = 's'
			
		if self.ticks % 20 == 0: # hardcoded number for now
			if self.frame + 1 == self.framecount[self.file][self.dir][self.state]:
				self.frame = 0
			else:
				self.frame += 1
			
		screen.blit(self.images[self.frames[self.file][self.dir][self.state][self.frame]], (x, y))
		
		self.olddir = self.dir
		self.ticks += 1

	def hittest(self, **args):
		if 'dx' in args:
			dx = args['dx']
		else:
			dx = 0
			
		if 'dy' in args:
			dy = args['dy']
		else:
			dy = 0
			
		if 'move' in args:
			move = args['move']
		else:
			move = True
		
		if 'map' in args:
			map = args['map']
		else:
			map = False
		
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
							if map.tile_within_square(tile, {'x': pos_x, 'y': pos_y}, {'x': (pos_x + self.images[self.frames[self.file][self.dir]['m'][0]].get_width()), 'y': (pos_y + self.images[self.frames[self.file][self.dir]['m'][0]].get_height())}, 1):
								if self.debug and 'screen' in args:
									pygame.draw.rect(args['screen'], (0, 0, 255), (((tile['pos_x'] + (args['gameW'] / 2) - map.pos_x), (tile['pos_y'] + (args['gameH'] / 2) - map.pos_y)), (tile['width'], tile['height'])), 2)
								return True
							
				ay += 1
				
			ax += 1
			
		#print('...')
		if move:
			self.x = pos_x
			self.y = pos_y
		
		return False
		
	def move_to(self, **args):

		if 'x' in args:
			x = args['x']
		else:
			x = self.x
			
		if 'y' in args:
			y = args['y']
		else:
			y = self.y
			
		if 'map' in args:
			map = args['map']
		else:
			map = False
			
		dx = x - self.x
		dy = y - self.y
		
		if x - self.speed <= self.x and y - self.speed <= self.y and x + self.speed >= self.x and y + self.speed >= self.y:
		#if dx < self.speed and 
			self.moving = False
			return True
		else:
			self.moving = True
			
			if self.x < x - self.speed:
				#print('e')
				if not self.hittest(dx = 1, map = map, move = False):
					self.dir = 'e'
					self.hittest(dx = self.speed, map = map)
				elif not self.hittest(dy = 1, map = map, move = False):
					self.dir = 's'
					self.hittest(dy = self.speed, map = map)
				elif not self.hittest(dy = -1, map = map, move = False):
					self.dir = 'n'
					self.hittest(dy = -self.speed, map = map)
				else:
					self.moving = False
			elif self.x > x + self.speed:
				#print('w')
				if not self.hittest(dx = -1, map = map, move = False):
					self.dir = 'w'
					self.hittest(dx = -self.speed, map = map)
				elif not self.hittest(dy = 1, map = map, move = False):
					self.dir = 's'
					self.hittest(dy = self.speed, map = map)
				elif not self.hittest(dy = -1, map = map, move = False):
					self.dir = 'n'
					self.hittest(dy = -self.speed, map = map)
				else:
					self.moving = False
			elif self.y < y - self.speed:
				#print('s')
				if not self.hittest(dy = 1, map = map, move = False):
					self.dir = 's'
					self.hittest(dy = self.speed, map = map)
				elif not self.hittest(dx = 1, map = map, move = False):
					self.dir = 'e'
					self.hittest(dx = self.speed, map = map)
				elif not self.hittest(dx = -1, map = map, move = False):
					self.dir = 'w'
					self.hittest(dx = -self.speed, map = map)
				else:
					self.moving = False
			elif self.y > y + self.speed:
				#print('n')
				if not self.hittest(dy = -1, map = map, move = False):
					self.dir = 'n'
					self.hittest(dy = -self.speed, map = map)
				elif not self.hittest(dx = 1, map = map, move = False):
					self.dir = 'e'
					self.hittest(dx = self.speed, map = map)
				elif not self.hittest(dx = -1, map = map, move = False):
					self.dir = 'w'
					self.hittest(dx = -self.speed, map = map)
				else:
					self.moving = False
				
			return False
			
	def interact(self, **args):
		start_talk = False
		
		if 'npcs' in args:
			npcs = args['npcs']
		else:
			npcs = False
			
		if npcs:
			for npc in npcs:
				if self.dir == 'n':
					if self.hittest(dy = -1, npcs = [npc], move = False):
						npc.dir = 's'
						start_talk = False
				elif self.dir == 's':
					if self.hittest(dy = 1, npcs = [npc], move = False):
						npc.dir = 'n'
						start_talk = False
				elif self.dir == 'w':
					if self.hittest(dx = -1, npcs = [npc], move = False):
						npc.dir = 'e'
						start_talk = False
				elif self.dir == 'e':
					if self.hittest(dx = 1, npcs = [npc], move = False):
						npc.dir = 'w'
						start_talk = False
					
		if start_talk:
			npc.moving = False
			npc.talking = True
			self.moving = False
			self.talking = True
			npc.listen(speaker = self)
			return
			
	def listen(self, **args):
		pass
