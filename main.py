import pygame
import sys
import random as rd
pygame.init() #initialize pygame
import pygame
import random
#from character import Character
from objectfinal2 import (Hippo,Capybara,Dog,Chicken,Owl,Zigzag,HorizonRock,VerticalRock,Sinusoidal,Oscillating,RotatingAroundPoint,Accelerating,Diagonal,Pipe,
                    Ground,Item,Cloud,Gen_button_from_image,Mountain,Popup,Txt_render
                    )
#menu instance
menu_bg = pygame.image.load('graphics\menuscreen\menubackground.png') #load image
menu_bg = pygame.transform.scale(menu_bg,(800,600))

#for choosing character instance
choosing_charactor_bg = pygame.image.load('graphics\character/18.png') #load image
choosing_charactor_bg = pygame.transform.scale(choosing_charactor_bg,(800,600))
lebel_button_group = pygame.sprite.Group()
hippo_button = Gen_button_from_image('graphics\character\hippolabel.png',203,194,True)
owl_button = Gen_button_from_image('graphics\character\owl_label.png',400,194,True)
chicken_button = Gen_button_from_image('graphics\character\chicken_label.png',594,194,True)
capybara_button = Gen_button_from_image('graphics\character\capybara_label.png',203,435,True)
dog_button = Gen_button_from_image('graphics\character\dog_label.png',400,435,True)
coming_soon_button = Gen_button_from_image('graphics\character\coming_soon_label.png',594,435,True)
choosing_charactor_button_map = [hippo_button,owl_button,chicken_button,capybara_button,dog_button]
hippo_model = Popup('graphics\character\hippyimage.png',203,154,23)
owl_model = Popup('graphics\character/owl_model.png',400,140,40)
chicken_model = Popup('graphics\character/chicken_model.png',594,150,40)
capybara_model = Popup('graphics\character\capybara_model.png',203,395,33)
dog_model = Popup('graphics\character\dog_model.png',400,380,35)
back_button = Popup('graphics\character/backbutton.png',410,548,True)
lebel_button_group.add(hippo_model,capybara_model,dog_model,chicken_model,owl_model,
chicken_button,owl_button,hippo_button,capybara_button,dog_button,back_button,coming_soon_button)

#for gameplay instance
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
    sound.set_volume(0.7)
    eating_sounds.append(sound)

crash_pipe_sound = pygame.mixer.Sound('sound\crash_sound\qubodupImpactWood.ogg')
crash_ob_sound = pygame.mixer.Sound('sound\crash_sound\qubodupImpactStone.ogg')
crash_ground_sound = pygame.mixer.Sound('sound\crash_sound\qubodupImpactMeat02.ogg')
crash_ground_sound.set_volume(0.3)
crash_pipe_sound.set_volume(0.5)
crash_ob_sound.set_volume(0.6)


#for restart window
restart_group = pygame.sprite.Group()
restart_button = Popup('graphics\menuscreen/restart.png',400,431,1,True)
gameplay_quit_button = Popup('graphics\menuscreen\quit.png',400,515,1,True)
game_over_label = Popup('graphics\menuscreen\game_over.png',400,150,4)
below_game_over_label = Popup('graphics\menuscreen/below_gameover.png',400,341,4)
score_pointer = Gen_button_from_image('graphics\menuscreen\score_pointer.png',400,263)
restart_group.add(game_over_label,score_pointer,below_game_over_label,restart_button,gameplay_quit_button)

#for level manager instance
obstacle_dict = {0:{'obstacle':None,'object_speed':None,'spawn_delay':None,'spawn_pipe_delay':3000,'scrolling_speed':(5,),'spawn_item_delay':3000},
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

#for main loop s
charactor_number = 1
display_state = 'menu'

class LevelManager:
    def __init__(self,score):
               
        self.level = 0
        self.score = score
        self.next_level_score = 1
        self.obstacle_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()

        self.ground_group = pygame.sprite.Group()
        ground = Ground(*obstacle_dict[self.level]['scrolling_speed'])
        self.ground_group.add(ground)

        self.spawn_time = pygame.time.get_ticks()
        self.spawn_pipe_time = pygame.time.get_ticks()
        self.spawn_item_time = pygame.time.get_ticks()

    def check_level_progress(self):
        # Check if the score has reached the threshold for the next level
        if self.score >= self.next_level_score:
            self.level += 1
            self.next_level_score += 1  # Increase score needed for each new level

    def spawn(self):
        i = 0
        lev = self.level
        if self.level > 9:
            lev -= 9
            i = 10*(lev)
        current_time =  pygame.time.get_ticks()
        if self.level == 0:
            spawn_pipe_delay = obstacle_dict[lev]['spawn_pipe_delay']
            if current_time - self.spawn_pipe_time > spawn_pipe_delay:
                self.spawn_pipe_time = current_time
                top_position = rd.randint(100,500)
                gaps = rd.randint(70,120)
                scrolling_speed = obstacle_dict[lev]['scrolling_speed']
                pipe_top = Pipe(865,top_position,-1,*scrolling_speed)
                pipe_bottom = Pipe(865,top_position-gaps,1,*scrolling_speed)
                self.pipe_group.add(pipe_top,pipe_bottom)
        else: 
            spawn_delay = obstacle_dict[lev]['spawn_delay'] - i
            if current_time - self.spawn_time > spawn_delay - i:
                self.spawn_time = current_time
                obstacle = obstacle_dict[lev]['obstacle']
                object_speed = (obstacle_dict[lev]['object_speed'][0] +i,)
                obstacle = obstacle(*object_speed)
                self.obstacle_group.add(obstacle)

            spawn_pipe_delay = obstacle_dict[lev]['spawn_pipe_delay'] - i
            if current_time - self.spawn_pipe_time > spawn_pipe_delay:
                self.spawn_pipe_time = current_time
                top_position = rd.randint(100,500)
                gaps = rd.randint(70,120)
                scrolling_speed = (obstacle_dict[lev]['scrolling_speed'][0] + i,)
                pipe_top = Pipe(865,top_position,-1,*scrolling_speed)
                pipe_bottom = Pipe(865,top_position-gaps,1,*scrolling_speed)
                self.pipe_group.add(pipe_top,pipe_bottom)

        spawn_item_delay = obstacle_dict[lev]['spawn_item_delay']
        if current_time - self.spawn_item_time > spawn_item_delay:
            self.spawn_item_time = current_time
            scrolling_speed = obstacle_dict[lev]['scrolling_speed']
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
        self.next_level_score = 2
        self.obstacle_group.empty()  # Remove all obstacles
        self.pipe_group.empty()
        self.item_group.empty()
      
def choosing_charactor():
    global display_state 
    global charactor_number
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('choosing charactor')
    clock = pygame.time.Clock()
    
    run = True
    while run == True:
        cersor_pos = pygame.mouse.get_pos()
        screen.blit(choosing_charactor_bg,(0,0))
        lebel_button_group.update(cersor_pos)
        lebel_button_group.draw(screen)
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                run = False
                exit_game()
        clock.tick(500)
        pygame.display.update()
        for button in choosing_charactor_button_map:
            if button.check_click(pygame.mouse.get_pressed()[0],cersor_pos) == 1:
                screen.blit(choosing_charactor_bg,(0,0))
                #wait screen
                pygame.display.update()
                display_state = 'gameplay'
                charactor_number = choosing_charactor_button_map.index(button)+1
                run = False
                break

            if  back_button.check_click(pygame.mouse.get_pressed()[0],cersor_pos) == 1:
                screen.blit(choosing_charactor_bg,(0,0))
                pygame.display.update()
                lebel_button_group.update(cersor_pos)
                display_state = 'menu'
                run = False
                break
        

def menu():
    global display_state
    song = pygame.mixer.Sound('sound/muzak-on-239167.mp3')
    
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
    lets_go_button = Popup('graphics\menuscreen\letsgobutton.png',403,341,1,True)
    quit_button = Popup('graphics\menuscreen\quitbuttton.png',403,445,1,True)
    button_group.add(lets_go_button,gamename,quit_button)
    
    clock = pygame.time.Clock()

    #song.play()
    run = True
    while run == True:
       
        cersor_pos = pygame.mouse.get_pos()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
                exit_game()

        screen.blit(menu_bg,(0,0)) 
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
        button_group.update(cersor_pos)
        button_group.draw(screen)
        
        if lets_go_button.check_click(pygame.mouse.get_pressed()[0],cersor_pos) == 1:
            object_group.empty()
            ground_group.empty()
            button_group.empty()
            run == False
            display_state = 'choosing_charactor'
            break
            
        if quit_button.check_click(pygame.mouse.get_pressed()[0],cersor_pos) == 1:
            exit_game()   
            
        clock.tick(30)
        pygame.display.update()
    

def gameplay(charactor_number):
    global display_state 
    #game variable
    prelude = preludes[charactor_number -1]
    game_frame_rate = 45
    flying = False # for intialize flying
    game_over = False 
    score = 0
    clock = pygame.time.Clock()
   
    #window size setup
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('(Not)Flappy zoo')
    
    #for charater part
    charactor_group = pygame.sprite.Group()
    charactor = charactor_map[charactor_number]
    charactor_group.add(charactor)

    #for showing score part
    score_group = pygame.sprite.Group()
    mini_score_pointer = Gen_button_from_image('graphics\menuscreen\mini_score_pointer.png',86,33)
    show_score = Txt_render(int(score),(255,255,255),125,34,20)
    score_group.add(mini_score_pointer,show_score)

    #to feed frame and process another thread
    charactor.start_thread() 
    charactor.is_running = True
    
    #for sound event
    sound_played1 = False
    sound_played2 = False
    sound_played3 = False 
    
    Level = LevelManager(score)
    run = True # key to run 
    while run == True:
        screen.blit(prelude,(0,0))
        frame = charactor.pygame_frame
        #game mocca####################
        if charactor.rect.bottom >= 540:
            if sound_played1 == False:
                sound_played1 = True
                crash_ground_sound.play()
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
                score += 1
                show_score.txt = score
                score_group.update()    
            score_group.draw(screen)
        else:
            #game over
            if frame is not None:
                screen.blit(frame,(0,0)) # paste bg to screen 
            Level.draw(screen)

        if pygame.sprite.groupcollide(charactor_group,Level.pipe_group,False,False):
            if sound_played2 == False:
                sound_played2 = True
                crash_pipe_sound.play()
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
        #game mocca#################

        #for reset the game
        if game_over == True and flying ==False:
            cersor_pos = pygame.mouse.get_pos()
            for event in pygame.event.get(): 
                    if event.type == pygame.QUIT:
                        charactor.stop_thread() 
                        exit_game()
                
            restart_group.draw(screen)
            restart_group.update(cersor_pos)
            show_score.font_size = 50
            show_score.rect.center = (456,264)
            screen.blit(show_score.image,show_score.rect)

            if restart_button.check_click(pygame.mouse.get_pressed()[0],cersor_pos) == 1:
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
            if gameplay_quit_button.check_click(pygame.mouse.get_pressed()[0],cersor_pos) ==1:
                score = 0
                game_over = False
                charactor.stop_thread()
                score_group.empty()
                charactor.reset()
                display_state = 'choosing_charactor'
                charactor.stop_thread() 
                run = False
                del Level
            
        for event in pygame.event.get(): #I think this for interact with user 
            # event handling to close the window
            if event.type == pygame.QUIT:
                charactor.stop_thread() 
                exit_game()

            # Check if the player presses the spacebar to flap
            #for starting game
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: 
                flying = True
                charactor.flying = True

        pygame.display.update()
        clock.tick(game_frame_rate) 
    charactor.stop_thread()
def exit_game():
    pygame.quit()
    sys.exit()


### main loop 
while True:
    if display_state == "menu":
        menu()
    elif display_state == "choosing_charactor":
        choosing_charactor()
    elif display_state == "gameplay":
        gameplay(charactor_number)
    else:
        pygame.quit()

