import pytmx
from map.obstacle import Obstacle

class TiledMap:
	def __init__(self, filename):
		tm = pytmx.load_pygame(filename, pixelalpha=True)
		self.width = tm.width * tm.tilewidth
		self.height = tm.height * tm.tileheight
		self.tmxdata = tm