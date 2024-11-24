import pygame
from pygame import SurfaceType
from pygame_render import RenderEngine, Layer

import sprite

#button class
class Button:

 can_click = True

 def __init__(self, x, y, image : SurfaceType, scale):
    width = image.get_width()
    height = image.get_height()
    self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.clicked = False

 def draw(self, surface:RenderEngine,layer : Layer = None):
    if pygame.mouse.get_pressed()[0] == 0:
      Button.can_click = True
    #draw button on the layer
    if layer is not None:
      surface.render(surface.surface_to_texture(self.image),layer, (self.rect.x, self.rect.y))
    else : surface.render(surface.surface_to_texture(self.image),surface.screen, (self.rect.x, self.rect.y))

 def is_hover(self):
    pos = pygame.mouse.get_pos()
    return self.rect.collidepoint(pos)

 def is_clicked(self):
    if self.is_hover() and pygame.mouse.get_pressed()[0] == 1 and Button.can_click:
      Button.can_click = False
      return True
    return False