import pygame
import math
from settings import *
from map.tiledmap import TiledMap
from map.obstacle import Obstacle
from render.support import import_csv_layout
from render.camera import YSortCameraGroup
from render.flashlight import *
from characters.player import Player
from characters.enemy import Enemy
from characters.particle import Particle

class Level:
	def __init__(self):
		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.light_post = pygame.sprite.Group()

		self.player_attackable_sprite = pygame.sprite.Group()
		self.enemy_attackable_sprite  = pygame.sprite.Group()

		# shadows
		self.dark = pygame.Surface((WIDTH, HEIGTH))
		self.dark.fill('black')
		self.darkness = pygame.sprite.Sprite(self.light_post)
		self.darkness.image = self.dark
		self.darkness.rect = self.dark.get_rect(topleft=(0, 0))
		self.darkness.alpha = 255
		self.darkness.image.set_alpha(self.darkness.alpha)

		# light surfaces

		# circle glow
		radius = 50
		self.circle_surface = glow(10, radius, 10)
		pygame.draw.circle(self.circle_surface, (122, 122, 122), (radius, radius), radius)
		self.circle_surface.set_colorkey((0, 0, 0))
		self.circle_surface.set_alpha(255)
		self.light_circle = pygame.sprite.Sprite(self.light_post)
		self.light_circle.image = self.circle_surface

		# flashlight
		self.sector_surface = create_circle_sector(1000, 0, math.pi/3)
		self.flashlight = Flashlight((0, 0), self.sector_surface, [self.light_post])
		self.flashlight.image.set_colorkey((0, 0, 0))
		self.flashlight.image.set_alpha(255)
		self.light_post.add(self.flashlight)

		# lights and shadows surface
		self.light_surface = pygame.Surface((WIDTH, HEIGTH))

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
		line = self.player1.sight()
		return line

	def run(self):
		# update and draw the game
		self.visible_sprites.update()
		self.visible_sprites.custom_draw(self.player1, self.light_post, self.light_surface)

		self.light_post.update(self.get_player_sight())