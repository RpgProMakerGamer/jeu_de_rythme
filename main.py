from time import time

import pygame
from pygame.font import FontType

import button
import sprite
import random
from pygame_render import RenderEngine, Layer

pygame.init()

#create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
engine = RenderEngine(SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption("Jeu de rythm")
clock = pygame.time.Clock()

#game variables
game_paused = True
menu_state = "main"
main_menu_music = True
afficher_shooting_stars = False
fps = 60

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (60, 255, 7)

#define Texture
line_texture = engine.surface_to_texture(pygame.Surface((1280, 720), pygame.SRCALPHA))

#define shader
shader_line = engine.load_shader_from_path('shader/vertex.glsl', 'shader/line.glsl')

#load button images
resume_img = pygame.image.load("assets/textures/GUI/main menu/Jouer.png").convert_alpha()
options_img = pygame.image.load("assets/textures/GUI/main menu/Paramètres.png").convert_alpha()
quit_img = pygame.image.load("assets/textures/GUI/main menu/quitter.png").convert_alpha()
audio_img = pygame.image.load('assets/textures/GUI/main menu/modifier le volume.png').convert_alpha()
back_img = pygame.image.load('assets/textures/GUI/main menu/retour.png').convert_alpha()
shooting_star_img = pygame.image.load('assets/textures/GUI/main menu/shooting_star.png').convert_alpha()
lines_img = pygame.image.load('assets/textures/GUI/lines.png')

#create button instances
resume_button = button.Button(640, 220, resume_img, 1.5)
options_button = button.Button(640, 360, options_img, 1.5)
quit_button = button.Button(640, 500, quit_img, 1.5)
audio_button = button.Button(640, 310, audio_img, 1.5)
back_button = button.Button(640, 410, back_img, 1.5)

# create sprite instances
if afficher_shooting_stars == True :
  shooting_star_sprt0 = sprite.Sprite(random.randrange(40,1280), 0, shooting_star_img, random.randrange(50,256), engine)
  shooting_star_sprt1 = sprite.Sprite(random.randrange(40,1280), 0, shooting_star_img, random.randrange(50,256), engine)
  shooting_star_sprt2 = sprite.Sprite(1280, random.randrange(700), shooting_star_img, random.randrange(50,256), engine)
  shooting_star_sprt3 = sprite.Sprite(1280, random.randrange(700), shooting_star_img, random.randrange(50,256), engine)


def draw_text(text, test : FontType, text_col, x, y):
  img = test.render(text, True, text_col)
  engine.render(engine.surface_to_texture(img), engine.screen, (x, y))
  

#game loop
run = True
while run:



  clock.tick(fps)
  t0 = time()

  engine.screen.clear(0, 22, 1,255)

  # main menu music player
  if main_menu_music == True:
    main_menu_music = False
    pygame.mixer.music.load("assets/sounds/musics/main_menu.mp3")
    pygame.mixer.music.set_volume(0.025)
    pygame.mixer.music.play() 

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if resume_button.draw(engine):
        game_paused = False
      if options_button.draw(engine):
        menu_state = "options"
      if quit_button.draw(engine):
        run = False
    #check if the options menu is open
    if menu_state == "options":
      #draw the different options buttons
      if audio_button.draw(engine):
        print("Audio Settings")
      if back_button.draw(engine):
        menu_state = "main"
  else:
    draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)

  # draw shooting stars
  # /!\ problème avec l'opacité /!\
  if afficher_shooting_stars == True :
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

  # affichage des raies/lignes
  # lines_sprt = sprite.Sprite(0,0,lines_img,255,screen)

  engine.render(line_texture,engine.screen,shader=shader_line)

  pygame.display.flip()

  # Display mspt
  t = time()
  mspt = (t - t0) * 1000

  pygame.display.set_caption(
    f'Rendering 1 sprites at {mspt:.3f} ms per tick!')
pygame.quit()