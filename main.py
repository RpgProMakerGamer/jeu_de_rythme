import pygame
import button
import sprite
import random

pygame.init()

#create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu de rythm")
clock = pygame.time.Clock()

#game variables
game_paused = True
menu_state = "main"
main_menu_music = True
fps = 60

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (60, 255, 7)

#load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()
shooting_star_img = pygame.image.load('assets/textures/GUI/main menu/shooting_star.png').convert_alpha()

#create button instances
resume_button = button.Button(304, 125, resume_img, 1)
options_button = button.Button(297, 250, options_img, 1)
quit_button = button.Button(336, 375, quit_img, 1)
video_button = button.Button(226, 75, video_img, 1)
audio_button = button.Button(225, 200, audio_img, 1)
keys_button = button.Button(246, 325, keys_img, 1)
back_button = button.Button(332, 450, back_img, 1)

# create sprite instances
shooting_star_sprt0 = sprite.Sprite(random.randrange(40,1280), 0, shooting_star_img, random.randrange(50,256), screen)
shooting_star_sprt1 = sprite.Sprite(random.randrange(40,1280), 0, shooting_star_img, random.randrange(50,256), screen)
shooting_star_sprt2 = sprite.Sprite(1280, random.randrange(700), shooting_star_img, random.randrange(50,256), screen)
shooting_star_sprt3 = sprite.Sprite(1280, random.randrange(700), shooting_star_img, random.randrange(50,256), screen)
# print(shooting_star_sprt0.x)
# print(locals()[f'shooting_star_sprt{0}'].x)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))


depop=0
#game loop
run = True
while run:

  screen.fill(( 0, 22, 1 ))

  # main menu music player
  if main_menu_music == True:
    main_menu_music = False
    pygame.mixer.music.load("assets\sounds\musics\main menu.mp3") 
    pygame.mixer.music.set_volume(0.025)
    pygame.mixer.music.play() 

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if resume_button.draw(screen):
        game_paused = False
      if options_button.draw(screen):
        menu_state = "options"
      if quit_button.draw(screen):
        run = False
    #check if the options menu is open
    if menu_state == "options":
      #draw the different options buttons
      if video_button.draw(screen):
        print("Video Settings")
      if audio_button.draw(screen):
        print("Audio Settings")
      if keys_button.draw(screen):
        print("Change Key Bindings")
      if back_button.draw(screen):
        menu_state = "main"
  else:
    draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)

  # draw shooting stars
  # /!\ problème avec l'opacité /!\
  for i in range(4):
    if locals()[f'shooting_star_sprt{i}'].x>-250 or locals()[f'shooting_star_sprt{i}'].y<720:
      locals()[f"shooting_star_sprt{i}"] = sprite.Sprite(locals()[f'shooting_star_sprt{i}'].x-1.5, locals()[f'shooting_star_sprt{i}'].y+1, shooting_star_img, 255, screen)
    else :
      if i < 2:
        locals()[f"shooting_star_sprt{i}"] = sprite.Sprite(random.randrange(40,1280), 0, shooting_star_img, random.randrange(50,256), screen)
        print(locals()[f"shooting_star_sprt{i}"].opacity)
      else :
        locals()[f"shooting_star_sprt{i}"] = sprite.Sprite(1280, random.randrange(700), shooting_star_img, random.randrange(50,256), screen)
        print(locals()[f"shooting_star_sprt{i}"].opacity)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()
  clock.tick(fps)
pygame.quit()