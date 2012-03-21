class map:
	tiles = []
	general = {}
	
	def __init__(self, name = 'main', prefix = '../'):
		#print(name)
		self.load_map(name, prefix)

	def load_map(self, name, prefix = '../'):
		#print(name)
		self.tiles = []
		self.general = {}
		tile_mode = False
		f = open(prefix+'data/maps/'+name+'.map', 'r') # open map
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
		
	def tile_within_square(self, tile, nw, se):
		if (tile['pos_y'] + tile['height']) >= nw['y'] and tile['pos_y'] <= se['y'] and (tile['pos_x'] + tile['height']) >= nw['x'] and tile['pos_x'] <= se['x']:
			return True
		else:
			return False
