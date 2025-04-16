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
from game_states import GameState
from weapons.map_weapon import MapWeapon

class Level:
	def __init__(self, map, completed):
		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.light_post = pygame.sprite.Group()

		self.player_attackable_sprite = pygame.sprite.Group()
		self.enemy_attackable_sprite  = pygame.sprite.Group()

		self.completed = completed

		# light surfaces
		# circle glow
		radius = 1000
		self.circle_surface = glow(100, radius, BRIGHT_DEFAULT)
		self.circle_surface.set_colorkey((0, 0, 0))
		self.circle_surface.set_alpha(255)
		self.light_circle = pygame.sprite.Sprite(self.light_post)
		self.light_circle.target = 'main'
		self.light_circle.image = self.circle_surface

		# ghost glow
		radius = 200
		self.ghost_glow = glow(210, radius, BRIGHT_DEFAULT + 40)
		self.ghost_glow.set_colorkey((0, 0, 0))
		self.ghost_glow.set_alpha(255)
		self.ghost_light = pygame.sprite.Sprite(self.light_post)
		self.ghost_light.target = 'ghost'
		self.ghost_light.image = self.ghost_glow
		self.ghost_light.rect = self.ghost_glow.get_rect(topleft=(0,0))

		# player hearts
		self.heart_full = pygame.image.load("graphics/coracao/full_heart.png").convert_alpha()
		self.heart_empty = pygame.image.load("graphics/coracao/empty_heart.png").convert_alpha()
		self.heart_size = 32
		self.heart_spacing = 10

		# flashlight
		self.flashlight = Flashlight((0, 0), math.pi/3, [self.light_post], 700)
		self.flashlight.target = 'main'
		self.flashlight.image.set_colorkey((0, 0, 0))
		self.flashlight.image.set_alpha(255)
		self.light_post.add(self.flashlight)

		# lights and shadows surface
		self.light_surface = pygame.Surface((WIDTH, HEIGTH))

		# load the map
		self.map = TiledMap(map)
		self.tmxdata = self.map.tmxdata

		# current enemies
		self.enemies = []

		# construct the map
		self.make_map()

		#Selects active player
		self.active_player = self.player1
		self.inactive_player = self.player2
		self.player1.change_active(True)
		self.player2.set_transparency(GHOST_ALPHA)


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

			tile = pygame.Surface((tile_object.width * SCALE_FACTOR,
									tile_object.height * SCALE_FACTOR))
			x = tile_object.x * SCALE_FACTOR
			y = tile_object.y * SCALE_FACTOR

			if tile_object.type == 'Spawn':
				if tile_object.name == 'P1':
					self.player1 = Player('diogo', (x, y), self.switch_player, self.drag_ghost, self.interact,
                        self.create_particle, [self.visible_sprites, self.enemy_attackable_sprite], self.obstacle_sprites)
				elif tile_object.name == 'P2':
					self.player2 = Player('lucas', (x, y), self.switch_player, self.drag_ghost, self.interact,
                        self.create_particle, [self.visible_sprites], self.obstacle_sprites)
				elif tile_object.name == 'Enemy' and not self.completed:
					self.enemies.append(Enemy('rat', (x, y), self.get_player_pos, self.get_player_sight, self.create_particle,
												[self.visible_sprites, self.player_attackable_sprite], self.obstacle_sprites))
			elif tile_object.name == "Start":
				self.leftDoor = Obstacle((x, y), tile, [self.obstacle_sprites])
			elif tile_object.name == "End":
				self.rightDoor = Obstacle((x, y), tile, [self.obstacle_sprites])
			elif tile_object.name == "Gun":
				self.weapon = Weapon("Initial_Weapon", 1, 400, (x, y), [self.visible_sprites])
			else:
				Obstacle((x, y), tile, [self.obstacle_sprites])


	def make_map(self):
		floor_surf = pygame.Surface((self.map.width * SCALE_FACTOR,
							   		 self.map.height * SCALE_FACTOR))
		self.render(floor_surf)
		self.visible_sprites.set_floor(floor_surf)

	def create_particle(self, caller, path, pos, direction):
		if caller == 'player':
			return Particle(path, pos, direction, self.active_player.inventory.weapon.damage, [self.visible_sprites], self.player_attackable_sprite)
		elif caller == 'enemy':
			return Particle(path, pos, direction, 1, [self.visible_sprites], self.enemy_attackable_sprite)

	def get_player_pos(self):
		rect = self.active_player.get_rect_center()
		pos = pygame.math.Vector2(rect[0], rect[1])
		return pos

	def get_player_sight(self):
		line = self.active_player.sight()
		return line

	def switch_changes(self, p1, p2):
		self.active_player = p2
		self.inactive_player = p1
		p1.change_active(False)
		p2.change_active(True)
		self.enemy_attackable_sprite.remove(p1)
		self.enemy_attackable_sprite.add(p2)
		p1.set_transparency(GHOST_ALPHA)
		p2.set_transparency(HUMAN_ALPHA)
		p2.switch_start = p1.switch_start

	def switch_player(self):
		if self.active_player == self.player1 and not self.player2.check_death():
			self.switch_changes(self.player1, self.player2)
		elif self.active_player == self.player2 and not self.player1.check_death():
			self.switch_changes(self.player2, self.player1)

	def is_game_over(self):
		return self.player1.check_death() and self.player2.check_death()

	def drag_ghost(self):
		if self.active_player == self.player1:
			self.player2.teleport_ghost(self.active_player.get_rect_center())
		else:
			self.player1.teleport_ghost(self.active_player.get_rect_center())

	def is_near(self, max_distance=100): # Por enquanto, fixo para 1 arma
		player_pos = pygame.math.Vector2(self.active_player.rect.centerx, self.active_player.rect.centery)
		item_pos = pygame.math.Vector2(self.weapon.rect.centerx, self.weapon.rect.centery)
		distance = player_pos.distance_to(item_pos)
		return distance <= max_distance
	
	def enemies_killed(self):
		for i in range(len(self.enemies)):
			if self.enemies[i].health > 0:
				return False
		return True

	def interact(self): # Por enquanto, fixo para 1 arma
		if self.is_near(100):
			self.active_player.inventory.change_weapon(self.weapon)
			self.active_player.casting_cooldown = self.weapon.cooldown

	def draw_hearts(self, surface):
		hearts = []
		for i in range(self.active_player.max_health):
			if i < self.active_player.health:
				hearts.append("full")  # Coração cheio
			else:
				hearts.append("empty")  # Coração vazio
		font = pygame.font.Font(None, 36)
		for i, heart_type in enumerate(hearts):
			x = 20 + i * (self.heart_size + self.heart_spacing)
			y = 20

			if heart_type == "full":
				surface.blit(self.heart_full, (x, y))
			else:
				color = (100, 100, 100)  # Cinza
				#surface.blit(self.heart_empty, (x, y))
			text = font.render("♥", True, color)
			surface.blit(text, (x, y))
	
	
	def nearest_door(self):
		vec_player = pygame.Vector2(self.active_player.get_rect_center())
		vec_left = pygame.Vector2(self.leftDoor.rect.center)
		vec_right = pygame.Vector2(self.rightDoor.rect.center)

		if vec_player.distance_to(vec_left) < SCALE_FACTOR*TILESIZE/2:
			return 0
		elif vec_player.distance_to(vec_right) < SCALE_FACTOR*TILESIZE/2:
			return 1
		else:
			return -1			

	def run(self, state):
		# update and draw the game
		self.light_surface.fill('black')
		self.light_surface.set_alpha(255)
		if state == GameState.PLAYING:
			self.visible_sprites.update()
		self.visible_sprites.custom_draw(self.active_player, self.inactive_player, self.light_post, self.light_surface)
		self.active_player.inventory.draw(pygame.display.get_surface())
		self.draw_hearts(pygame.display.get_surface())
		self.light_post.update(self.get_player_sight())
		if self.enemies_killed():
			return self.nearest_door()	
		else:
			return -1
