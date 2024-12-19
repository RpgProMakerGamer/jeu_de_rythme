import pygame
from pygame import SurfaceType
from pygame.mixer import SoundType
from pygame_render import RenderEngine, Layer

volume = 0.5
select_sound : SoundType = None

def init(sound,vol):
    global select_sound
    global volume
    volume = vol
    select_sound = sound
#button class
class Button:

 can_click = True

 def __init__(self, x, y, image : SurfaceType, scale):
    width = image.get_width()
    height = image.get_height()
    self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

 def draw(self, surface:RenderEngine,layer : Layer = None):
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
      select_sound.set_volume(volume)
      select_sound.play()
      return True
    return False