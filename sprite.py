import pygame

#button class
class Sprite():
    def __init__(self, x, y, image, opacity, screen):
        # width = image.get_width()
        # height = image.get_height()
        # self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        # self.image.set_alpha(opacity) 
        # self.rect = self.image.get_rect()
        # self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.opacity = opacity
        temp = pygame.Surface((image.get_width(), image.get_height())).convert()
        temp.blit(screen, (-self.x, -self.y))
        temp.blit(image, (0, 0))
        temp.set_alpha(opacity)        
        screen.blit(temp, (self.x,self.y))


	

