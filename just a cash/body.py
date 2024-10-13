import pygame
import sys
import random as rd
from detec import  MediapipeThread,MountTracking,HandTracking,NoseTracking
from home import menu
pygame.init() #initialize pygame
#inform
#coordinate system in pygame is x-(-y) plane
def gameplay(charactor_number):
    #game variable
    game_frame_rate = 30
    scrolling_ground = 0
    scrolling_shade = 800
    scrolling_speed = 5
    screen_width = 800
    screen_heigth = 600
    flying = False # for intialize flying
    game_over = False 
    gen_pipe_freq = 2000 #(millisecond unit)
    prev_time = pygame.time.get_ticks()
    score_count = False
    score = 0
    font = pygame.font.SysFont('arial',40)
    restart_img_button = pygame.image.load('graphics/restart.png') #50x70
    #for dealing with frame rate
    clock = pygame.time.Clock()
    
    def game_restart():
        pipe_group.empty()
        item_group.empty()
        charactor.rect.y = screen_heigth//2
        charactor.rect.x = 70
        score = 0
        return score
    class gen_pipe(pygame.sprite.Sprite):
        def __init__(self,x,y,ref):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('graphics/screen1/sat.png')
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
                
            if self.rect.x < -65: 
                self.kill() #this method gonna kill this sprite object

    class gen_item(pygame.sprite.Sprite):
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

    class hippo(pygame.sprite.Sprite): #inharited from sprite parents (make this class be a part of pygame)
        def __init__(self,x,y):   
            pygame.sprite.Sprite.__init__(self)
            self.mount_tracking = MountTracking()
            self.mediapipe_thread = MediapipeThread(self.mount_tracking)
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
                if self.rect.bottom < 540: #make it fallen
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
                if self.mount_tracking.mount_state == 'open' and self.mount == False:
                    self.velocity = -7
                    self.mount = True
                if self.mount_tracking.mount_state == 'closed' and self.mount == True:
                    self.mount = False

                    #img rotation
                self.image = pygame.transform.rotate(self.images[self.index],self.velocity *-1.5) #radiouse to rotate 
            else:
                self.image = pygame.transform.rotate(self.images[self.index],-75) 

        
    
    class gen_button_from_text(pygame.sprite.Sprite):
    
        def __init__(self,text,x,y,font,text_color):
            pygame.sprite.Sprite.__init__(self)
            self.image = font.render(text,True,text_color)
            self.rect = self.image.get_rect()
            self.rect.center = [x,y]
            self.click_state = False
            self.click = 0

        def update(self):
            self.click = 0
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1\
                and self.click_state == False:
                self.click_state = True
                self.click = 0
            if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 0\
                and self.click_state == True:
                self.click_state = False
                self.click = 1

    #for background
    bg = pygame.image.load('graphics/screen1/3.png') #load image

    ground = pygame.image.load('graphics\screen1\groundfinal.png') #load image 1456 x160
    tree_shade = pygame.image.load('graphics\screen1\shade.png')

    #window size setup
    screen = pygame.display.set_mode((screen_width,screen_heigth))
    #game window setup
    pygame.display.set_caption('Flappy Bird')
    charactor = ['hippo']
    #to store

    class_map = {
    "charactor01": hippo}

    pipe_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    charactor_group = pygame.sprite.Group()
    charactor = class_map['charactor01'](200,screen_heigth//2)
    charactor_group.add(charactor)
    reset_button = gen_button_from_text('RESET',screen_width//2,screen_heigth//2,pygame.font.SysFont('arial',20),(255,255,255))
    back_home_button = gen_button_from_text('BACK',screen_width//2,screen_heigth//2 +50,pygame.font.SysFont('arial',20),(255,255,255))
    reset_button_group = pygame.sprite.Group()
    reset_button_group.add(reset_button,back_home_button)
  
    charactor.mediapipe_thread.start()
    run = True # key to run 

    while run == True:
        if charactor.rect.bottom >= 540:
            game_over = True
            flying = False   #game_over to stop bird animetion flying to stop fallen

        if flying ==True and game_over == False:
        #background part        
            screen.blit(bg,(0,0)) # paste bg to screen 
            if scrolling_ground > -400:
                scrolling_ground -= scrolling_speed
                screen.blit(ground,(scrolling_ground,495))
            else:
                scrolling_ground = 0
                screen.blit(ground,(scrolling_ground,495))

            
            con_time = pygame.time.get_ticks()
            if con_time - prev_time > 5500:
                prev_time = con_time
                top_position = rd.randint(100,500)
                gaps = rd.randint(70,120)
                pipe_top = gen_pipe(865,top_position,-1)
                pipe_bottom = gen_pipe(865,top_position-gaps,1)
                pipe_group.add(pipe_top,pipe_bottom)

                if rd.randint(1,2) == 2:
                    drop_item = gen_item(rd.randint(350,600),rd.randint(100,500))
                    item_group.add(drop_item)
            
            pipe_group.update()    
            pipe_group.draw(screen)
            item_group.update()    
            item_group.draw(screen)

        else:
            screen.blit(bg,(0,0)) # paste bg to screen 
            screen.blit(ground,(scrolling_ground,495))
            pipe_group.draw(screen)
            item_group.draw(screen)


        charactor_group.update() 
        charactor_group.draw(screen)


        #check collid
        if pygame.sprite.groupcollide(charactor_group,pipe_group,False,False):
            game_over = True
        if pygame.sprite.groupcollide(charactor_group,item_group,False,True): 
            score += 1
        score_image = pygame.font.SysFont('arial',20).render(str(score),True,(255,255,255))
        screen.blit(score_image,(10,10))
        
        
        if game_over == True and flying ==False:
            reset_button_group.draw(screen)
            reset_button_group.update()
            if reset_button.click == 1:
                pipe_group.empty()
                item_group.empty()
                charactor.rect.y = screen_heigth//2
                charactor.rect.x = 70
                score = 0
                charactor.velocity = 0
                game_over = False

            if back_home_button.click ==1:
                charactor.mediapipe_thread.stop()
                menu()
                sys.exit()
                
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            # Check if the player presses the spacebar to flap
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: 
                flying = True

        pygame.display.update()
        clock.tick(game_frame_rate) #30 frame per sec


    charactor.mediapipe_thread.stop()
    pygame.quit()

gameplay('hippo')