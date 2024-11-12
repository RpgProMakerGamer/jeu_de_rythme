import pygame
import button

# p setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("jeu_de_rythme")
# pygame.mouse.set_visible(False)
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
clock = pygame.time.Clock()
running = True

# Starting the mixer 
pygame.mixer.init() 
main_menu = True  

# initialisation de l'image des boutons
jouer_img = pygame.image.load('Jouer.png').convert_alpha()

# création des instances de boutons
jouer_btn = button.Button(640, 260, jouer_img, 1.2)

while running:
    clock.tick(60)  # limits FPS to 60
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    if main_menu == False:
        screen.fill(( 0, 22, 1 ))
    else :
        screen.fill(( 78, 22, 1 ))

    # Check for the fullscreen toggle event
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
        # Toggle fullscreen mode
        pygame.display.toggle_fullscreen()

    # main menu music player
    if main_menu == True:
        main_menu = False
        pygame.mixer.music.load("assets\sounds\musics\main menu.mp3") 
        pygame.mixer.music.set_volume(0.025)
        pygame.mixer.music.play() 

    if jouer_btn.draw(screen):
        print('Jouer')
        main_menu = 'Maybe'
        # + il faut faire disparaitre le bouton 


    # Update the game state
    pygame.display.update()

    # flip() the display to put your work on screen
    pygame.display.flip()


pygame.quit()