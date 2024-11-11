import pygame as p

# p setup
p.init()
screen = p.display.set_mode((1280, 720))
clock = p.time.Clock()
running = True

while running:
    # poll for events
    # p.QUIT event means the user clicked X to close your window
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    p.display.flip()

    clock.tick(60)  # limits FPS to 60

p.quit()
