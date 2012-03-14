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
						x += 1
					self.tiles.append({})
				else: # settings
					vals = line.split(':', 1)
					vals[0] = vals[0].strip()
					vals[1] = vals[1].strip()
					
					"""
					assume_center_pos
					walkable: true
					"""
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
