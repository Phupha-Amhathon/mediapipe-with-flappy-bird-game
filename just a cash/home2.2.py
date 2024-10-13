import pygame
import sys
import random as rd
from object import hippo,snake,mosquitoe,FloatingObstacle
pygame.init() #initialize pygame
import pygame
import random
#from character import Character
from object import FloatingObstacle,Zigzag,HorizonRock,VerticalRock,Sinusoidal,Oscillating,RotatingAroundPoint,Accelerating,Diagonal


class LevelManager:
    def __init__(self,score):
        self.obstacle_dict = {1:{'obstacle':HorizonRock,'object_speed':(5,),'spawn_delay':1500},
                              2:{'obstacle':HorizonRock,'object_speed':(7,),'spawn_delay':1000},
                              3:{'obstacle':Diagonal,'object_speed':(10,),'spawn_delay':1500},
                              4:{'obstacle':VerticalRock,'object_speed':(10,),'spawn_delay':1000},
                              5:{'obstacle':RotatingAroundPoint,'object_speed':(5,),'spawn_delay':1500},
                              6:{'obstacle':Oscillating,'object_speed':(5,),'spawn_delay':1500}, #sun u gab t(up and down)
                              7:{'obstacle':Accelerating,'object_speed':(5,),'spawn_delay':1500},
                              8:{'obstacle':Zigzag,'object_speed':(5,),'spawn_delay':1500},#up n down max
                              9:{'obstacle':Sinusoidal,'object_speed':(5,),'spawn_delay':1500},
                              }
                              
        self.level = 0
        self.score = score
        self.next_level_score = 5
        self.obstacle_group = pygame.sprite.Group()
        self.spawn_time = pygame.time.get_ticks()
    def check_level_progress(self):
        # Check if the score has reached the threshold for the next level
        if self.score >= self.next_level_score:
            self.level += 1
        
            self.next_level_score += 5  # Increase score needed for each new level
    def spawn(self):
        if self.level > 0:
            current_time =  pygame.time.get_ticks()
            spawn_delay = self.obstacle_dict[self.level]['spawn_delay']
            if current_time - self.spawn_time > spawn_delay:
                
                self.spawn_time = current_time
                obstacle = self.obstacle_dict[self.level]['obstacle']
                object_speed = self.obstacle_dict[self.level]['object_speed']
                obstacle = obstacle(*object_speed)
                self.obstacle_group.add(obstacle)

    def update(self):
        self.check_level_progress()
        self.spawn()
        self.obstacle_group.update()


    def draw(self, screen):
        # Draw obstacles
        self.obstacle_group.draw(screen) 
    def reset(self):
        self.level = 0
        self.score = 0
        self.next_level_score = 5
        self.obstacle_group.empty()  # Remove all obstacles

class gen_button_from_text(pygame.sprite.Sprite):
    
    def __init__(self,text,x,y,font,text_color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(text,True,text_color)
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.click_state = False
        self.click = 0
        self.click_sound = pygame.mixer.Sound('sound/clicksound01.wav')

    def update(self):
        self.click = 0
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1\
        and self.click_state == False:
            self.click_state = True
            self.click_sound.play()
            self.click = 0
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 0\
            and self.click_state == True:
            self.click_state = False
            self.click = 1
            
def choosing_charactor():
    bg = pygame.image.load('graphics/images (1).jpg') #load image
    bg = pygame.transform.scale(bg,(800,600))
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('choosing charactor')
    screen.blit(bg,(0,0)) # paste bg to screen 
    run = True
    charactor_number1_button = gen_button_from_text('hippy',400,200,pygame.font.SysFont('arial',20),(0,0,0))
    charactor_number2_button = gen_button_from_text('snake',400,250,pygame.font.SysFont('arial',20),(0,0,0))
    charactor_number3_button = gen_button_from_text('mosquitto',400,300,pygame.font.SysFont('arial',20),(0,0,0))
    back_button = gen_button_from_text('back',400,350,pygame.font.SysFont('arial',20),(0,0,0))
    wait_button = gen_button_from_text('wait...',400,350,pygame.font.SysFont('arial',20),(0,0,0))


    button_group = pygame.sprite.Group()
    button_group.add(charactor_number1_button,charactor_number2_button,
                     charactor_number3_button,charactor_number3_button,
                     back_button)
    button_group.draw(screen)
    while run == True:
        button_group.update()
        if charactor_number1_button.click == 1:
            button_group.empty()
            button_group.add(wait_button)
            screen.blit(bg,(0,0))
            button_group.draw(screen)
            pygame.display.update()
            gameplay(1)
            sys.exit() 
            
        if charactor_number2_button.click == 1:
            button_group.empty()
            button_group.add(wait_button)
            screen.blit(bg,(0,0))
            button_group.draw(screen)
            pygame.display.update()
            gameplay(2)
            sys.exit() 

        if charactor_number3_button.click == 1:
            button_group.empty()
            button_group.add(wait_button)
            screen.blit(bg,(0,0))
            button_group.draw(screen)
            pygame.display.update()
            gameplay(3)
            sys.exit() 
           
        if  back_button.click == 1:
            button_group.empty()
            button_group.add(wait_button)
            screen.blit(bg,(0,0))
            button_group.draw(screen)
            pygame.display.update()
            menu()
            sys.exit()
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        pygame.display.update()

def menu():
    song = pygame.mixer.Sound('sound/muzak-on-239167.mp3')
    bg = pygame.image.load('graphics/images (1).jpg') #load image
    bg = pygame.transform.scale(bg,(800,600))
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('flappy zoo')
    screen.blit(bg,(0,0)) # paste bg to screen 

    play_button = gen_button_from_text('PLAY',400,200,pygame.font.SysFont('arial',20),(0,0,0))
    throw_button = gen_button_from_text('EXIT',400,300,pygame.font.SysFont('arial',20),(0,0,0))

    button_group = pygame.sprite.Group()
    button_group.add(play_button,throw_button)
    button_group.draw(screen)
    #song.play()
    run = True
    while run == True:
        button_group.update()
        if play_button.click ==1:
            run == False
            choosing_charactor()
            sys.exit()
            

        if throw_button.click == 1:
            run = False
            sys.exit()
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        pygame.display.update()
 
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
            self.sound = pygame.mixer.Sound('sound/clicksound01.wav')
        def update(self):
            if flying == True:
                self.rect.x -= scrolling_speed

            if self.rect.x < -30:
                self.kill()

            

    #for background
    bg = pygame.image.load('graphics/screen1/3.png') #load image

    ground = pygame.image.load('graphics\screen1\groundfinal.png') #load image 1456 x160
    tree_shade = pygame.image.load('graphics\screen1\shade.png')

    #window size setup
    screen = pygame.display.set_mode((screen_width,screen_heigth))
    #game window setup
    pygame.display.set_caption('Flappy Bird')
    
    #to store

    class_map = {
    "charactor1": hippo,"charactor2":snake,'charactor3':mosquitoe}

    pipe_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    charactor_group = pygame.sprite.Group()
    charactor = class_map[f'charactor{charactor_number}'](200,screen_heigth//2,False,False)
    charactor_group.add(charactor)
    reset_button = gen_button_from_text('RESET',screen_width//2,screen_heigth//2,pygame.font.SysFont('arial',20),(255,255,255))
    back_home_button = gen_button_from_text('BACK',screen_width//2,screen_heigth//2 +50,pygame.font.SysFont('arial',20),(255,255,255))
    reset_button_group = pygame.sprite.Group()
    reset_button_group.add(reset_button,back_home_button)
  
    charactor.mediapipe_thread.start()
    
    # Convert the image to a format that Pygame can handle
    #background part        
     # paste bg to screen   

    Level = LevelManager(score)
    run = True # key to run 
    while run == True:
        process_frame = charactor.mediapipe_thread.frame_bgr
        if charactor.rect.bottom >= 540:
            game_over = True
            flying = False   #game_over to stop bird animetion flying to stop fallen
            charactor.game_over = True
            charactor.flying = False

        if flying ==True and game_over == False:
            #for bg
            if process_frame is not None:
                screen.blit(process_frame,(0,0))
            #for scrolling ground
            if scrolling_ground > -400:
                scrolling_ground -= scrolling_speed
                screen.blit(ground,(scrolling_ground,495))
            else:
                scrolling_ground = 0
                screen.blit(ground,(scrolling_ground,495))

            Level.score = score
            Level.update()
            Level.draw(screen)


            #ja mai chai cuz u nai level
            con_time = pygame.time.get_ticks()
            if con_time - prev_time > 4000:
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
            if process_frame is not None:
                screen.blit(process_frame,(0,0)) # paste bg to screen 
            screen.blit(ground,(scrolling_ground,495))
            pipe_group.draw(screen)
            item_group.draw(screen)
        
        #check collid
        '''
        if pygame.sprite.groupcollide(charactor_group,pipe_group,False,False)\
            or pygame.sprite.groupcollide(charactor_group,Level.obstacle_group,False,False):
            game_over = True
            charactor.game_over = True
        '''
        if pygame.sprite.groupcollide(charactor_group,pipe_group,False,False):
            game_over = True
            charactor.game_over = True

        charactor_group.update() 
        charactor_group.draw(screen)

        
        #for scoring   
        if pygame.sprite.groupcollide(charactor_group,item_group,False,True): 
            drop_item.sound.play()
            score += 5
        score_image = pygame.font.SysFont('arial',20).render(str(score),True,(255,255,255))
        screen.blit(score_image,(10,10))
        
        
        #for reset the game
        if game_over == True and flying ==False:
            
            font = pygame.font.SysFont('arial', 50)
            game_over_text = font.render('Game Over', True, (255, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - 100, screen_heigth // 2 - 50))
            reset_button_group.draw(screen)
            reset_button_group.update()
            if reset_button.click == 1:
                Level.reset()
                pipe_group.empty()
                item_group.empty()
                charactor.rect.y = screen_heigth//2
                charactor.rect.x = 70
                score = 0
                charactor.velocity = 0
                game_over = False
                charactor.game_over = False
            
            if back_home_button.click ==1:
                charactor.mediapipe_thread.stop()
                choosing_charactor()
                sys.exit()
               
                
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                run = False
                charactor.mediapipe_thread.stop() 
                sys.exit()


            # Check if the player presses the spacebar to flap
            #for starting game
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: 
                flying = True
                charactor.flying = True

        pygame.display.update()
        clock.tick(game_frame_rate) #30 frame per sec


    charactor.mediapipe_thread.stop()
    pygame.quit()
menu()