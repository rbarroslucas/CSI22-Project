import pygame
from settings import *
from render.camera import YSortCameraGroup
from map.wall import Wall
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
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Wall('./graphics/2.png', (x,y), [self.visible_sprites,self.obstacle_sprites])
				if col == 'p':
					self.player1 = Player('./graphics/1.png', (x,y), self.obstacle_sprites, [self.visible_sprites])

	def run(self):
		# update and draw the game
		self.visible_sprites.update()
		self.visible_sprites.custom_draw(self.player1)