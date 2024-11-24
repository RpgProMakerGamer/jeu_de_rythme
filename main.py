from time import time, sleep

import pygame
from pygame.font import FontType

import button
import sprite
import random
from pygame_render import RenderEngine

pygame.init()

#create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
engine = RenderEngine(SCREEN_WIDTH, SCREEN_HEIGHT,resizable=False)
curs, mask = pygame.cursors.compile(pygame.cursors.textmarker_strings, 'X', 'o')
pygame.mouse.set_cursor((8,16), (0, 0), curs, mask)
pygame.display.set_caption("Jeu de rythm")
clock = pygame.time.Clock()

#game variables
game_paused = True
menu_state = "main"
main_menu_music = False
afficher_shooting_stars = False
fps = 60
start_time = (time() - int(time())) * 100

#define fonts
font = pygame.font.Font("assets/textures/fonts/Chomsky.otf", 32)

#define colours
TEXT_COL = (60, 255, 7,255)

#define layer
menu_layer = engine.make_layer((SCREEN_WIDTH, SCREEN_HEIGHT))

#define Texture
blank_texture = engine.surface_to_texture(pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA))

#define shader
shader_line = engine.load_shader_from_path('shader/vertex.glsl', 'shader/line.glsl')
shader_glitch = engine.load_shader_from_path('shader/vertex.glsl', 'shader/glitch.glsl')
shader_star = engine.load_shader_from_path('shader/vertex.glsl', 'shader/star.glsl')

#load button images
resume_img = pygame.image.load("assets/textures/GUI/main menu/Jouer.png").convert_alpha()
options_img = pygame.image.load("assets/textures/GUI/main menu/Paramètres.png").convert_alpha()
quit_img = pygame.image.load("assets/textures/GUI/main menu/quitter.png").convert_alpha()
audio_img = pygame.image.load('assets/textures/GUI/main menu/modifier le volume.png').convert_alpha()
back_img = pygame.image.load('assets/textures/GUI/main menu/retour.png').convert_alpha()
shooting_star_img = pygame.image.load('assets/textures/GUI/main menu/shooting_star.png').convert_alpha()
lines_img = pygame.image.load('assets/textures/GUI/lines.png')

#generated text Surface
fullScreen_img = font.render("Fullscreen", True, TEXT_COL)
fullScreen_img = pygame.transform.scale(fullScreen_img, (int(fullScreen_img.get_width() * 1.6),
                                                       fullScreen_img.get_height()))

#create button instances
resume_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/3.2, resume_img, 1.5)
options_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, options_img, 1.5)
quit_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/1.42, quit_img, 1.5)
audio_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/3.2, audio_img, 1.5)
full_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, fullScreen_img, 1.5)
back_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/1.42, back_img, 1.5)



# create sprite instances
if afficher_shooting_stars == True :
  shooting_star_sprt0 = sprite.Sprite(random.randrange(40,1280), 0, shooting_star_img, random.randrange(50,256), engine)
  shooting_star_sprt1 = sprite.Sprite(random.randrange(40,1280), 0, shooting_star_img, random.randrange(50,256), engine)
  shooting_star_sprt2 = sprite.Sprite(1280, random.randrange(700), shooting_star_img, random.randrange(50,256), engine)
  shooting_star_sprt3 = sprite.Sprite(1280, random.randrange(700), shooting_star_img, random.randrange(50,256), engine)


def draw_text(message, font : FontType, text_col:tuple[int,int,int,int], x, y):
  img = font.render(message, True, text_col)
  engine.render(engine.surface_to_texture(img), engine.screen, (x, y))

def draw_main_menu():
  resume_button.draw(engine,menu_layer)
  options_button.draw(engine,menu_layer)
  quit_button.draw(engine,menu_layer)

def draw_options_menu():
  audio_button.draw(engine,menu_layer)
  full_button.draw(engine,menu_layer)
  back_button.draw(engine,menu_layer)

def update_layer_size():
  global menu_layer
  menu_layer = engine.make_layer((SCREEN_WIDTH, SCREEN_HEIGHT))

change_fullscreen = False
counter = 0
#game loop
run = True
while run:
  if change_fullscreen :
    change_fullscreen = False
    if pygame.display.is_fullscreen():
      pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    else:
      pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
  shader_glitch['time'] = start_time
  shader_line['time'] = pygame.time.get_ticks()
  shader_star['time'] = pygame.time.get_ticks()


  clock.tick(fps)
  t0 = time()

  engine.screen.clear(0, 22, 1,255)
  menu_layer.clear(0, 22, 1,0)



  # main menu music player
  if main_menu_music == True:
    main_menu_music = False
    pygame.mixer.music.load("assets/sounds/musics/main_menu.mp3")
    pygame.mixer.music.set_volume(0.025)
    pygame.mixer.music.play()

  engine.render(blank_texture, engine.screen, shader=shader_star)
  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      draw_main_menu()

      #draw pause screen buttons
      if resume_button.is_clicked():
        game_paused = False
      if options_button.is_clicked():
        menu_state = "options"
      if quit_button.is_clicked():
        run = False
    #check if the options menu is open
    if menu_state == "options":
      draw_options_menu()
      #draw the different options buttons
      if audio_button.is_clicked():
        print("Audio Settings")
      if back_button.is_clicked():
        menu_state = "main"
      if full_button.is_clicked():
        #toggle fullscreen
        change_fullscreen = True
        print("click")
        #engine.render(engine.surface_to_texture(fullScreen_img), menu_layer, (640, 220))
    #engine.render(menu_layer.texture, engine.screen, shader=shader_glitch)
  else:
    #the Game is running
    draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)

  # draw shooting stars
  # /!\ problème avec l'opacité /!\
  if afficher_shooting_stars:
    for i in range(4):
      if locals()[f'shooting_star_sprt{i}'].x>-250 or locals()[f'shooting_star_sprt{i}'].y<720:
        locals()[f"shooting_star_sprt{i}"] = sprite.Sprite(locals()[f'shooting_star_sprt{i}'].x - 1.5, locals()[f'shooting_star_sprt{i}'].y + 1, shooting_star_img, 255, engine)
      else :
        if i < 2:
          locals()[f"shooting_star_sprt{i}"] = sprite.Sprite(random.randrange(40,1280), 0, shooting_star_img, random.randrange(50,256), engine)
          print(locals()[f"shooting_star_sprt{i}"].opacity)
        else :
          locals()[f"shooting_star_sprt{i}"] = sprite.Sprite(1280, random.randrange(700), shooting_star_img, random.randrange(50,256), engine)
          print(locals()[f"shooting_star_sprt{i}"].opacity)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.VIDEORESIZE:
      SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_window_size()
      update_layer_size()
      print("resize : ",SCREEN_WIDTH, SCREEN_HEIGHT)
      print("resize1 : ",menu_layer.size)
      print("resize2 : ", engine.screen.size)

  #print("resize : ", )

  #engine.render(engine.surface_to_texture(resume_img), menu_layer, (640, 220))

  engine.render(menu_layer.texture, engine.screen, shader=shader_glitch)


  # affichage des raies/lignes
  # lines_sprt = sprite.Sprite(0,0,lines_img,255,screen)
  engine.render(blank_texture, engine.screen, shader=shader_line)

  pygame.display.flip()

  # Display mspt
  t =time()
  start_time += (t - t0)

  mspt = (t - t0) * 1000

  pygame.display.set_caption(
    f'Rendering 1 sprites at {mspt:.3f} ms per tick!')
pygame.quit()


