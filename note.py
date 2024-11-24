import pygame
from moderngl import Texture
from pygame_render import RenderEngine, Layer, Shader



class Note:
  def __init__(self, texture:Texture, x,y,color:tuple[int,int,int,int]):
    self.texture = texture
    self._x = x
    self._y = y
    self.color = color

  def set_pos(self, x : int ,y :int ) -> None:
    self._x = x
    self._y = y

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y


  def draw(self, engine:RenderEngine, layer:Layer = None, shader: Shader = None):
    if shader is not None:
      shader['pixel_color'] = self.color
    if layer is None:
      engine.render(self.texture, engine.screen, (self.x, self.y),shader=shader)
    else :
      engine.render(self.texture, engine.screen, (self.x, self.y),shader=shader)

class Animation:
  FPS= 60

  def __init__(self, textures: Texture, x, y, fps: int,frame : int,loop: bool = True,scale:int = 1,rotation : float = 0):
    self.textures = textures
    self._x = x
    self._y = y
    self.fps = fps
    self.max_frame = frame
    self.frame_counter = 0
    self._current_frame = 0
    self.width = textures.width//frame
    self.loop = loop
    self.scale = scale
    self.rotation = rotation
    from main import fps
    Animation.FPS = fps

  def set_pos(self, x : float ,y :float ) -> None:
    self._x = x
    self._y = y

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @property
  def current_frame(self):
    return self._current_frame

  @current_frame.setter
  def current_frame(self, value):
    self._current_frame = value

  def start(self):
    self.current_frame = 0
    if self.frame_counter == self.fps:
      self.current_frame += 1
      self.frame_counter = 0

  def draw(self, engine:RenderEngine, layer:Layer = None, shader: Shader = None,rotation : float = 0):
    if self.current_frame >= self.max_frame-1 :
      if self.loop :
        self.current_frame = 0
      else :
        return
    if self.frame_counter >= Animation.FPS/self.fps:
      self.current_frame += 1
      self.frame_counter = 0
    if layer is None:
      engine.render(self.textures, engine.screen, (self.x-(self.textures.height/2)*self.scale,
                                                   self.y-(self.width/2)*self.scale),
                    shader=shader,
                    section=pygame.Rect(
        self.current_frame*self.width,0,self.width,self.textures.height),scale=self.scale,angle=self.rotation)
    else :
      engine.render(self.textures, layer, (self.x-(self.textures.height/2)*self.scale,
                                                   self.y-(self.width/2)*self.scale) ,
                    shader=shader,section=pygame.Rect(
        self.current_frame*self.width,0,self.width,self.textures.height),scale=self.scale,angle=self.rotation)
    self.frame_counter += 1
