import io
import os
import pygame


class map:
	file = ''
	loaded = []
	npc_files = []
	tiles = []
	general = {}
	images = {}
	debug = False
	pos_x = 0
	pos_y = 0

	def __init__(self, name='main', prefix=os.path.join('..', '')):
		#print(name)
		if name:
			self.load_map(name, prefix)

	def load_map(self, name, prefix=os.path.join('..', '')):
		#print(name)
		self.tiles = []
		self.general = {}
		self.npc_files = []
		self.file = name

		tile_mode = False
		with io.open(prefix + os.path.join('data', 'maps', '') + name + '.map', 'r') as f:
			k = 0

			if self.file in self.loaded:
				loaded = True
			else:
				loaded = False
				self.loaded.append(self.file)

			for line in f.readlines():  # loop through file
				if '#' in line:  # comment found
					parts = line.split('#', 1)
					#print(parts)
					line = parts[0]
				line = line.strip()

				if line != '':
					#print(line, sep = '', end = '\n')  # echo whole file
					if line[0:1] == '~':

						if not tile_mode:
							#print(self.general)

							if 'start_cords' in self.general:
								cords = self.general['start_cords'].split(',')
								self.general['start_pos_x'] = int(cords[0])
								self.general['start_pos_y'] = int(cords[1])
								del self.general['start_cords']

							if 'npc' in self.general:
								if not loaded:
									npcs = self.general['npc'].split(',')
									for npc in npcs:
										npc = npc.strip()
										self.npc_files.append(os.path.join('npc', '') + npc)
								del self.general['npc']

							tile_mode = True
						else:
							#print(str(k), self.tiles[k])

							if 'src' in self.tiles[k] and self.tiles[k]['src'] not in self.images:
								self.images[self.tiles[k]['src']] = pygame.image.load(prefix + os.path.join('data', 'tiles', '') + self.tiles[k]['src'])

							if 'size' in self.tiles[k]:
								parts = self.tiles[k]['size'].split('x')
								self.tiles[k]['width'] = int(parts[0])
								self.tiles[k]['height'] = int(parts[1])
								del self.tiles[k]['size']

							if 'cords' in self.tiles[k]:
								self.tiles[k]['pos'] = self.tiles[k]['cords']
								del self.tiles[k]['cords']

							if 'pos' in self.tiles[k]:
								cords = self.tiles[k]['pos'].split(',')
								self.tiles[k]['pos_x'] = int(cords[0])
								self.tiles[k]['pos_y'] = int(cords[1])
								del self.tiles[k]['pos']

							if 'repeat' in self.tiles[k]:
								parts = self.tiles[k]['repeat'].split('x')
								self.tiles[k]['repeat_x'] = int(parts[0])
								self.tiles[k]['repeat_y'] = int(parts[1])
								del self.tiles[k]['repeat']

							#
							# DEFAULT VALUES
							#

							if 'width' not in self.tiles[k]:
								if 'src' in self.tiles[k]:
									self.tiles[k]['width'] = self.images[self.tiles[k]['src']].get_width()
								else:
									self.tiles[k]['width'] = 0

							if 'height' not in self.tiles[k]:
								if 'src' in self.tiles[k]:
									self.tiles[k]['height'] = self.images[self.tiles[k]['src']].get_height()
								else:
									self.tiles[k]['height'] = 0

							if 'walkable' not in self.tiles[k]:
								self.tiles[k]['walkable'] = True

							#
							# repeat_x and repeat_y
							#
							if 'repeat_x' in self.tiles[k] or 'repeat_y' in self.tiles[k]:
								if 'repeat_x' in self.tiles[k]:
									repeat_x = self.tiles[k]['repeat_x']
									del self.tiles[k]['repeat_x']  # not needed to have those in memory anymore
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
										if i == 0 and j == 0:  # tile we already have
											continue
										k += 1
										new = original.copy()
										new['pos_x'] = original['pos_x'] + (i * original['width'])
										new['pos_y'] = original['pos_y'] + (j * original['height'])
										self.tiles.append(new)
										#print(str(i)+', '+str(j)+', '+str(k), self.tiles[k])

							k += 1

						self.tiles.append({})

					else:  # settings
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

			self.tiles.pop()

	def tile_within_square(self, tile, nw, se, offset=0):
		if (tile['pos_y'] + tile['height']) >= (nw['y'] + offset) and tile['pos_y'] <= (se['y'] - offset) and (tile['pos_x'] + tile['width']) >= (nw['x'] + offset) and tile['pos_x'] <= (se['x'] - offset):
			return True
		else:
			return False

	def draw_map(self, screen, x, y, gameW=640, gameH=480):
		self.pos_x = x
		self.pos_y = y

		nw = {'x': (x - (gameW / 2)), 'y': (y - (gameH / 2))}
		se = {'x': (x + (gameW / 2)), 'y': (y + (gameH / 2))}

		for tile in self.tiles:  # loop our tiles
			if self.tile_within_square(tile, nw, se):
				#print(tile)
				if 'src' in tile:
					screen.blit(self.images[tile['src']], ((tile['pos_x'] + (gameW / 2) - x), (tile['pos_y'] + (gameH / 2) - y)))
				if self.debug and False:
					pygame.draw.rect(screen, (255, 0, 0), (((tile['pos_x'] + (gameW / 2) - x), (tile['pos_y'] + (gameH / 2) - y)), (tile['width'], tile['height'])), 2)
