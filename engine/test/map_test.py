import sys
sys.path.append('../lib/')

import Tkinter
import Image, ImageTk
from map import *

map = map('main', '../../')

root = Tkinter.Tk()
root.geometry('640x480')
root.title('Map view')

x = 0
y = 0
gameW = 640
gameH = 480
nw = {'x': (x - (gameW / 2)), 'y': (y - (gameH / 2))}
sw = {'x': (x - (gameW / 2)), 'y': (y + (gameH / 2))}
se = {'x': (x + (gameW / 2)), 'y': (y + (gameH / 2))}
ne = {'x': (x + (gameW / 2)), 'y': (y - (gameH / 2))}

images = {}

for tile in map.tiles: # loop our tiles
	if 'pos_y' not in tile: # debugging
		print(tile)
	else :
		if map.tile_within_square(tile, nw, se):
			#print(tile)
			if tile['src'] not in images:
				image1 = Image.open('../../data/tiles/'+tile['src'])
				images[tile['src']] = ImageTk.PhotoImage(image1)
			label_image = Tkinter.Label(root, image = images[tile['src']])
			label_image.place(x = tile['pos_x'] + gameW / 2, y = tile['pos_y'] + gameH / 2, width = tile['width'], height = tile['height'])

root.mainloop()
