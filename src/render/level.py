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
	"""
    Representa uma fase (nível) do jogo, responsável por carregar e gerenciar os elementos do mapa,
    como jogadores, inimigos, obstáculos, luzes, partículas, interações e HUD.

    A classe também trata a lógica de renderização, atualização dos sprites e mudanças de estado
    durante a execução do jogo.

    Atributos:
        visible_sprites (YSortCameraGroup): Grupo de sprites visíveis com ordenação por profundidade.
        obstacle_sprites (pygame.sprite.Group): Grupo de sprites que funcionam como obstáculos.
        light_post (pygame.sprite.Group): Grupo de sprites que emitem ou interagem com luz.
        player_attackable_sprite (pygame.sprite.Group): Grupo de sprites que podem ser atacados por inimigos.
        enemy_attackable_sprite (pygame.sprite.Group): Grupo de sprites que podem ser atacados pelos jogadores.
        completed (bool): Indica se o nível já foi completado.
        circle_surface (pygame.Surface): Superfície de iluminação circular para o jogador ativo.
        ghost_glow (pygame.Surface): Superfície de iluminação suave para o jogador inativo (fantasma).
        heart_full/heart_empty (pygame.Surface): Imagens dos corações cheios e vazios do HUD.
        flashlight (Flashlight): Lanterna que emite um cone de luz a partir do jogador ativo.
        light_surface (pygame.Surface): Superfície geral para renderização de luz e sombras.
        map (TiledMap): Mapa carregado a partir de um arquivo TMX.
        tmxdata (pytmx.TiledMap): Dados brutos do mapa no formato TMX.
        enemies (list): Lista dos inimigos instanciados no nível.
        player1/player2 (Player): Instâncias dos jogadores.
        active_player/inactive_player (Player): Jogador atualmente controlado e o outro jogador.
        weapon (MapWeapon): Arma disponível para coleta no nível.
        leftDoor/rightDoor (Obstacle): Portas localizadas no início e fim do mapa.

    Métodos:
        render(surface): Renderiza as camadas e objetos do mapa.
        make_map(): Cria a superfície de fundo e popula os grupos de sprites.
        create_particle(caller, path, pos, direction): Cria uma partícula de ataque baseada em jogador ou inimigo.
        get_player_pos(): Retorna a posição do jogador ativo.
        get_player_sight(): Retorna a linha de visão do jogador ativo.
        switch_changes(p1, p2): Realiza a troca de jogador ativo e inativo.
        switch_player(): Alterna entre os dois jogadores, se possível.
        is_game_over(): Retorna se ambos os jogadores morreram.
        drag_ghost(): Teleporta o jogador fantasma até o ativo.
        is_near(max_distance): Verifica se o jogador está próximo de um item interagível.
        enemies_killed(): Verifica se todos os inimigos foram derrotados.
        interact(): Realiza a ação de interação com a arma do mapa.
        draw_hearts(surface): Desenha os corações de vida do jogador ativo na tela.
        nearest_door(): Retorna qual porta está mais próxima do jogador ativo.
        set_players(player=1): Define qual jogador começa como ativo.
        run(state): Atualiza e renderiza o estado atual do nível com base no estado do jogo.
    """
    
	def __init__(self, map, completed):
		"""
    	Inicializa o nível, carregando o mapa, jogadores, inimigos, sistema de luz, HUD e grupos de sprites.

    	Args:
    	    map (str): Caminho para o arquivo do mapa no formato TMX.
    	    completed (bool): Indica se o nível já foi concluído anteriormente.
    	"""
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

		self.set_players()



	def render(self, surface):
		"""
    	Renderiza todas as camadas e objetos do mapa sobre a superfície fornecida.

    	Args:
    	    surface (pygame.Surface): Superfície onde o mapa será desenhado.
    	"""
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
			elif tile_object.type == 'Enemy' and not self.completed:
					self.enemies.append(Enemy(tile_object.name, (x, y), self.get_player_pos, self.get_player_sight, self.create_particle,
												[self.visible_sprites, self.player_attackable_sprite], self.obstacle_sprites))
			elif tile_object.name == "Start":
				self.leftDoor = Obstacle((x, y), tile, [self.obstacle_sprites])
			elif tile_object.name == "End":
				self.rightDoor = Obstacle((x, y), tile, [self.obstacle_sprites])
			elif tile_object.name == "Gun":
				self.weapon = MapWeapon("Initial_Weapon", 1, 400, (x, y), [self.visible_sprites])
			else:
				Obstacle((x, y), tile, [self.obstacle_sprites])


	def make_map(self):
		"""
    	Cria a superfície de fundo com base no mapa renderizado e define como fundo da câmera.
    	"""
		floor_surf = pygame.Surface((self.map.width * SCALE_FACTOR,
							   		 self.map.height * SCALE_FACTOR))
		self.render(floor_surf)
		self.visible_sprites.set_floor(floor_surf)

	def create_particle(self, caller, path, pos, direction):
		"""
    	Cria e retorna uma partícula de ataque com base no chamador (jogador ou inimigo).

    	Args:
    	    caller (str): 'player' ou 'enemy'.
    	    path (str): Caminho para o sprite da partícula.
    	    pos (tuple): Posição inicial da partícula.
    	    direction (pygame.Vector2): Direção de movimento da partícula.

    	Returns:
    	    Particle: Instância da partícula criada.
    	"""
		if caller == 'player':

			# cooldown buff handler
			if self.active_player.inventory.weapon.cooldown_buff_duration == 0:
				self.active_player.casting_cooldown = self.active_player.inventory.weapon.cooldown
				self.active_player.inventory.weapon.cooldown_buff = 0
			else:
				self.active_player.casting_cooldown = self.active_player.inventory.weapon.cooldown - self.active_player.inventory.weapon.cooldown_buff
				self.active_player.inventory.weapon.cooldown_buff_duration -= 1

			# damage buff handler
			if self.active_player.inventory.weapon.damage_buff_duration == 0:
				damage = self.active_player.inventory.weapon.damage
				self.active_player.inventory.weapon.damage_buff = 0
			else:
				damage = self.active_player.inventory.weapon.damage + self.active_player.inventory.weapon.damage_buff
				self.active_player.inventory.weapon.damage_buff_duration -= 1

			return Particle(path, pos, direction, damage, [self.visible_sprites], self.player_attackable_sprite)
		elif caller == 'enemy':
			return Particle(path, pos, direction, 1, [self.visible_sprites], self.enemy_attackable_sprite)

	def get_player_pos(self):
		"""
    	Retorna a posição central do jogador ativo.

    	Returns:
    	    pygame.Vector2: Posição do jogador ativo.
    	"""
		rect = self.active_player.get_rect_center()
		pos = pygame.math.Vector2(rect[0], rect[1])
		return pos

	def get_player_sight(self):
		"""
    	Retorna a linha de visão (vetor) do jogador ativo.

    	Returns:
    	    tuple: Par de pontos representando a linha de visão.
    	"""
		line = self.active_player.sight()
		return line

	def switch_changes(self, p1, p2):
		"""
    	Realiza a troca do jogador ativo e inativo, atualizando transparência e estado.

    	Args:
    	    p1 (Player): Jogador atual ativo.
    	    p2 (Player): Jogador que se tornará ativo.
    	"""
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
		"""
    	Alterna entre os dois jogadores, desde que o outro não esteja morto.
    	"""
		if self.active_player == self.player1 and not self.player2.check_death():
			self.switch_changes(self.player1, self.player2)
		elif self.active_player == self.player2 and not self.player1.check_death():
			self.switch_changes(self.player2, self.player1)

	def is_game_over(self):
		"""
    	Verifica se ambos os jogadores estão mortos.

    	Returns:
    	    bool: True se o jogo acabou, False caso contrário.
    	"""
		return self.player1.check_death() and self.player2.check_death()

	def drag_ghost(self):
		"""
    	Teleporta o jogador inativo (fantasma) até a posição do jogador ativo.
    	"""
		if self.active_player == self.player1:
			self.player2.teleport_ghost(self.active_player.get_rect_center())
		else:
			self.player1.teleport_ghost(self.active_player.get_rect_center())

	def is_near(self, max_distance=100): # Por enquanto, fixo para 1 arma
		"""
    	Verifica se o jogador ativo está próximo o suficiente de um item interagível.

    	Args:
    	    max_distance (float): Distância máxima para considerar interação.

    	Returns:
    	    bool: True se estiver perto, False caso contrário.
    	"""
		player_pos = pygame.math.Vector2(self.active_player.rect.centerx, self.active_player.rect.centery)
		item_pos = pygame.math.Vector2(self.weapon.rect.centerx, self.weapon.rect.centery)
		distance = player_pos.distance_to(item_pos)
		return distance <= max_distance
	
	def enemies_killed(self):
		"""
    	Verifica se todos os inimigos do nível foram derrotados.

    	Returns:
    	    bool: True se não houver inimigos vivos, False caso contrário.
    	"""
		for i in range(len(self.enemies)):
			if self.enemies[i].health > 0:
				return False
		return True

	def interact(self): # Por enquanto, fixo para 1 arma
		"""
    	Realiza a interação com o item do nível (atualmente, a arma).
    	"""
		if self.is_near(100):
			self.active_player.inventory.change_weapon(self.weapon)
			self.active_player.casting_cooldown = self.weapon.cooldown

	def draw_hearts(self, surface):
		"""
    	Desenha os corações de vida do jogador ativo no canto superior da tela.

    	Args:
    	    surface (pygame.Surface): Superfície onde os corações serão desenhados.
    	"""
		hearts = []
		for i in range(self.active_player.max_health):
			if i < self.active_player.health:
				hearts.append("full")  # Coração cheio
			else:
				hearts.append("empty")  # Coração vazio

		for i, heart_type in enumerate(hearts):
			x = 20 + i * (self.heart_size + self.heart_spacing)
			y = 20

			if heart_type == "full":
				surface.blit(self.heart_full, (x, y))
			else:
				surface.blit(self.heart_empty, (x, y))

	
	def nearest_door(self):
		"""
    	Retorna qual porta está mais próxima do jogador ativo.

    	Returns:
    	    int: 0 para porta esquerda, 1 para direita, -1 se nenhuma estiver próxima.
    	"""
		vec_player = pygame.Vector2(self.active_player.get_rect_center())
		vec_left = pygame.Vector2(self.leftDoor.rect.center)
		vec_right = pygame.Vector2(self.rightDoor.rect.center)

		if vec_player.distance_to(vec_left) < SCALE_FACTOR*TILESIZE/2:
			return 0
		elif vec_player.distance_to(vec_right) < SCALE_FACTOR*TILESIZE/2:
			return 1
		else:
			return -1			
		
	def set_players(self, player = 1):
		"""
    	Define qual jogador inicia como ativo.

    	Args:
    	    player (int): 1 para player1, 2 para player2.
    	"""
		#Selects active player
		if player == 1:
			self.active_player = self.player1
			self.inactive_player = self.player2
			self.player1.change_active(True)
			self.player2.set_transparency(GHOST_ALPHA)
		else:
		
			self.active_player = self.player2
			self.inactive_player = self.player1
			self.player2.change_active(True)
			self.player1.change_active(False)
			self.player1.set_transparency(GHOST_ALPHA)


	def run(self, state):
		"""
    	Atualiza o estado do jogo e renderiza os elementos visuais na tela.
	
    	Args:
    	    state (GameState): Estado atual do jogo (ex: GameState.PLAYING).
	
    	Returns:
    	    int: 0 ou 1 se porta estiver acessível (nível completo), -1 caso contrário.
    	"""
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