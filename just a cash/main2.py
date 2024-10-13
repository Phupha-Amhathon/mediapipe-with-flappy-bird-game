import pygame
import sys
import random as rd
from detec import HandTracking, MediapipeThread,MountTracking,NoseTracking,EyesTracking
pygame.init() #initialize pygame
#inform
#coordinate system in pygame is x-(-y) plane

#game variable
game_frame_rate = 30
scrolling_ground = 0
scrolling_speed = 4 
screen_width = 400
screen_heigth = 600
flying = False # for intialize flying
game_over = False 
gen_pipe_freq = 2000 #(millisecond unit)
prev_time = pygame.time.get_ticks()
score_count = False
score = 0
font = pygame.font.SysFont('arial',40)
restart_img_button = pygame.image.load('graphics/restart.png') #50x70

def get_gaps():
    return rd.randint(80,110)

def get_rdposi():
    return rd.randint(30,450)

def text_convernt(text,font,text_color,x,y):
    img = font.render(str(text),True,text_color)
    screen.blit(img,(x,y))

def game_restart():
    pipe_group.empty()
    tem_group.empty()
    flappy.rect.y = screen_heigth//2
    flappy.rect.x = 70

    score = 0
    return score
 
class hippo(pygame.sprite.Sprite): #inharited from sprite parents (make this class be a part of pygame)
    
    def __init__(self,x,y):
        
        pygame.sprite.Sprite.__init__(self)
    
        #load image
        self.images = []
        for i in range(1,5):
            image = pygame.image.load(f'graphics/{i}.png')
            self.images.append(image)

        self.index = 0
        self.counter = 0

        #prepare for draw require
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #get properties of ractangle like to refer address
        self.rect.center = [x,y] #pass positon (x,y)<center of rec> to rec

        #for gravity
        self.velocity = 0
        
        self.clicked = False

        self.mount = False

    def update(self): #overdrive update
        #for animation
        self.counter +=1
        reset = 15

        if flying == True:   
            #for gravity
            self.velocity +=0.5
            if self.velocity > 5: #take limit
                self.velocity == 5
            if self.rect.bottom < 560:
                self.rect.y += int(self.velocity) #y-coodinate of rect and image

        if game_over == False:
        #15 frame per one im 
            if self.counter >= reset:
                self.index +=1 
                self.counter = 0
                
                if self.index >= len(self.images): #reset when iterable idex will cautch en index out of range
                    self.index = 0
            self.image = self.images[self.index] #just update it 

            #flape
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
                self.clicked = True
                self.velocity = -7
            if pygame.mouse.get_pressed()[0] == 0:# for avoid continouse click
                self.clicked = False

            #hippo rotation
            self.image = pygame.transform.rotate(self.images[self.index],self.velocity *-1.5) #radiouse to rotate 
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-75) 

class pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,ref):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics\pipe.png')
        self.image = pygame.transform.scale(self.image,(40,560))
        self.rect = self.image.get_rect()
        
        #ref =1 is top ,ref = -1 if from the bottom
        if ref == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y]
        else:
            self.rect.topleft = [x,y]

    def update(self):
        if flying == True:
            self.rect.x -= scrolling_speed
        if self.rect.x < -30: 
            self.kill() #this method gonna kill this sprite object

class item(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics\cabbage.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        if flying == True:
            self.rect.x -= scrolling_speed

        if self.rect.x < -30:
            self.kill()

class gen_button_from_img():
    def __init__(self,img,x,y):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(self.img,(self.rect.x,self.rect.y))
        #check position of cersor when it is clicked
        cersor_pos = pygame.mouse.get_pos() #index got x and y coordinate
        if self.rect.collidepoint(cersor_pos) and pygame.mouse.get_pressed()[0] == 1:
            return 1





#for dealing with frame rate
clock = pygame.time.Clock()
#window size setup
screen = pygame.display.set_mode((screen_width,screen_heigth))
#game window setup
pygame.display.set_caption('Flappy Bird')

#for background 
bg = pygame.image.load('graphics/images (1).jpg') #load image
bg = pygame.transform.scale(bg,(400,550))
ground = pygame.image.load('graphics/underground.png') #load image 1456 x160


flappy = hippo(70,screen_heigth//2) #create hippo
hippo_group = pygame.sprite.Group() #for storing hippo   # like a list but store sprite and  will use method for individual
hippo_group.add(flappy)


pipe_group = pygame.sprite.Group()#for store pipes

#main game loop
tem_group = pygame.sprite.Group()
tem = item(screen_width//2,screen_heigth//2)
tem_group.add(tem)


run = True # key to run 


while run == True:
    
    #check if bird dies
    if flappy.rect.bottom >= 560:
        game_over = True
        flying = False
    
    #check if bird colide some pipe
    if pygame.sprite.groupcollide(hippo_group,pipe_group,False,False): #if it colide kill them == false
        game_over = True

    #background part     
    screen.blit(bg,(0,0)) # paste bg to screen 
    if game_over == False and flying == True:
        
        #for item
        tem_group.draw(screen)
        tem_group.update()

        #pipe draw part
        pipe_group.draw(screen)
        pipe_group.update()

        #to scrolling background   
        if -scrolling_ground > 1456:
            scrolling_ground = 0
        scrolling_ground -= scrolling_speed
        screen.blit(ground,(scrolling_ground,550))

        #generate pipe
        con_time = pygame.time.get_ticks()
        if con_time - prev_time >= gen_pipe_freq:
            prev_time = con_time
            gaps1 =get_gaps()
            rdposi = get_rdposi()
            lower_pipe = pipe(screen_width,rdposi + gaps1 ,-1)
            upper_pipe = pipe(screen_width,rdposi,1)
            pipe_group.add(lower_pipe)
            pipe_group.add(upper_pipe)

            tem = item(rd.randint(50,500),rd.randint(120,400))
            tem_group.add(tem)
        
    else:
        #when collide is True stop scrolling background
        pipe_group.draw(screen)
        tem_group.draw(screen)
        screen.blit(ground,(scrolling_ground,550))

    #for score
    if pygame.sprite.groupcollide(hippo_group,tem_group,False,True):
        score +=1
    text_convernt(score,font,(255,255,255),screen_width-50,screen_heigth-50) #show

    #bird part  
    hippo_group.draw(screen) #put hippo (will apply this to each in group)
    hippo_group.update()
   
    for event in pygame.event.get(): #I think this for interact with user 
        # event handling to close the window
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
         # Check if the player presses the spacebar to flap
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: 
            flying = True

    #restart part
    restart_button = gen_button_from_img(restart_img_button,screen_width//2,screen_heigth//2 -30)
    
    if game_over == True:
        val = restart_button.draw()
        if val == 1:
            game_over = False
            score = game_restart()

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(game_frame_rate) #30 frame per sec

pygame.quit()