import pygame
from settings import *
from map.tiledmap import TiledMap
from map.obstacle import Obstacle
from render.support import import_csv_layout
from render.camera import YSortCameraGroup
from characters.player import Player
from characters.enemy import Enemy
from characters.particle import Particle


class Level:
	def __init__(self):
		# boundary surface for debugging
		self.boundary_surface = pygame.Surface((TILESIZE, TILESIZE))
		self.boundary_surface.fill('red')

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.player_attackable_sprite = pygame.sprite.Group()
		self.enemy_attackable_sprite  = pygame.sprite.Group()

		# load the map
		self.map = TiledMap('./layouts/teste.tmx')
		self.tmxdata = self.map.tmxdata

		# current enemies
		self.enemies = []

		# construct the map
		self.make_map()

	def render(self, surface):
		si = self.tmxdata.get_tile_image_by_gid
		for layer in self.tmxdata.visible_layers:
			if hasattr(layer, 'data'):
				for x, y, gid in layer:
					tile = si(gid)
					if tile:
						tile = pygame.transform.scale(tile, (self.tmxdata.tilewidth * SCALE_FACTOR,
										  				 self.tmxdata.tileheight * SCALE_FACTOR))
						surface.blit(tile, (x * self.tmxdata.tilewidth * SCALE_FACTOR,
						  					y * self.tmxdata.tileheight * SCALE_FACTOR))
		for tile_object in self.tmxdata.objects:
			if tile_object.type == 'Obstacle':
				tile = pygame.Surface((tile_object.width * SCALE_FACTOR,
						   			   tile_object.height * SCALE_FACTOR))
				x = tile_object.x * SCALE_FACTOR
				y = tile_object.y * SCALE_FACTOR
				Obstacle((x, y), tile, [self.obstacle_sprites])

		# load the player
		self.enemies.append(Enemy('diogo', (376, 288), self.get_player_pos, self.get_player_sight, [self.visible_sprites, self.player_attackable_sprite], self.obstacle_sprites))
		self.player1 = Player('diogo', (288, 288), self.create_particle, [self.visible_sprites, self.enemy_attackable_sprite], self.obstacle_sprites)

	def make_map(self):
		floor_surf = pygame.Surface((self.map.width * SCALE_FACTOR,
							   		 self.map.height * SCALE_FACTOR))
		self.render(floor_surf)
		self.visible_sprites.set_floor(floor_surf)

	def create_particle(self, caller, pos, direction):
		if caller == 'player':
			return Particle(pos, direction, [self.visible_sprites], self.player_attackable_sprite)

	def get_player_pos(self):
		return self.player1.rect.center

	def get_player_sight(self):
		return self.player1.sight()
 
	def run(self):
		# update and draw the game
		self.visible_sprites.update()
		self.visible_sprites.custom_draw(self.player1)