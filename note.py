import math

import pygame
from moderngl import Texture
from pygame import Vector2
from pygame_render import RenderEngine, Layer, Shader

Center = (0,0)
red_circle : Texture = pygame.Surface((4, 4), pygame.SRCALPHA)
pygame.draw.circle(red_circle, (255, 0, 0), (2, 2), 2)


def init(fps1,center,eng):
  Animation.FPS = fps1
  global Center
  global red_circle
  Center = center
  engine = eng
  red_circle = engine.surface_to_texture(red_circle)




class Note:

  list_notes : list = []

  def __init__(self, texture:Texture, x,y,color:tuple[int,int,int]):
    self.texture = texture
    self._x = x
    self._y = y
    self.color = color
    self.normal = Vector2(Center[0] - self._x, Center[1] - self._y).normalize()
    self.to = Vector2(Center[0], Center[1])
    self.rotation = math.degrees(math.atan2(self.normal.y, self.normal.x))
    Note.list_notes.append(self)

  def set_pos(self, x : int ,y :int ) -> None:
    self._x = x
    self._y = y

  def move(self, x : float ,y :float ) -> None:
    self._x += x
    self._y += y

  def move_to(self,dist : float, x : float = None ,y :float = None ) -> None:
    if x and y :
      self.to = Vector2(x,y)
      self.normal = Vector2(self.to.x - self._x, self.to.y - self._y).normalize()
      self.rotation = math.degrees(math.atan2(self.normal.y, self.normal.x))
    self._x += self.normal.x * dist
    self._y += self.normal.y * dist

  def get_pos(self) -> Vector2:
    return Vector2(self._x,self._y)

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  def remove(self):
    try:
      Note.list_notes.remove(self)
    except:
      pass


  def draw(self,engine : RenderEngine , layer:Layer = None, shader: Shader = None):
    if shader is not None:
      shader['pixel_color'] = (self.color[0]/255,self.color[1]/255,self.color[2]/255)
    if layer is None:
      engine.render(self.texture, engine.screen, (self.x-self.texture.width/2, self.y-self.texture.height/2),
                    shader=shader,angle=self.rotation)
    else :
      engine.render(self.texture, layer, (self.x-self.texture.width/2, self.y-self.texture.height/2),
                    shader=shader,angle=self.rotation)
    #engine.render(red_circle, engine.screen, (self.x-self.texture.width/2, self.y-self.texture.height/2))

  def draw_all(engine : RenderEngine, layer:Layer = None, shader: Shader = None):
    for note in Note.list_notes:
      note.draw(engine,layer,shader)

  def move_to_all( dist : float, x : float = None ,y :float = None) -> None:
    if x and y :
      for note in Note.list_notes:
        note.move_to(dist,x,y)
    else :
      for note in Note.list_notes:
        note.move_to(dist)

  def collision(self,cursor_x,cursor_y):
      r = 16 #/!\ ←— mettre la moitié de la longueur du côté de la note (height//2)
      d = (cursor_x - self.x)**2 + (cursor_y - self.y)**2
      if d < r**2:
          score = int(r - d ** 0.5)
          return True,int(score/3)+5
      return False,None

class Animation:
  FPS= 60
  List_animations = []

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
    Animation.List_animations.append(self)

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

  def draw_all(engine :RenderEngine, layer:Layer = None, shader: Shader = None):
    for anim in Animation.List_animations:
      anim.draw(engine,layer,shader)

  def draw(self, engine:RenderEngine, layer:Layer = None, shader: Shader = None):
    if self.current_frame >= self.max_frame-1 :
      if self.loop :
        self.current_frame = 0
      else :
        Animation.List_animations.remove(self)
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
    #engine.render(red_circle, engine.screen, (self.x-(self.textures.height/2), self.y-(self.width/2)))

  def collision(self):
    liste = []
    for note in Note.list_notes:
      collide,score = note.collision(self.x,self.y)
      if collide:
        liste.append((note,score))
    return liste

