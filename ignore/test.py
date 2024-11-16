from random import randrange
from time import time
import pygame
from moderngl import Texture
from pygame_render import RenderEngine


# Initialize pygame
pygame.init()

# Create a render engine
width, height = 1280, 720
engine = RenderEngine(width, height)

# Load texture
tex = engine.load_texture('sprite.png')

# Clock
clock = pygame.time.Clock()

# Positions
num_sprites = 1
positions = [(50,50) for _ in range(num_sprites)]

# Load shader
shader_glow = engine.load_shader_from_path('vertex.glsl', 'fragment_glow.glsl')
surface = pygame.SurfaceType((width, height))
surface.fill((64, 200, 64))
background =engine.surface_to_texture(surface)
# Main game loop
running = True
total_time = 0
while running:
    # Tick the clock at 60 frames per second
    clock.tick(60)
    t0 = time()

    # Clear the screen
    engine.clear(64, 0, 64)

    # Update the time
    total_time += clock.get_time()

    rand = randrange(200)

    # Send time uniform to glow shader
    shader_glow['time'] = total_time
    shader_glow['rand'] = rand


    engine.render(background, engine.screen, shader=shader_glow)
    # Render texture to screen
    angle = 0
    for p in positions:
        engine.render(tex, engine.screen,
                      position=p, scale=16., angle=angle, shader=shader_glow)


    # Update the display
    pygame.display.flip()

    # Display mspt
    t = time()
    mspt = (t-t0)*1000

    pygame.display.set_caption(
        f'Rendering {num_sprites} sprites at {mspt:.3f} ms per tick!')

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False