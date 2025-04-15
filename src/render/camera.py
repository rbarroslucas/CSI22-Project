import pygame
from settings import *


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		# general setup
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def set_floor(self, floor_surf):
		self.floor_surf = floor_surf
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self, main, second, post, post_surface):
		# getting the offset
		self.offset.x = main.rect.centerx - self.half_width
		self.offset.y = main.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)

		# lighting
		for sprite in post.sprites():
			if sprite.target == 'main':
				image = sprite.image
				post_surface.blit(sprite.image, (self.half_width - image.get_width()/2, self.half_height - image.get_height()/2))
			elif sprite.target == 'none':
				image = sprite.image
				post_surface.blit(sprite.image, (sprite.rect.topleft - self.offset))
			elif sprite.target == 'ghost':
				offset_pos = second.rect.center - self.offset - pygame.math.Vector2(sprite.rect.width/2, sprite.rect.height/2)
				image = sprite.image
				post_surface.blit(sprite.image, offset_pos)


		self.display_surface.blit(post_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)