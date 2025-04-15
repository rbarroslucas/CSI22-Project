import pygame, sys
from settings import *
from render.level import Level
from interfaces.pause_menu import PauseMenu
from interfaces.main_menu import MainMenu

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		self.surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
		pygame.display.set_caption('Bad Trip')
		self.clock = pygame.time.Clock()

		self.paused = False
		self.inMainMenu = True

		self.level = Level()
		self.pauseMenu = PauseMenu()
		self.mainMenu = MainMenu()

	def run(self):
		while True: # Para adicionar qualquer novo evento, lembre-se de colocar "if not self.paused"
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.paused = not self.paused
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if self.inMainMenu:  # Menu principal
						action = self.mainMenu.handle_event(event)
						if action == "new_game":
							self.inMainMenu = False
						elif action == "continue":
							pass
							# if hasattr(self.level, 'has_progress'):
							#	self.inMainMenu = True
						elif action == "options":
							pass
							# print("Abrir opções")
						elif action == "quit":
							pygame.quit()
							sys.exit()
					elif self.paused:  # Menu de pausa
						action = self.pauseMenu.handle_event(event)
						if action == "continue":
							self.paused = False
						elif action == "options":
							pass
							# print("Abrir opções de pausa")
						elif action == "main_menu":
							self.inMainMenu = True
							self.paused = False

			self.screen.fill('black')
      pygame.display.get_surface().fill('black')
      
			if self.inMainMenu:
				self.mainMenu.draw()
			else:
				self.level.run(self.paused)
				if self.paused:
					self.pauseMenu.draw()
          
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()