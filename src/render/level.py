import pygame
from settings import *
from render.support import import_csv_layout
from render.camera import YSortCameraGroup
from map.tile import Tile
from characters.player import Player


class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		layout = {
			'boundary': import_csv_layout('./layouts/teste_boundary.csv'),
		}

		for style, layout in layout.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					x = col_index * TILESIZE
					y = row_index * TILESIZE
					if style == 'boundary':
						Tile((x, y), [self.obstacle_sprites], 'invisible')

		self.player1 = Player('./graphics/1.png', (144, 144), [self.visible_sprites], self.obstacle_sprites)


	def run(self):
		# update and draw the game
		self.visible_sprites.update()
		self.visible_sprites.custom_draw(self.player1)