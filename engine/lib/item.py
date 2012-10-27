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
	power_type = ''
	burden = 0
	src = False
	img = False
	msg = True
	summary = ''
	instant = False
	pickup_on_touch = False
	duration = 0
	uses = 1
	used = 0
	total_used = 0
	remove_after_used = True

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

					if vals[0] in ['value', 'duration', 'uses']:
						vals[1] = int(vals[1])
					elif vals[0] in ['burden']:
						vals[1] = float(vals[1])
					elif vals[0] in ['instant', 'msg', 'pickup_on_touch', 'remove_after_used']:
						if vals[1] == 'true':
							vals[1] = True
						else:
							vals[1] = False

					if vals[0] == 'power':
						p_vals = vals[1].split(' ', 1)
						if '.' in p_vals[0]:
							p_vals[0] = float(p_vals[0])
						else:
							p_vals[0] = int(p_vals[0])

						self.power = p_vals[0]
						self.power_type = p_vals[1]
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
					if vals[0] == 'duration':
						self.duration = vals[1]
					if vals[0] == 'uses':
						self.uses = vals[1]
					if vals[0] == 'remove_after_used':
						self.remove_after_used = vals[1]

					if vals[0] == 'src':
						self.src = vals[1]
						self.img = pygame.image.load(prefix + os.path.join('data', 'items', '') + self.src)
						self.img.convert_alpha()
						self.h = self.img.get_height()
						self.w = self.img.get_width()

	def use(self, **args):
		if self.used < self.uses or self.uses == 0:  # maximum amount of uses hasn't been reached
			self.used += 1
			self.total_used += 1

			target = args.get('target', self.owner)

			if self.power_type == 'health':
				target.health += self.power

		if self.used >= self.uses and self.uses != 0 and self.remove_after_used:
			self.owner.bag.remove(self)
