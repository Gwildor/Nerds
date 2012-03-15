class map:
	tiles = []
	general = {}
	
	def __init__(self, name = 'main', prefix = '../'):
		#print(name)
		self.load_map(name, prefix)

	def load_map(self, name, prefix = '../'):
		#print(name)
		tile_mode = False
		f = open(prefix+'data/maps/'+name+'.map', 'r') # open map
		
		for line in f.readlines(): # loop through file
			line = line.strip()
			x = 0
			if line != '':
				#print(line, sep = '', end = '\n') # echo whole file
				if line[0:1] == '~':
					if not tile_mode:
						print(self.general)
						tile_mode = True
					else:
						print(self.tiles[x])
						
						if 'repeat_x' in self.tiles[x] or 'repeat_y' in self.tiles[x]:
							if 'repeat_x' in self.tiles[x]:
								repeat_x = self.tiles[x]['repeat_x']
							else:
								repeat_x = 1
							if 'repeat_y' in self.tiles[x]:
								repeat_y = self.tiles[x]['repeat_y']
							else:
								repeat_y = 1
							
							original = self.tiles[x]
							for i in range(repeat_x):
								for j in range(repeat_y):
									if i == 0 and j == 0: # tile we already have
										continue
									x += 1
									new = original.copy()
									new['pos_x'] = original['pos_x'] + (i * original['width'])
									new['pos_y'] = original['pos_y'] + (j * original['height'])
									self.tiles.append(new)
									print(str(i)+', '+str(j)+' ', self.tiles[x])
						
						x += 1
						
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
						self.tiles[x][vals[0]] = vals[1]
					else:
						self.general[vals[0]] = vals[1]


		f.close()
