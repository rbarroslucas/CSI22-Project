import pygame, sys
from settings import *
from render.level import Level
from interfaces.pause_menu import PauseMenu
from interfaces.main_menu import MainMenu
from interfaces.game_over import GameOverMenu
from game_states import GameState

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		self.surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
		pygame.display.set_caption('Bad Trip')
		self.clock = pygame.time.Clock()

		self.state = GameState.MAIN_MENU

		self.fade_img = pygame.Surface((WIDTH, HEIGTH)).convert_alpha()
		self.fade_img.fill((139, 0, 0))
		self.fade = self.fade_img.get_rect()
		self.fade_alpha = 255
		self.fade_speed = 2

		# soundtrack
		#pygame.mixer.init()
		#main_sound = pygame.mixer.Sound('./audio/main.ogg')
		#main_sound.set_volume(0.5)
		#main_sound.play(loops = -1)

		self.levels = [None]*4
		self.current_level = 0
		self.levels[self.current_level] = Level(f'./layouts/sala{self.current_level + 1}.tmx', False)
		self.level = self.levels[self.current_level]
		self.completed = [False for i in self.levels]

		self.pauseMenu = PauseMenu()
		self.mainMenu = MainMenu()
		self.gameOverMenu = GameOverMenu()

	def run(self):
		while True:
			# Handle events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				# Estado-agnostic events
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE and self.state in (GameState.PLAYING, GameState.PAUSED):
						self.state = GameState.PAUSED if self.state == GameState.PLAYING else GameState.PLAYING

				# State-specific events
				if self.state == GameState.MAIN_MENU:
					action = self.mainMenu.handle_event(event)
					if action == "new_game":
						self.state = GameState.PLAYING
						self.fade_alpha = 255
						self.fade_speed = 3
						self.set_levels()
					elif action == "quit":
						pygame.quit()
						sys.exit()

				elif self.state == GameState.PAUSED:
					action = self.pauseMenu.handle_event(event)
					if action == "continue":
						self.state = GameState.PLAYING
					elif action == "main_menu":
						self.state = GameState.MAIN_MENU

				elif self.state == GameState.GAME_OVER:
					action = self.gameOverMenu.handle_event(event)
					if action == "retry":
						self.state = GameState.PLAYING
						self.set_levels()

					elif action == "main_menu":
						self.state = GameState.MAIN_MENU
						self.set_levels()

			# Draw
			self.screen.fill('black')

			if self.level.is_game_over():
				self.state = GameState.GAME_OVER
			if self.state == GameState.MAIN_MENU:
				self.mainMenu.draw()
			elif self.state == GameState.GAME_OVER:
				self.gameOverMenu.draw()
			else:
				door = self.level.run(self.state)
				if door >= 0:
					self.completed[self.current_level] = True
					if door == 0 and self.current_level > 0:
						self.current_level -= 1
					elif self.current_level < 3:
						self.current_level += 1
						if self.levels[self.current_level] is None:
							self.levels[self.current_level] = Level(f'./layouts/sala{self.current_level+1}.tmx', False)

					self.level = self.levels[self.current_level]
					self.fade_alpha = 255
					self.fade_speed = 3

				if self.state == GameState.PAUSED:
					self.pauseMenu.draw()

			self.fade_img.set_alpha(self.fade_alpha)
			self.screen.blit(self.fade_img, self.fade)
			self.fade_alpha -= self.fade_speed
			pygame.display.update()
			self.clock.tick(FPS)

	def set_levels(self):
		self.levels = [None]*4
		self.current_level = 0
		self.levels[self.current_level] = Level(f'./layouts/sala{self.current_level+1}.tmx', False)
		self.level = self.levels[self.current_level]
		self.completed = [False for i in self.levels]
	
		

if __name__ == '__main__':
	game = Game()
	game.run()