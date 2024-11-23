from pygame_render import Layer,RenderEngine

#button class
class Sprite:
    def __init__(self, x, y, image, opacity, screen : RenderEngine):
        self.x = x
        self.y = y
        self.opacity = opacity
        temp = Layer(image.get_width(), image.get_height())
        screen.render(image, temp,(-self.x, -self.y))
        screen.render(image, temp, (0, 0))
        #print("show")
        #Layer.(opacity)



	

