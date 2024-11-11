import pygame as p

# p setup
p.init()
screen = p.display.set_mode((1280, 720))
p.display.set_caption("jeu_de_rythme")
# p.mouse.set_visible(False)
p.mouse.set_cursor(p.SYSTEM_CURSOR_CROSSHAIR)
clock = p.time.Clock()
running = True

# Starting the mixer 
p.mixer.init() 
main_menu = True  

while running:
    # poll for events
    # p.QUIT event means the user clicked X to close your window
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    # Check for the fullscreen toggle event
    if event.type == p.KEYDOWN and event.key == p.K_F11:
        # Toggle fullscreen mode
        p.display.toggle_fullscreen()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(( 0, 22, 1 ))

    if main_menu == True:
        main_menu = False
        p.mixer.music.load("assets\sounds\musics\main menu.mp3") 
        p.mixer.music.set_volume(0.5)
        p.mixer.music.play() 


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    p.display.flip()

    clock.tick(60)  # limits FPS to 60

p.quit()