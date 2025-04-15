import pygame
import math
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
  
		#Selects active player
		self.active_player = self.player1
		self.player1.active = True
		self.player2.set_transparency(128)

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
		self.player1 = Player('diogo', (288, 288), self.switch_player, self.drag_ghost, 
                        self.create_particle, [self.visible_sprites, self.enemy_attackable_sprite], self.obstacle_sprites)
		self.player2 = Player('lucas', (288, 288), self.switch_player, self.drag_ghost,
                        self.create_particle, [self.visible_sprites], self.obstacle_sprites)

	def make_map(self):
		floor_surf = pygame.Surface((self.map.width * SCALE_FACTOR,
							   		 self.map.height * SCALE_FACTOR))
		self.render(floor_surf)
		self.visible_sprites.set_floor(floor_surf)

	def create_particle(self, caller, pos, direction):
		if caller == 'player':
			return Particle(pos, direction, [self.visible_sprites], self.player_attackable_sprite)

	def get_player_pos(self):
		pos = pygame.math.Vector2(self.active_player.rect.center[0], self.active_player.rect.center[1])
		return pos

	def get_player_sight(self):
		line = self.active_player.sight()
		return line

	def switch_changes(self, p1, p2):
		self.active_player = p2
		p1.active = False
		p2.active = True
		self.enemy_attackable_sprite.remove(p1)
		self.enemy_attackable_sprite.add(p2)
		p1.set_transparency(GHOST_ALPHA)
		p2.set_transparency(HUMAN_ALPHA)
		p2.switch_start = p1.switch_start
 
	def switch_player(self):
		if self.active_player == self.player1:
			self.switch_changes(self.player1, self.player2)
		else:
			self.switch_changes(self.player2, self.player1)
   	
	def drag_ghost(self):
		if self.active_player == self.player1:
			self.player2.rect.center = self.active_player.rect.center
			self.player2.hitbox = self.player2.rect
		else:
			self.player1.rect.center = self.active_player.rect.center
			self.player1.hitbox = self.player1.rect
   
	def run(self):
		# update and draw the game
		self.visible_sprites.update()
		self.visible_sprites.custom_draw(self.active_player)