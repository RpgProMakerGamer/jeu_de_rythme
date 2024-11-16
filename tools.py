import pygame
import math
import os
WHITE = (255,255,255)

pygame.mixer.init()
#click_sound = pygame.mixer.Sound(os.path.join('../../Desktop/python nsi/filtre_project/Assets', 'click.wav'))
#click_sound.set_volume(0.8)
#all class for graphique elements

class element():
  def __init__(self,x:float,y:float):
    self.x = x
    self.y = y
    
  def affiche(self,WIN):
    pass


#class for put somme text in the screen
class texte:
  def initialisation(self):
    self.bold = False
    self.italic = False
    self.underline = False
    
  def __init__(self,text:list,x:float,y:float,scale:float,color:tuple=(255,255,255),space:float=0)->None:
    '''
    permet d'afficher du texte sur l'écran
    
    :param text: list de str : le texte à afficher. (affiche ligne par ligne les éléments de la liste)
    '''
    self.text_x = x
    self.text_y = y
    self.scale = scale
    self.text = text
    self.text_color = color
    self.space = space
    self.normal_font = pygame.font.SysFont('comicsans', self.scale)
    self.initialisation()
  
  
  def affiche(self,WIN):
    NORMAL_FONT = self.normal_font
    dist = len(self.text)
    
     #set the font style
    NORMAL_FONT.set_bold(self.bold)
    NORMAL_FONT.set_italic(self.italic)
    NORMAL_FONT.set_underline(self.underline)
    
    for i in range(dist) :
      
      text_font = NORMAL_FONT.render(self.text[i], 1, self.text_color)
      #get the distance between the text
      dist_height = text_font.get_height()/2+self.space
      #relly complexe formul for juste put some text in the middle of the screen
      WIN.blit(text_font,
           (self.text_x - text_font.get_width() / 2, self.text_y - ((dist_height * dist)/2 - dist_height*i) - (text_font.get_height()/4-self.space)))
      
      #debug thing
      #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
      #print(self.y - ((dist_height * dist)/2 - dist_height*i)," : ",dist_height," : ",text_font.get_height()," : ",(dist_height * dist)/2)
      
  def set_bold(self,b:bool):
    self.bold = b
    
  def set_italic(self,i:bool):
    self.italic = i
    
  def set_underline(self,u:bool):
    self.underline = u
    
  def add_line(self,text):
    self.text.append(text)
    
class button_template:
  can_click = True
  def __init__(self,cord:tuple[int,int],scale:int,color:tuple[int,int,int],border_width:int=0,border_color:tuple[int,int,int]=(0,0,0)):
      '''make the base variable for all button :
      self.scale: int  : the size of the button
      self.color: tuple[int,int,int] : the color of the button
      self.x: int : the x position of the button
      self.y: int : the y position of the button
      self.border_width : the width of the border
      self.border_color : the color of the border
      self.is_click : if the button is clicked
      '''
      
      self.scale = scale
      self.color = color
      self.x = cord[0]
      self.y = cord[1]
      self.border_width = border_width
      self.border_color = border_color
      self.is_click = False
      
  def affiche(self,WIN):
    pass
  
  def mouseHover(self) -> bool:
    pass
  
  def click(self) -> bool:
    pass
  



class cir_button(button_template):
  def __init__(self,cord:tuple,scale,color,border_width=0,border_color=(0,0,0)):
    super().__init__(cord,scale,color,border_width,border_color)
    self.size = scale
    self.color = color
    self.x = cord[0]
    self.y = cord[1]
    self.border_width = border_width
    self.border_color = border_color
      
  def affiche(self,WIN):
    pygame.draw.circle(WIN, self.color, (self.x,self.y), self.size)
    if self.border_width != 0 :
      pygame.draw.circle(WIN, self.border_color, (self.x,self.y), self.size,self.border_width)
    if not pygame.mouse.get_pressed()[0]:
      button_template.can_click = True
    #debug thing
    #pygame.draw.circle(WIN, (255,255,0), (self.x, self.y), 10)
      
  def mouseHover(self) -> bool:
    if math.dist((self.x,self.y), pygame.mouse.get_pos()) <= self.scale :
      return True
    return False
  
  def click(self) -> bool:
    if self.mouseHover() and pygame.mouse.get_pressed()[0] and self.can_click:
      button_template.can_click = False
      #click_sound.play()
      return True
    return False
  
class rectangle(element):
  
    def __init__(self,cord:tuple,scale:tuple,color:tuple,border_width:float=0,border_color:tuple=(0,0,0),smooth_corner:int=0):
        super().__init__(cord[0],cord[1])
        self.scale = scale
        self.color = pygame.Color(color)
        self.color.a = 10
        self.x = cord[0]
        self.y = cord[1]
        #print(color)
        self.border_width = border_width
        self.border_color = border_color
        self.smooth_corner = smooth_corner
        if isinstance(scale, int):
          self.recwidth = scale
          self.recheight = scale
        elif isinstance(scale, tuple) and len(scale) == 2:  # Vérifier si scale est une tuple de longueur 2
            self.recwidth = scale[0]
            self.recheight = scale[1]
        else:
            raise ValueError("L'échelle (scale) doit être un entier ou un tuple de deux entiers (largeur, hauteur).")
      
    def affiche(self,WIN):
      pygame.draw.rect(WIN, self.color ,pygame.Rect(self.x-self.recwidth/2,self.y-self.recheight/2,self.recwidth,self.recheight),0,self.smooth_corner)
      if self.border_width != 0 :
        pygame.draw.rect(WIN, self.border_color ,pygame.Rect(self.x-self.recwidth/2,self.y-self.recheight/2,self.recwidth,self.recheight),self.border_width,self.smooth_corner)
    

# make a simple rectangle button with a color and a scale
class rect_button(button_template):
    can_click = True
    def __init__(self,cord:tuple,scale,color,border_width=0,border_color=(0,0,0),transparent =False):
        if isinstance(scale, int):
          self.recwidth = scale
          self.recheight = scale
        elif isinstance(scale, tuple) and len(scale) == 2:  # Vérifier si scale est une tuple de longueur 2
            self.recwidth = scale[0]
            self.recheight = scale[1]
        else:
            raise ValueError("L'échelle (scale) doit être un entier ou un tuple de deux entiers (largeur, hauteur).")
        super().__init__(cord,scale,color,border_width,border_color)
        self.transparent = transparent
      
    def affiche(self,WIN):
      #print(self.color)
      if not self.transparent :
        pygame.draw.rect(WIN, self.color ,pygame.Rect(self.x-self.recwidth/2,self.y-self.recheight/2,self.recwidth,self.recheight))
      if self.border_width != 0 :
        pygame.draw.rect(WIN, self.border_color ,pygame.Rect(self.x-self.recwidth/2,self.y-self.recheight/2,self.recwidth,self.recheight),self.border_width)
      if not pygame.mouse.get_pressed()[0]:
        rect_button.can_click = True
      self.is_click = False
      self.click()
        
      #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
        
        
    def mouseHover(self) -> bool:
      mouseX = pygame.mouse.get_pos()[0]
      mouseY = pygame.mouse.get_pos()[1]
      #print(self.x-self.width/2," : ",self.x+self.width/2," : ", mouseX," : ",self.x-self.width/2 <= mouseX ," : ", self.x+self.width/2 >= mouseX)
      if self.x-self.recwidth/2 <= mouseX and self.x+self.recwidth/2 >= mouseX and self.y-self.recheight/2 <= mouseY and self.y+self.recheight/2 >= mouseY :
        return True
      else : return False
      
    def click(self) -> bool:
      #print(self.mouseHover() , pygame.mouse.get_pressed()[0] , self.can_click)
      if self.mouseHover() and pygame.mouse.get_pressed()[0] and self.can_click:
        rect_button.can_click = False
        self.is_click = True
        #click_sound.play()
        return True
      else : return False
      
      
class cir_text_button(cir_button,texte):
  
  def __init__(self,text:str, cord: tuple, scale : float, color,text_scale = 0, border_width=0, border_color=(0, 0, 0)):
    
    
    if color[0]+color[1]+color[2] > 382 :
        self.text_color = (0,0,0)
    else :
        self.text_color = (255,255,255)
        
    if text_scale == 0:
      text_scale = scale
    texte.__init__(self, text, cord[0], cord[1]-text_scale/8, text_scale, self.text_color)
    
    self.size = scale
    if text_scale == 0:
      text_height = 0
      for text in self.text:
        render = self.normal_font.render(text,1,color)
        heigth =render.get_height()/1.4
        #print(render.get_width(),":",render.get_height(),":",scale)
        if render.get_width() > self.size:
          self.size = render.get_width()
        text_height += heigth
        if text_height > self.size:
          self.size = text_height
        
    cir_button.__init__(self, cord, self.size, color, border_width, border_color)
    
  def affiche(self,WIN):
    cir_button.affiche(self,WIN)
    texte.affiche(self,WIN)
    
  def change_text(self,text):
      self.text = text
      
# make a button with a text in the middle      
class text_button(rect_button,texte):
    def __init__(self,text:list,coord:tuple,scale:int | tuple,color:tuple,width:int=0,height:int=0,border_width=0,
                 border_color=(0,0,0),transparent = False):
        if isinstance(scale, int):
          scale = (scale,scale)
        rect_button.__init__(self,coord,scale,color,border_width,border_color,transparent)
        
        if color[0]+color[1]+color[2] > 500 :
          self.text_color = (0,0,0)
        else :
          self.text_color = (255,255,255)
        
        texte.__init__(self,[text],coord[0],coord[1]-scale[1]/8,scale[1],self.text_color)
        
        
        self.cwidth = width
        self.cheight = height
        self.max_text_width = 0
        self.text_height = 0
        for text in self.text:
          if self.normal_font.render(text,1,0).get_width() > self.max_text_width:
            self.max_text_width = self.normal_font.render(text,1,0).get_width()
          self.text_height += self.normal_font.render(text,1,0).get_height()
        self.width = self.max_text_width+20+self.cwidth
        self.height = self.text_height+10+self.cheight
        self.recheight = self.height
        self.recwidth = self.width
        
      
    def affiche(self,WIN):
      rect_button.affiche(self,WIN)
      texte.affiche(self,WIN)
      
      #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
      
    def change_text(self,text):
      self.text = text
      
# make a button with a image
class button_image:
    def __init__(self,image,x,y,scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.image = pygame.transform.scale(image,scale)
      
    def affiche(self,WIN):
      WIN.blit(self.image,(self.x-self.scale[0]/2,self.y-self.scale[1]/2))

    def mouseHover(self):
      if math.dist((self.x+self.scale[0]/2,self.y+self.scale[1]/2), pygame.mouse.get_pos()) <= self.scale[0]/2 :
        return True
      else : return False
      
    def set_image(self,image):
      self.image = pygame.transform.scale(image,self.scale)
      
class array_button(button_template):
    def __init__(self,text:list[list],coord:tuple[float,float],scale:int,color:tuple[int,int ,int],width:int=0,height:int=0,border_width:int=0,border_color:tuple[int,int ,int]=(255,255,255)):
      
      #initialise the base color of the button
      self.custom_color = color
      #the number of button
      n_button = len(text)
      self.n_button = n_button
      #test if the color is a tuple or a liste of tuple for each button
      if isinstance(color,tuple) or len(color) != n_button:
        self.custom_color = [color for i in range(n_button)]
      #initialise the button list
      self.button = []
      #initialise the button_template 
      super().__init__(coord,scale,color,border_width,border_color)
      #the width of all button
      self.max_width = 0
      #create all the button and get which have the greatest width
      for i in range(n_button):
        self.button.append(text_button(text[i],coord,scale,self.custom_color[i],width,height,border_width,border_color))
        #print(self.button[i].width,self.button[i].normal_font.render(text[i],1,color).get_width())
        if self.button[i].width > self.max_width:
          self.max_width = self.button[i].width
          
      #get the greatest height of the button
      self.max_height = max(self.button, key=lambda x: x.height).height
      
      #set the position of all button
      self.update_pos()
    
    #update the position of all button
    def update_pos(self):
      #the half of the total width of all button
      self.midle_lenth = self.max_width*(self.n_button-1)/2
      
      for i in range(self.n_button):
        self.button[i].recwidth = self.max_width
        self.button[i].recheight = self.max_height
        self.button[i].x = self.x-self.midle_lenth+i*self.max_width
        self.button[i].y = self.y
        self.button[i].text_y = self.y
        self.button[i].text_x = self.x-self.midle_lenth+i*self.max_width
        
    def affiche(self,WIN):
      for currant in self.button:
        currant.affiche(WIN)
        
    #change the width of all button    
    def set_button_size(self,height:int,width:int):
      self.max_width = height
      self.max_height = width
      self.update_pos()
      
class select_button(array_button):
    
    def __init__(self,text:list[list],coord:tuple[float,float],scale:int,color:tuple[int,int ,int],width:int=0,height:int=0,border_width:int=0,border_color:tuple[int,int ,int]=(255,255,255),default_selected:int=0):
      super().__init__(text,coord,scale,color,width,height,border_width,border_color)
      
      self.is_click = False
      
      #create the color of the button when it's not selected
      cstm_col = self.custom_color
      self.selected_color = [(cstm_col[i][0]-40*(cstm_col[i][0]-40>0),cstm_col[i][1]-40*(cstm_col[i][1]-40>0),cstm_col[i][2]-40*(cstm_col[i][2]-40>0)) for i in range(self.n_button)]
      
      #initialise the selected button
      self.selected = default_selected
        
      #change the color of the selected button
      if self.selected != None:
        self.set_selected(self.selected)
    
    #affiche all button
    def affiche(self,WIN):
      super().affiche(WIN)
      self.click()
      #print(self.selected)
    
    #dectect which button was clicked  
    def click(self) -> int:
      for i in range(len(self.button)):
          if self.button[i].is_click:
            if self.selected != i:
              self.set_selected(i)
              self.is_click = True
            return i 
      return None
    
    def set_selected(self,selected:int):
      if self.selected != None:
        self.button[self.selected].color = self.custom_color[self.selected]
        self.button[self.selected].border_color = self.border_color
      self.button[selected].color = self.selected_color[selected]
      self.button[selected].border_color = (200,200,200)
      self.selected = selected
    
    #get the selected button
    def get_value(self) -> int:
      return self.selected
      #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
 
class number_selector(button_template):
  def __init__(self,coord:tuple,scale,color,text_scale=0,width=0,height=0,border_width=0,border_color=(0,0,0),default_value=1,max:int=50,min:int=1):
    super().__init__(coord,scale,color,border_width,border_color)
    
    self.is_click = False
    
    self.number = default_value
    self.max_number = max
    self.min_number = min
    self.cwidth = width
    self.cheight = height
    self.text_font = pygame.font.SysFont('comicsans',self.scale)
    self.text = text_button(str(self.number),(self.x,self.y),self.scale,self.color,self.cwidth,self.cheight,border_width,border_color)
    self.minus_button = cir_text_button("-",(self.x-self.scale*2.5-self.cwidth/2,self.y),self.scale,self.color,text_scale,border_width,border_color)
    self.plus_button = cir_text_button("+",(self.x+self.scale*2.5+self.cwidth/2,self.y),self.scale,self.color,text_scale,border_width,border_color)
    
  def affiche(self,WIN):
    self.text.affiche(WIN)
    self.minus_button.affiche(WIN)
    self.plus_button.affiche(WIN)
    
    self.click()
    
  def click(self) -> int:
    if self.minus_button.click() and self.number > self.min_number:
        self.number -= 1    
    elif self.plus_button.click() and self.number < self.max_number:
        self.number += 1
    else :
      return None
    self.is_click = True
    self.text.change_text([str(self.number)])
    return self.number
    #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
  
  def get_value(self) -> int:
    return self.number
      
class text_saisie(texte) :
    def __init__(self,x,y,scale,color=(0,0,0),key_limit=(0,512)):
        texte.__init__(self,[""],x,y,scale,color)
        self.key_limit = key_limit
        self.text_font = pygame.font.SysFont('comicsans',self.scale)
        self.use_input = [pygame.key.get_pressed()[i] for i in range(512)]
        self.entre = False
      
    def affiche(self,WIN):
      texte.affiche(self,WIN)
      self.get_key()
      
    def get_key(self) -> str:
      keys=pygame.key.get_pressed()
      for key in range(len(keys)):
        if keys[key] and not self.use_input[key]:
          #print(ord("."))
          self.use_input[key] = True
          if key == 8:
            self.delete_text()
          elif key == 13:
            self.answer = self.text[0]
            self.clear_text()
            self.entre = True
          elif len(self.key_limit) == 2 and (key >= self.key_limit[0] and key <= self.key_limit[1]):
            if key == 59 :
              key = 46
            self.add_text(chr(key))
          elif key in self.key_limit:
            if key == 59 :
              key = 46
            self.add_text(chr(key))
              
        if self.use_input[key] and not keys[key]:
          self.use_input[key] = False
          
    def add_text(self,letter):
      self.text[0] += letter
      #print(self.text)
      
    def delete_text(self):
      self.text[0] = self.text[0][:-1]
      
    def clear_text(self):
      self.text[0] = ""
    
    def get_text(self):
      return self.text[0]
    
    def get_answer(self):
      return self.answer
    
class twoD_array_button(button_template):
    def __init__(self,text:list[list],coord:tuple[float,float],scale:int,color:tuple[int,int ,int],width:int=0,height:int=0,space:int=0,border_width:int=0,border_color:tuple[int,int ,int]=(0,0,0)) :
      self.custom_color = color
      self.n_buttons = len(text)
      
      self.buttons = [array_button for i in range(self.n_buttons)]
      self.text = text
            
      if isinstance(color,tuple):
        self.custom_color = [[color for i in range(len(text[j]))]for j in range(self.n_buttons)]
      
      self.space = space
      button_template.__init__(self,coord,scale,color,border_width,border_color)
      max_width = 0
      max_height = 0
      
      #print(self.n_buttons)
      for i in range(self.n_buttons):
        self.buttons[i] = (array_button(text[i],coord,scale,color,width,height,border_width,border_color))
        #print(self.buttons[i].max_height, ":",self.buttons[i].max_width)
        
        #get the greatest width and height of all button
        if self.buttons[i].max_width > max_width:
          max_width = self.buttons[i].max_width
        if self.buttons[i].max_height > max_height:
          max_height = self.buttons[i].max_height
        #print(max_width, ":",max_height) 
      
      self.max_width = max_width
      self.max_height = max_height
        
      self.update()
        
        
    def update(self):
      for i in range(self.n_buttons):
        buton = self.buttons[i]
        buton.set_button_size(self.max_width,self.max_height)
        buton.y = self.y - (self.n_buttons-1)/2*self.max_height + i*self.max_height + i*self.space
        buton.update_pos()
        self.buttons[i] = buton
        
    def affiche(self,WIN):
      for but in self.buttons:
        but.affiche(WIN)
    
    
class towD_select_button(twoD_array_button):
  def __init__(self,text:list[list],coord:tuple[float,float],scale:int,color:tuple[int,int ,int],width:int=0,height:int=0,space:int=0,border_width:int=0,border_color:tuple[int,int ,int]=(0,0,0),default_selected:tuple[int,int]=(0,0)):
      
      super().__init__(text,coord,scale,color,width,height,space,border_width,border_color)
      
      self.selected = default_selected
      cstm_col = self.custom_color
      self.selected_color = [[(cstm_col[i][j][0]-40*(cstm_col[i][j][0]-40>0),cstm_col[i][j][1]-40*(cstm_col[i][j][1]-40>0),cstm_col[i][j][2]-40*(cstm_col[i][j][2]-40>0)) for j in range(self.buttons[i].n_button)] for i in range(self.n_buttons)]
      
      #change the color of the selected button
      if self.selected != None:
        self.set_selected(default_selected)
      
      
  def set_selected(self,selected:tuple[int,int]):
      x,y = selected
      cx,cy = self.selected
      if self.selected != None:
        self.buttons[cy].button[cx].color = self.custom_color[cy][cx]
        self.buttons[cy].button[cx].border_color = self.border_color
      self.buttons[y].button[x].color = self.selected_color[y][x]
      self.buttons[y].button[x].border_color = (200,200,200)
      self.selected = selected
        
  def affiche(self,WIN):
    for i in range(self.n_buttons):
      self.buttons[i].affiche(WIN)
    self.click()
        
  def click(self):
    if pygame.mouse.get_pressed():
      for i in range(self.n_buttons):
        button = self.buttons[i]
        n_button = len(button.button)
        for j in range(n_button):
          if button.button[j].is_click:
            self.set_selected((j,i))
            self.is_click = True
            #print (j,i)
    return None
        
  def get_value(self):
    return self.selected
      