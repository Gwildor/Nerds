import io
import os
import pygame


class item:
	x = 0
	y = 0
	w = 0
	h = 0
	map = ''
	file = ''
	debug = False
	owner = False
	value = 0
	power = 0
	burden = 0
	src = False
	img = False
	msg = True
	summary = ''
	instant = False
	pickup_on_touch = False

	def __init__(self, file, prefix=os.path.join('..', '')):
		if file:
			self.load_file(file, prefix)

	def load_file(self, file, prefix=os.path.join('..', '')):

		self.file = file

		with io.open(prefix + os.path.join('data', 'items', '') + file + '.item', 'r') as f:
			for line in f.readlines():  # loop through file

				if '#' in line:  # comment found
					parts = line.split('#', 1)
					line = parts[0]
				line = line.strip()

				if line != '':
					#print(line)  # echo whole file

					vals = line.split(':', 1)
					vals[0] = vals[0].strip()
					vals[1] = vals[1].strip()

					if vals[0] in ['power', 'value']:
						vals[1] = int(vals[1])
					elif vals[0] in ['burden']:
						vals[1] = float(vals[1])
					elif vals[0] in ['instant', 'msg', 'pickup_on_touch']:
						if vals[1] == 'true':
							vals[1] = True
						else:
							vals[1] = False

					if vals[0] == 'power':
						self.power = vals[1]
					if vals[0] == 'value':
						self.value = vals[1]
					if vals[0] == 'burden':
						self.burden = vals[1]
					if vals[0] == 'instant':
						self.instant = vals[1]
					if vals[0] == 'pickup_on_touch':
						self.pickup_on_touch = vals[1]
					if vals[0] == 'msg':
						self.msg = vals[1]
					if vals[0] == 'summary':
						self.summary = vals[1]

					if vals[0] == 'src':
						self.src = vals[1]
						self.img = pygame.image.load(prefix + os.path.join('data', 'items', '') + self.src)
						self.img.convert_alpha()
						self.h = self.img.get_height()
						self.w = self.img.get_width()
