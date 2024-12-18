import math
from math import atan2, degrees
from time import time

import pygame
from pygame import Vector2
from pygame.font import FontType

from note import Note,Animation,init

import button
import random
from pygame_render import RenderEngine

pygame.init()

#create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CENTER = Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
engine = RenderEngine(SCREEN_WIDTH, SCREEN_HEIGHT,resizable=False)
curs, mask = pygame.cursors.compile(pygame.cursors.textmarker_strings, 'X', 'o')
pygame.mouse.set_cursor((8,16), (0, 0), curs, mask)
pygame.display.set_caption("Jeu de rythm")
clock = pygame.time.Clock()

#global game variables
debug = False
high_score = 0
game_paused = True
menu_state = "main"
main_menu_music = True
afficher_shooting_stars = False
fps = 60
start_time = (time() - int(time())) * 100
rotation = 0
current_score = 0
speed = 10
max_health = 50
health = max_health
damage = 5
shake = False
frame_count = 0
volume = 0.025

try:
  with open('save.super_cripte', 'r') as f :
    a = int(f.readline()[::-1], 2)/-23-50
    if a-int(a) != 0:
      menu_state = "cheat"
    print(a)
    high_score = int(a)
except FileNotFoundError:
  print("No save file found")

#load other module
init(fps,(CENTER.x,CENTER.y),engine)

#define fonts
font = pygame.font.Font("assets/textures/fonts/Chomsky.otf", 32)

#define colours
TEXT_COL = (60, 255, 7,255)

#load sounds
hurt_sound = pygame.mixer.Sound("assets/sounds/effects/hurt.mp3",)
explode_sound = pygame.mixer.Sound("assets/sounds/effects/explode.mp3",)
select_sound = pygame.mixer.Sound("assets/sounds/effects/select.mp3",)

button.init(select_sound,volume)

#define layer
menu_layer = engine.make_layer((SCREEN_WIDTH, SCREEN_HEIGHT))
note_layer = engine.make_layer((SCREEN_WIDTH, SCREEN_HEIGHT))
note_layer2 = engine.make_layer((SCREEN_WIDTH, SCREEN_HEIGHT))
main_screen_layer = engine.make_layer((SCREEN_WIDTH,SCREEN_HEIGHT))
shake_layer = engine.make_layer((SCREEN_WIDTH, SCREEN_HEIGHT))

#define Texture
blank_texture = engine.surface_to_texture(pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA))
perso = engine.load_texture("assets/textures/game/perso.png")
note = engine.load_texture("assets/textures/game/note.png")
health_bar = engine.surface_to_texture(pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT/20), pygame.SRCALPHA))

#define shader
shader_line = engine.load_shader_from_path('shader/vertex.glsl', 'shader/line.glsl')
shader_glitch = engine.load_shader_from_path('shader/vertex.glsl', 'shader/glitch.glsl')
shader_star = engine.load_shader_from_path('shader/vertex.glsl', 'shader/star.glsl')
shader_particle = engine.load_shader_from_path('shader/vertex.glsl', 'shader/particle.glsl')
shader_blend = engine.load_shader_from_path('shader/vertex.glsl', 'shader/blend.glsl')
clear_black = engine.load_shader_from_path('shader/vertex.glsl', 'shader/clear_black.glsl')
shader_health_bar = engine.load_shader_from_path('shader/vertex.glsl', 'shader/health.glsl')
shader_shake = engine.load_shader_from_path('shader/vertex.glsl', 'shader/shake.glsl')


#load button images
resume_img = pygame.image.load("assets/textures/GUI/main menu/Jouer.png").convert_alpha()
options_img = pygame.image.load("assets/textures/GUI/main menu/Paramètres.png").convert_alpha()
quit_img = pygame.image.load("assets/textures/GUI/main menu/quitter.png").convert_alpha()
audio_img = pygame.image.load('assets/textures/GUI/main menu/modifier le volume.png').convert_alpha()
back_img = pygame.image.load('assets/textures/GUI/main menu/retour.png').convert_alpha()
shooting_star_img = pygame.image.load('assets/textures/GUI/main menu/shooting_star.png').convert_alpha()
lines_img = pygame.image.load('assets/textures/GUI/lines.png')

#define note object
#Note(note, 100, 100, (0, 255, 0))

#load animation
slash = engine.load_texture("assets/textures/game/slash.png")

#generated text Surface
fullScreen_img = font.render("Fullscreen", True, TEXT_COL)
fullScreen_img = pygame.transform.scale(fullScreen_img, (int(fullScreen_img.get_width() * 1.6),
                                                       fullScreen_img.get_height()))
Game_Over_img = font.render("Game Over", True, TEXT_COL)
Game_Over_img = pygame.transform.scale(Game_Over_img, (int(Game_Over_img.get_width() * 2),
                                                       int(Game_Over_img.get_height()*1.5)))
game_over_text = engine.surface_to_texture(Game_Over_img)
Score_img = font.render("Score : "+str(current_score), True, TEXT_COL)
Score_img = pygame.transform.scale(Score_img, (int(Score_img.get_width() * 1.6),
                                                       Score_img.get_height()))
score_text = engine.surface_to_texture(Score_img)

high_score_text = None


#create button instances
resume_button = button.Button(CENTER.x, SCREEN_HEIGHT/3.2, resume_img, 1.5)
options_button = button.Button(CENTER.x, CENTER.y, options_img, 1.5)
quit_button = button.Button(CENTER.x, SCREEN_HEIGHT/1.42, quit_img, 1.5)
audio_button = button.Button(CENTER.x, SCREEN_HEIGHT/3.2, audio_img, 1.5)
full_button = button.Button(CENTER.x, CENTER.y, fullScreen_img, 1.5)
back_button = button.Button(CENTER.x, SCREEN_HEIGHT/1.42, back_img, 1.5)


def random_color() -> tuple[int,int,int]:
  levels = range(128, 256, 32)
  return tuple(random.choice(levels) for _ in range(3))

def update_high_score():
  global high_score, high_score_text
  high_score_img = font.render("High Score : " + str(high_score), True, TEXT_COL)
  high_score_img = pygame.transform.scale(high_score_img, (int(high_score_img.get_width() * 1.6),
                                                           high_score_img.get_height()))
  high_score_img = pygame.transform.rotate(high_score_img, -25)
  high_score_text = engine.surface_to_texture(high_score_img)

update_high_score()

def draw_text(message, font : FontType, text_col:tuple[int,int,int,int], x, y):
  img = font.render(message, True, text_col)
  engine.render(engine.surface_to_texture(img), engine.screen, (x-img.get_width()/2, y-img.get_height()/2))

def draw_main_menu():
  resume_button.draw(engine,menu_layer)
  options_button.draw(engine,menu_layer)
  quit_button.draw(engine,menu_layer)
  if high_score > 0:
    draw_texture_center(high_score_text, SCREEN_WIDTH/1.2, SCREEN_HEIGHT/3, menu_layer)


def draw_options_menu():
  audio_button.draw(engine,menu_layer)
  full_button.draw(engine,menu_layer)
  back_button.draw(engine,menu_layer)

def draw_game_over():
  draw_texture_center(game_over_text, CENTER.x, 240, menu_layer)
  draw_texture_center(score_text, CENTER.x, 360, menu_layer)
  back_button.draw(engine, menu_layer)

def draw_game():
  global note_layer
  global shake
  global frame_count
  if frame_count > 15:
    frame_count = 0
    shake=False
  main_layer = engine.screen
  if shake:
    frame_count += 1
    shake_layer.clear(0, 0, 0, 0)
    main_layer = shake_layer
  draw_text("Press SPACE to pause", font, TEXT_COL, SCREEN_WIDTH/8, SCREEN_HEIGHT/25)
  draw_text("Score : "+str(current_score), font, TEXT_COL, SCREEN_WIDTH /1.15, SCREEN_HEIGHT / 25)
  engine.render(perso, main_layer, (CENTER.x - perso.width / 2 * 2, CENTER.y - perso.height / 2 * 2), scale=2,
                angle=rotation)
  if shake:
    shader_shake['time'] = pygame.time.get_ticks()/100
    engine.render(shake_layer.texture, engine.screen, shader=shader_shake)

  Note.draw_all(engine, note_layer, shader=shader_particle)
  engine.render(note_layer.texture, note_layer2, shader=shader_blend)
  engine.render(note_layer2.texture, note_layer)
  note_layer2.clear(0, 0, 0, 0)
  engine.render(note_layer.texture, engine.screen, shader=clear_black)
  Note.draw_all(engine, engine.screen, shader=shader_particle)
  Note.move_to_all( 3)
  Animation.draw_all(engine, engine.screen)
  global health
  for note1 in Note.list_notes:
    if note1.get_pos().distance_to(Vector2(CENTER.x, CENTER.y)) < 3:
      note1.remove()
      health -= damage
      shake = True
      hurt_sound.set_volume(volume)
      hurt_sound.play()



  # draw health bar
  shader_health_bar['uv_size'] = health_bar.size
  shader_health_bar['health'] = health/max_health
  engine.render(health_bar, engine.screen, (SCREEN_WIDTH/1.4, SCREEN_HEIGHT/1.12),shader=shader_health_bar)

def draw_texture_center(texture, x, y,layers = None,shader = None):
  if layers is None:
    engine.render(texture, engine.screen, (x - texture.width/2, y - texture.height/2),shader=shader)
  else:
    engine.render(texture,layers, (x - texture.width/2, y - texture.height/2),shader=shader)


def update_layer_size():
  global menu_layer
  menu_layer = engine.make_layer((SCREEN_WIDTH, SCREEN_HEIGHT))


note_layer.clear(0, 0, 0, 0)
note_layer2.clear(0, 0, 0, 0)

pygame.mixer.music.load("assets/sounds/musics/main_menu.mp3")
pygame.mixer.music.set_volume(volume)

if main_menu_music:
  pygame.mixer.music.play(1000000)

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


  #player rotaion
  mousex,mousey = pygame.mouse.get_pos()
  rotation = degrees(-atan2(CENTER.x-mousex, CENTER.y-mousey))

  if pygame.mouse.get_pressed()[0] == 0:
    button.Button.can_click = True

  #update shader variables
  shader_glitch['time'] = start_time
  shader_line['time'] = pygame.time.get_ticks()
  shader_star['time'] = pygame.time.get_ticks()


  clock.tick(fps)
  t0 = time()

  engine.screen.clear(0, 22, 1,255)
  menu_layer.clear(0, 22, 1,0)



    #background
  engine.render(blank_texture, engine.screen, shader=shader_star)



  #check if game is paused
  if game_paused:
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
        #stop the music
        if main_menu_music:
          pygame.mixer.music.stop()
        else:
          pygame.mixer.music.play(1000000)
        main_menu_music = not main_menu_music
      if back_button.is_clicked():
        menu_state = "main"
      if full_button.is_clicked():
        #toggle fullscreen
        change_fullscreen = True
        #engine.render(engine.surface_to_texture(fullScreen_img), menu_layer, (640, 220))
    #engine.render(menu_layer.texture, engine.screen, shader=shader_glitch)

    if menu_state == "game over":
      draw_game_over()
      if back_button.is_clicked():
        menu_state = "main"
        current_score = 0

    if menu_state == "cheat":
      draw_text("Cheat detected", pygame.font.Font("assets/textures/fonts/Chomsky.otf", 64), TEXT_COL,
                SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

  else:
    #the Game is running

    draw_game()
    #check if the player clicked and spawn a slash animation
    if pygame.mouse.get_pressed()[0] and button.Button.can_click :
      button.Button.can_click = False
      # current_score += 1
      coord = Vector2(0, -65).rotate(rotation)
      anim = Animation(slash, CENTER.x+coord.x, CENTER.y+coord.y,
                15, 6, loop = False, scale = 3,rotation=rotation)
      if len(anim.collision()) == 0 and current_score > 0:
        current_score -= 1

    for animation in Animation.List_animations:
      # print([note_coord[0],note_coord[1],CENTER.x+coord.x,CENTER.y+coord.y])
      colision_list: list[(Note, int)] = animation.collision()
      if len(colision_list) != 0:
        for collision_result in colision_list:
          collision_result[0].remove()
          current_score += collision_result[1]
        explode_sound.set_volume(volume)
        explode_sound.play()



    #print(counter, current_score, speed, math.ceil(100-current_score/speed))
    if counter % (math.ceil(100-current_score/speed)) == 0:
      rot = random.random() * 360
      vec = Vector2(0, -1000).rotate(rot)
      color = random_color()
      Note(note, vec.x + SCREEN_WIDTH / 2, vec.y + SCREEN_HEIGHT / 2, color)

    if health <= 0:
      game_paused = True
      menu_state = "game over"
      high_score = max(high_score, current_score)

      #update the end screen Score
      Score_img = font.render("Score : " + str(current_score), True, TEXT_COL)
      Score_img = pygame.transform.scale(Score_img, (int(Score_img.get_width() * 2),
                                                     int(Score_img.get_height()*1.5)))
      score_text = engine.surface_to_texture(Score_img)

      #update the High Score image
      update_high_score()

      health = 100
      Note.list_notes.clear()
      Animation.List_animations.clear()
      note_layer2.clear(0, 0, 0, 0)
      note_layer.clear(0, 0, 0, 0)

      frame_count = 0
      shake = False

  #    main_menu_music = True

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
  if debug:
    pygame.display.set_caption(
      f'Rendering 1 sprites at {mspt:.3f} ms per tick!')

  counter += 1

with open('save.super_cripte', 'w') as f:
  f.write(f'{(high_score+50)*-23:b}'[::-1])
pygame.quit()