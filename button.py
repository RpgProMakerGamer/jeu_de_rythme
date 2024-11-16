import pygame
from pygame_render import RenderEngine

import sprite

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self, surface:RenderEngine):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			#img = sprite.Sprite(self.rect.topleft[0]+20, self.rect.topleft[1]+20, self.image, 255,surface)
			#print("hover")
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.render(surface.surface_to_texture(self.image),surface.screen, (self.rect.x, self.rect.y))

		return action