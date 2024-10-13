import pygame
import sys
import random as rd
pygame.init() #initialize pygame
import pygame
import random
#from character import Character
from object4 import (Hippo,Capybara,Dog,Chicken,Owl,FloatingObstacle,Zigzag,HorizonRock,VerticalRock,Sinusoidal,Oscillating,RotatingAroundPoint,Accelerating,Diagonal,Pipe,
                    Ground,Item,Cloud,Gen_button_from_image,Mountain,Popup,Txt_render
                    )
charactor_map = {1:Hippo(150,300),
                 2:Owl(150,300),
                 3:Chicken(150,300),
                 4:Capybara(150,300),
                 5:Dog(150,300)}
preludes = []
eating_sounds = []
for i in range(1,6):
    prelude = pygame.image.load(f'graphics\character\prelude/{i}.png')
    preludes.append(prelude)
    sound = pygame.mixer.Sound(f'sound\eating sound/{i}.mp3')
    eating_sounds.append(sound)

crash_pipe_sound = pygame.mixer.Sound('sound\crash_sound\qubodupImpactWood.ogg')
crash_ob_sound = pygame.mixer.Sound('sound\crash_sound\qubodupImpactStone.ogg')
crash_ground_sound = pygame.mixer.Sound('sound\crash_sound\qubodupImpactMeat02.ogg')

class LevelManager:
    def __init__(self,score):
        self.obstacle_dict = {0:{'obstacle':None,'object_speed':None,'spawn_delay':None,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
                              1:{'obstacle':HorizonRock,'object_speed':(5,),'spawn_delay':1500,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
                              2:{'obstacle':HorizonRock,'object_speed':(7,),'spawn_delay':1000,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
                              3:{'obstacle':Diagonal,'object_speed':(10,),'spawn_delay':1500,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
                              4:{'obstacle':VerticalRock,'object_speed':(10,),'spawn_delay':1000,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
                              5:{'obstacle':RotatingAroundPoint,'object_speed':(5,),'spawn_delay':1500,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
                              6:{'obstacle':Oscillating,'object_speed':(5,),'spawn_delay':1500,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000}, #sun u gab t(up and down)
                              7:{'obstacle':Accelerating,'object_speed':(5,),'spawn_delay':1500,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
                              8:{'obstacle':Zigzag,'object_speed':(5,),'spawn_delay':1500,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},#up n down max
                              9:{'obstacle':Sinusoidal,'object_speed':(5,),'spawn_delay':1500,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
                              }
                              
        self.level = 0
        self.score = score
        self.next_level_score = 5
        self.obstacle_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()

        self.ground_group = pygame.sprite.Group()
        ground = Ground(*self.obstacle_dict[self.level]['scrolling_speed'])
        self.ground_group.add(ground)

        self.spawn_time = pygame.time.get_ticks()
        self.spawn_pipe_time = pygame.time.get_ticks()
        self.spawn_item_time = pygame.time.get_ticks()

    def check_level_progress(self):
        # Check if the score has reached the threshold for the next level
        if self.score >= self.next_level_score:
            self.level += 1
            self.next_level_score += 5  # Increase score needed for each new level

    def spawn(self):
        current_time =  pygame.time.get_ticks()
        
        if self.level > 0:
            spawn_delay = self.obstacle_dict[self.level]['spawn_delay']
            if current_time - self.spawn_time > spawn_delay:
                self.spawn_time = current_time
                obstacle = self.obstacle_dict[self.level]['obstacle']
                object_speed = self.obstacle_dict[self.level]['object_speed']
                obstacle = obstacle(*object_speed)
                self.obstacle_group.add(obstacle)


        spawn_pipe_delay = self.obstacle_dict[self.level]['spawn_pipe_delay']
        if current_time - self.spawn_pipe_time > spawn_pipe_delay:
            self.spawn_pipe_time = current_time
            top_position = rd.randint(100,500)
            gaps = rd.randint(70,120)
            scrolling_speed = self.obstacle_dict[self.level]['scrolling_speed']
            pipe_top = Pipe(865,top_position,-1,*scrolling_speed)
            pipe_bottom = Pipe(865,top_position-gaps,1,*scrolling_speed)
            self.pipe_group.add(pipe_top,pipe_bottom)

        spawn_item_delay = self.obstacle_dict[self.level]['spawn_item_delay']
        if current_time - self.spawn_item_time > spawn_item_delay:
            self.spawn_item_time = current_time
            scrolling_speed = self.obstacle_dict[self.level]['scrolling_speed']
            item = Item(random.randint(150,850),random.randint(20,540),*scrolling_speed)
            self.item_group.add(item)

    def update(self):
        self.check_level_progress()
        self.spawn()
        self.obstacle_group.update()
        self.pipe_group.update()
        self.item_group.update()
        self.ground_group.update()

    def draw(self, screen):
        # Draw obstacles
        self.obstacle_group.draw(screen) 
        self.ground_group.draw(screen) 
        self.pipe_group.draw(screen) 
        self.item_group.draw(screen)
        

    def reset(self):
        self.level = 0
        self.score = 0
        self.next_level_score = 5
        self.obstacle_group.empty()  # Remove all obstacles
        self.pipe_group.empty()
        self.item_group.empty()
          
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
    bg = pygame.image.load('graphics\character/18.png') #load image
    bg = pygame.transform.scale(bg,(800,600))
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('choosing charactor')
     # paste bg to screen 
    
    lebel_button_group = pygame.sprite.Group()
    hippo_button = Gen_button_from_image('graphics\character\hippolabel.png',203,194)
    owl_button = Gen_button_from_image('graphics\character\owl_label.png',400,194)
    chicken_button = Gen_button_from_image('graphics\character\chicken_label.png',594,194)
    capybara_button = Gen_button_from_image('graphics\character\capybara_label.png',203,435)
    dog_button = Gen_button_from_image('graphics\character\dog_label.png',400,435)
    coming_soon_button = Gen_button_from_image('graphics\character\coming_soon_label.png',594,435)
    
    hippo_model = Popup('graphics\character\hippyimage.png',203,154,23)
    owl_model = Popup('graphics\character/owl_model.png',400,140,40)
    chicken_model = Popup('graphics\character/chicken_model.png',594,150,40)
    capybara_model = Popup('graphics\character\capybara_model.png',203,395,33)
    dog_model = Popup('graphics\character\dog_model.png',400,380,35)
    
    

    back_button = Gen_button_from_image('graphics\character/backbutton.png',410,548)
    lebel_button_group.add(hippo_model,capybara_model,dog_model,chicken_model,owl_model,
                           chicken_button,owl_button,hippo_button,capybara_button,dog_button,back_button,coming_soon_button)


    wait_button = gen_button_from_text('wait...',400,350,pygame.font.SysFont('arial',20),(0,0,0))


    

    run = True
    while run == True:
        screen.blit(bg,(0,0))
        lebel_button_group.update()
        lebel_button_group.draw(screen)
        if hippo_button.update() == 1:
            lebel_button_group.empty
            screen.blit(bg,(0,0))
            #wait screen
            pygame.display.update()
            gameplay(1)
            sys.exit() 
            
        if capybara_button.update() == 1:
            lebel_button_group.empty
            screen.blit(bg,(0,0))
            
            pygame.display.update()
            gameplay(4)
            sys.exit() 

        if dog_button.update() == 1:
            lebel_button_group.empty
            screen.blit(bg,(0,0))
            
            pygame.display.update()
            gameplay(5)
            sys.exit() 
        
        if chicken_button.update() == 1:
            lebel_button_group.empty
            screen.blit(bg,(0,0))
            
            pygame.display.update()
            gameplay(3)
            sys.exit() 

        if owl_button.update() == 1:
            lebel_button_group.empty
            screen.blit(bg,(0,0))
            
            pygame.display.update()
            gameplay(2)
            sys.exit() 

        if  back_button.update() == 1:
            screen.blit(bg,(0,0))
            
            pygame.display.update()
            menu()
            sys.exit()
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        pygame.display.update()
    pygame.quit()
def menu():
    song = pygame.mixer.Sound('sound/muzak-on-239167.mp3')
    bg = pygame.image.load('graphics\menuscreen\menubackground.png') #load image
    bg = pygame.transform.scale(bg,(800,600))
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('flappy zoo')
    # paste bg to screen 

    object_group = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()
    prev_time = pygame.time.get_ticks()
    ground = Ground(2)
    ground_group.add(ground)
    
    button_group = pygame.sprite.Group()
    gamename = Popup('graphics\menuscreen\gamename.png',403,175,1)
    lets_go_button = Popup('graphics\menuscreen\letsgobutton.png',403,341,1)
    quit_button = Popup('graphics\menuscreen\quitbuttton.png',403,445,1)
    button_group.add(lets_go_button,gamename,quit_button)
    

    
    
    
    clock = pygame.time.Clock()

    #song.play()
    run = True
    while run == True:
        screen.blit(bg,(0,0)) 
        #for object
        con_time = pygame.time.get_ticks()
        if con_time - prev_time>5000:
            prev_time = con_time
            pipe = Pipe(860,random.randint(100,400),random.choice([-1,1]),3)

            for i in range(random.choice([1,2,3])):
                cloud = Cloud(860,random.randint(10,500),random.randint(1,7))
                item = Item(860,random.randint(10,550),random.randint(1,5))
                object_group.add(cloud,item)

            i = random.randint(1,30)
            if i == 1:
                mountain = Mountain(900,550,1)
                object_group.add(mountain)
                
            object_group.add(pipe)
        
        object_group.update()
        object_group.draw(screen)
        ground_group.update()
        ground_group.draw(screen)
        button_group.draw(screen)
        
        if lets_go_button.update() == 1:
            print('what the hell')
            object_group.empty()
            ground_group.empty()
            button_group.empty()
            run == False
            choosing_charactor()
            sys.exit()
            

        if quit_button.update() == 1:
            run = False
            sys.exit()
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        clock.tick(30)
        pygame.display.update()
    pygame.quit()
def gameplay(charactor_number):
    #game variable
    
    prelude = preludes[charactor_number -1]
    game_frame_rate = 45
    scrolling_shade = 800
    screen_width = 800
    screen_heigth = 600
    flying = False # for intialize flying
    game_over = False 
    score_count = False
    score = 0
    #for dealing with frame rate
    clock = pygame.time.Clock()
   
    tree_shade = pygame.image.load('graphics\screen1\shade.png')

    #window size setup
    screen = pygame.display.set_mode((screen_width,screen_heigth))
    pygame.display.set_caption('(Not)Flappy zoo')
    


    charactor_group = pygame.sprite.Group()
    charactor = charactor_map[charactor_number]
    charactor_group.add(charactor)

    pause_button = gen_button_from_text('PAUSE',750,20,pygame.font.SysFont('arial',20),(255,255,255))
    continue_button = gen_button_from_text('CONTINUE',750,20,pygame.font.SysFont('arial',20),(255,255,255))

    #for restart window
    restart_group = pygame.sprite.Group()
    restart_button = Popup('graphics\menuscreen/restart.png',400,431,1)
    quit_button = Popup('graphics\menuscreen\quit.png',400,515,1)
    game_over_label = Popup('graphics\menuscreen\game_over.png',400,150,4)
    below_game_over_label = Popup('graphics\menuscreen/below_gameover.png',400,341,4)
    score_pointer = Gen_button_from_image('graphics\menuscreen\score_pointer.png',400,263)
    restart_group.add(game_over_label,score_pointer,below_game_over_label,restart_button,quit_button)

    #for showing score part
    score_group = pygame.sprite.Group()
    mini_score_pointer = Gen_button_from_image('graphics\menuscreen\mini_score_pointer.png',86,33)
    show_score = Txt_render(int(score),(255,255,255),125,34,20)
    score_group.add(mini_score_pointer,show_score)
    
    '''
    pause_button_group = pygame.sprite.Group()
    pause_button_group.add(pause_button)
    continue_button_group = pygame.sprite.Group()
    continue_button_group.add(continue_button)
    '''

    charactor.start_thread() #initialize
    charactor.is_running = True
    
    sound_played1 = False
    sound_played2 = False
    sound_played3 = False
    # Convert the image to a format that Pygame can handle
    #background part        
     # paste bg to screen   
    
    Level = LevelManager(score)
    run = True # key to run 
    while run == True:
        screen.blit(prelude,(0,0))
        frame = charactor.pygame_frame
        if charactor.rect.bottom >= 540:
            if sound_played1 == False:
                sound_played1 = True
                crash_ground_sound.play
            game_over = True
            flying = False   #game_over to stop bird animetion flying to stop fallen
            charactor.game_over = True
            charactor.flying = False

        if flying ==True and game_over == False:
            #for bg
            if frame is not None:
                screen.blit(frame,(0,0))
            Level.score = score
            Level.update()
            Level.draw(screen)

            #for scoring   
            if pygame.sprite.groupcollide(charactor_group,Level.item_group,False,True): 
                eating_sounds[random.randint(0,4)].play()
                score += 5
                show_score.txt = score
                score_group.update()    
            score_group.draw(screen)
            

        else:
            #game over
            if frame is not None:
                screen.blit(frame,(0,0)) # paste bg to screen 
            #screen.blit(ground,(scrolling_ground,495))
            Level.draw(screen)


        if pygame.sprite.groupcollide(charactor_group,Level.pipe_group,False,False):
            if sound_played2 == False:
                sound_played2 = True
                crash_pipe_sound.play
            game_over = True
            charactor.game_over = True
        if pygame.sprite.groupcollide(charactor_group,Level.obstacle_group,False,False):
            if sound_played3 == False:
                sound_played3 = True
                crash_ob_sound.play()
            game_over = True
            charactor.game_over = True

        charactor_group.update() 
        charactor_group.draw(screen)

        
        
        
        '''
        #for pauasing game
        pause_button_group.update()
        pause_button_group.draw(screen)
        if pause_button.click == 1:
            while True:
                screen.blit(process_frame,(0,0))
                Level.draw(screen)
                continue_button_group.update()
                continue_button_group.draw(screen)
                reset_button_group.draw(screen)
                print('we fuck uppppp')
                if continue_button.click == 1:
                    break
            '''


        #for reset the game
        if game_over == True and flying ==False:
            restart_group.draw(screen)
            restart_group.update()

            show_score.font_size = 50
            show_score.rect.center = (456,264)
            screen.blit(show_score.image,show_score.rect)

            if restart_button.update()== 1:
                Level.reset()

                show_score.font_size = 20
                show_score.rect.center = (125,34)
                show_score.txt = 0
                score_group.update()  
                score = 0
                game_over = False
                charactor.reset()
                sound_played1 = False
                sound_played2 = False
                sound_played3 = False
            #for quit game
            if quit_button.update() ==1:
                
                score = 0
                game_over = False
                charactor.stop_thread()
                score_group.empty()
                charactor.reset()
                choosing_charactor()
                del Level
                sys.exit()
               
                
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                run = False
                charactor.stop_thread() 
                sys.exit()


            # Check if the player presses the spacebar to flap
            #for starting game
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: 
                flying = True
                charactor.flying = True

        pygame.display.update()
        clock.tick(game_frame_rate) #30 frame per sec

    charactor.stop_thread()
    pygame.quit()
menu()
