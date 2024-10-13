import pygame
import random 
import cv2
import math 
import threading
from detectfinal import MountTracking,HandTracking,NoseTracking,PoseTracking,EyesTracking
pygame.init() #initialize pygame

class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, mediapipe_solution):
        pygame.sprite.Sprite.__init__(self)
        self.mediapipe_solution = mediapipe_solution
        self.mediapipe_thread = None
        self.images = []
        self.rect = None
        self.velocity = 0
        self.load_images()
        self.rect.center = [x, y]
        self.is_running = True
        self.flying = False
        self.game_over = False
        self.pygame_frame= None

    def load_images():
        pass

    def process_frame(self, frame):
        self.mediapipe_solution.process_frame(frame)
    
    def start_thread(self):
        #start the Mediapipe thread
        if self.mediapipe_thread is None or not self.mediapipe_thread.is_alive():
            self.mediapipe_thread = threading.Thread(target=self.run_tracking)
            self.mediapipe_thread.start()

    def run_tracking(self):
        #feed in other thread
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        while self.is_running:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)  
                self.process_frame(frame) #initialize processing frame
                #no need to use processed frame
                #self.pygame_image = pygame.image.frombuffer(processed_frame.tobytes(), (800, 600), "RGB")
                self.pygame_frame = pygame.image.frombuffer(frame.tobytes(), (800, 600), "BGR")
        cap.release()
      
    def stop_thread(self):
        #for stop thread
        self.is_running = False
        if self.mediapipe_thread and self.mediapipe_thread.is_alive():
            self.mediapipe_thread.join()

    def reset(self):
        self.pygame_frame = None
        self.rect.y = 300
        self.rect.x = 150
        self.velocity = 0
        self.game_over = False

class Dog(BaseCharacter):
    def __init__(self, x, y):
        mediapipe_solution = NoseTracking()  # Specific Mediapipe solution for this character
        super().__init__(x, y, mediapipe_solution)
        self.counter = 0
        self.index = 0

    def load_images(self):
        for i in range(1, 7):
            image = pygame.image.load(f'graphics\character\doggy/{i}.png')
            image_size = image.get_size()
            image = pygame.transform.scale(image,(image_size[0]*1/3,image_size[0]*1/3))
            self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def process_frame(self, frame):
        self.mediapipe_solution.process_frame(frame)
    
    def update(self):
        self.counter +=1
        reset = 15

        if self.flying == True and self.mediapipe_solution.face_landmarks == None:   
            #for gravity
            self.velocity +=0.5
            if self.velocity > 5: #take limit
                self.velocity == 5
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity)  
        if self.game_over == False : 
            #for animation       
            if self.counter >= reset:
                self.index +=1 
                self.counter = 0
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index] #just update it 
            if self.mediapipe_solution.face_landmarks:
                self.rect.x = self.mediapipe_solution.nose_position_x
                self.rect.y = self.mediapipe_solution.nose_position_y
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-75) 
            self.velocity +=1
            if self.velocity > 5: #take limit
                self.velocity == 10
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) #y-coodinate of rect and image  
            

    def reset(self):
        super().reset()
        self.image = pygame.transform.rotate(self.images[self.index],0)


class Hippo(BaseCharacter):
    def __init__(self, x, y):
        mediapipe_solution = MountTracking()  # Specific Mediapipe solution for this character
        super().__init__(x, y, mediapipe_solution)
        self.counter = 0
        self.index = 0
        self.sound = pygame.mixer.Sound('sound\clicksound01.wav')

    def load_images(self):
        for i in range(1, 4):
            image = pygame.image.load(f'graphics\character\Hippo/{i}.png')
            image_size = image.get_size()
            image = pygame.transform.scale(image,(image_size[0]*1/3,image_size[0]*4/15))
            self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.mount = False

    def process_frame(self, frame):
        self.mediapipe_solution.process_frame(frame)
    
    def update(self):
        self.counter +=1
        reset = 15

        if self.flying == True:   
            #for gravity
            self.velocity +=0.5
            if self.velocity > 5: #take limit
                self.velocity == 5
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) 

        if self.game_over == False:
            if self.counter >= reset:
                self.index +=1 
                self.counter = 0
                if self.index >= len(self.images): #reset when iterable idex will cautch en index out of range
                    self.index = 0
            self.image = self.images[self.index] #just update it 
            #flape
            if self.mediapipe_solution.mount_state == 'open' and self.mount == False:
                self.velocity = -7
                self.sound.play()
                self.mount = True
            if self.mediapipe_solution.mount_state == 'closed' and self.mount == True:
                self.mount = False

                #img rotation
            self.image = pygame.transform.rotate(self.images[self.index],self.velocity *-1.5) #radiouse to rotate 
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-75) 

class Capybara(BaseCharacter):
    def __init__(self, x, y):
        mediapipe_solution = HandTracking()  # Specific Mediapipe solution for this character
        super().__init__(x, y, mediapipe_solution)
        self.counter = 0
        self.index = 0
        self.prev_y = y
       
    def load_images(self):
        image = pygame.image.load(f'graphics\character\capybara/1.png')
        image_size = image.get_size()
        image = pygame.transform.scale(image,(image_size[0]*1/3,image_size[0]*1/3))
        self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
    def process_frame(self, frame):
        self.mediapipe_solution.process_frame(frame)
        # return frame no need to retrun processing frame
    
    def update(self):   
        self.counter +=1
        reset = 15     
        if self.flying == True and self.mediapipe_solution.hand_landmarks == None:   
            #for gravity
            self.velocity +=0.5
            if self.velocity > 5: #take limit
                self.velocity == 5
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) #y-coodinate of rect and image  
        if self.game_over == False :        
            if self.mediapipe_solution.hand_landmarks:
                self.rect.x = self.mediapipe_solution.index_finger_position_x
                self.rect.y = self.mediapipe_solution.index_finger_position_y
 
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-75) 
            self.velocity +=1
            if self.velocity > 5: #take limit
                self.velocity == 10
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) #y-coodinate of rect and image  

    def reset(self):
        super().reset()
        self.image = pygame.transform.rotate(self.images[self.index],0) 

class Chicken(BaseCharacter):
    def __init__(self, x, y):
        mediapipe_solution = PoseTracking()  # Specific Mediapipe solution for this character
        super().__init__(x, y, mediapipe_solution)
        self.counter = 0
        self.index = 0
        self.sound = pygame.mixer.Sound('sound\clicksound01.wav')

    def load_images(self):
        for i in range(1, 3):
            image = pygame.image.load(f'graphics\character\chicken/{i}.png')
            image_size = image.get_size()
            image = pygame.transform.scale(image,(image_size[0]*1/3,image_size[0]*4/15))
            self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.flap = False

    def process_frame(self, frame):
        frame = self.mediapipe_solution.process_frame(frame)
        return frame
    
    def update(self):
        if self.flying == True:   
            #for gravity
            self.velocity +=0.175
            if self.velocity > 2: #take limit
                self.velocity == 2
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) #y-coodinate of rect and image
        
        if self.game_over == False:
            #flape
            if self.mediapipe_solution.flap_state == 'raise' and self.flap == False:    
                self.sound.play()
                self.index = 1
                self.flap = True
            if self.mediapipe_solution.flap_state == 'down' and self.flap == True:
                self.index = 0
                self.velocity = -7
                self.flap = False
                #img rotation
            self.image = pygame.transform.rotate(self.images[self.index],self.velocity *-1.5) #radiouse to rotate 
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-75) 

class Owl(BaseCharacter):
    def __init__(self, x, y):
        mediapipe_solution = EyesTracking()  # Specific Mediapipe solution for this character
        super().__init__(x, y, mediapipe_solution)
        self.counter = 0
        self.index = 0
        self.flap = False
        self.sound = pygame.mixer.Sound('sound\clicksound01.wav')

    def load_images(self):
        for i in range(1, 5):
            image = pygame.image.load(f'graphics\character\owl/{i}.png')
            image_size = image.get_size()
            image = pygame.transform.scale(image,(image_size[0]*1/3,image_size[0]*4/15))
            self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
    def process_frame(self, frame):
        frame = self.mediapipe_solution.process_frame(frame)
        return frame
    
    def update(self):
        if self.flying == True:   
            #for gravity
            self.velocity +=0.25
            if self.velocity > 2.5: #take limit
                self.velocity == 2.5
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) #y-coodinate of rect and image

        if self.game_over == False:

            #flape
            if self.mediapipe_solution.eye_state == 'open'\
                and self.flap == False:
                self.index = 0    
                self.sound.play()
                self.flap = True
            if self.mediapipe_solution.eye_state == 'closed' \
                 and self.flap == True:
                self.index = random.choice([1,3])
                self.velocity = -5
                self.flap = False
                #img rotation
            self.image = pygame.transform.rotate(self.images[self.index],self.velocity *-1.5)
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-75) 

class Obstacle(pygame.sprite.Sprite): 
    def __init__(self,speed, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.width = 80
        self.height = 80
        self.image = pygame.image.load(image_path)  # Load image specific to movement type
        self.image = pygame.transform.scale(self.image, (self.width,self.height))  # Rese imageiz
        self.rect = self.image.get_rect()
        self.speed = speed
    def update(self):
        #self.rect.x -= self.speed  # Common behavior: move left
        if self.rect.x < -60 or self.rect.y > 700 :  # Remove when off-screen
            self.kill()

class HorizonRock(Obstacle):
    def __init__(self,speed):
        super().__init__(speed, 'graphics\obstacle\driftwood.png')  
        self.rect.y = random.randint(40,550)
        self.rect.x = 860
    def update(self):
        super().update()
        self.rect.x -= self.speed #

class Diagonal(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics\obstacle/rock.png')  
        self.rect.x = random.randint(150,800)
    def update(self):
        super().update()
        self.rect.x -=7
        self.rect.y += 7  

class VerticalRock(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics\obstacle/fallingrock.png')  
        self.rect.x = random.randint(150,800)
        self.rect.y  = -40
    def update(self):
        super().update()
        self.rect.x -= 5
        self.rect.y += self.speed  

class Sinusoidal(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics\obstacle/terriblelang.png')  # Specific image for Sinusoidal
        self.angle = 0
        self.rect.x = 860
        self.rect.y = random.randint(50,560)
    def update(self):
        super().update()
        self.rect.y += int(10 * math.sin(self.angle))  # Move in a wave
        self.angle += 0.1
        self.rect.x -= self.angle
    
class Oscillating(Obstacle):
    def __init__(self,speed):
        super().__init__(speed, 'graphics\obstacle\Ftranscript.png')  # Specific image for Oscillating
        self.angle = 0
        self.rect.x = 860
        self.rect.y = random.randint(30,560)
    def update(self):
        super().update()
        self.rect.x -= self.speed
        self.rect.y += int(5 * math.sin(self.angle))  # Oscillating up and down
        self.angle += 0.1

class Zigzag(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics\obstacle/ballwiththrones.png')
        self.rect.x = 840 #starting position x
        self.rect.y = random.randint(30, 550)  #random vertical start position
        self.direction = 1  # 1 for down -1 for up
       

    def update(self):
        super().update()  
        self.rect.y += self.direction * 5
        self.rect.x -= self.speed
        if self.rect.y <= 40 or self.rect.y >= 550:
            self.direction *= -1

class Accelerating(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics\obstacle\missilewithF.png')  
        self.rect.x = 860
        self.rect.y = random.randint(30, 560)
    def update(self):
        super().update()
        self.rect.x -= self.speed
        self.speed += 0.25 

class Bouncing(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics/horiob/horiob01.png')  # Image for bouncing movement
        self.rect.x = 860
        self.rect.y = random.randint(30, 560)
        self.vertical_speed = 4  # Speed of bouncing up/down

    def update(self):
        super().update()
        # Bounce between the top and bottom of the screen
        self.rect.y += self.vertical_speed
        self.rect.x -=self.speed
        if self.rect.y <= 30 or self.rect.y >= 550:
            self.vertical_speed *= -1  # Reverse direction when hitting screen bounds
class Teleporting(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics/horiob/horiob10.png')  # Image for teleporting movement
        self.rect.x = 860
        self.rect.y = random.randint(30, 560)
        self.teleport_timer = pygame.time.get_ticks()

    def update(self):
        super().update()
        current_time = pygame.time.get_ticks()
        if current_time - self.teleport_timer > 3000:  # Teleport every 3 seconds
            self.rect.x = random.randint(860, 1000)  # Teleport to a random x position
            self.teleport_timer = current_time
class RotatingAroundPoint(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics/horiob/horiob01.png')  
        self.center_x = 860  
        self.center_y = random.randint(100, 500) 
        self.radius = 40  
        self.angle = 0 

    def update(self):    
        self.center_x-= self.speed
        self.rect.x = self.center_x + int(self.radius * math.cos(self.angle))
        self.rect.y = self.center_y + int(self.radius * math.sin(self.angle))       
        self.angle += 0.05  
        super().update() 

class Pipe(pygame.sprite.Sprite):
        def __init__(self,x,y,ref,speed):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('graphics/screen1/sat.png')
            self.rect = self.image.get_rect()
            self.scrolling_speed = speed
            #ref =1 is top ,ref = -1 if from the bottom
            if ref == 1:
                self.image = pygame.transform.flip(self.image,False,True)
                self.rect.bottomleft = [x,y]
            else:
                self.rect.topleft = [x,y]

        def update(self):
            self.rect.x -= self.scrolling_speed 
            if self.rect.x < -65: 
                self.kill() #this method gonna kill this sprite object

class Item(pygame.sprite.Sprite):
        def __init__(self,x,y,speed):
            pygame.sprite.Sprite.__init__(self)
            self.scrolling_speed = speed
            i = random.randint(1,8)
            self.image = pygame.image.load(f'graphics\item/{i}.png')
            self.size = self.image.get_size()
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image,((self.size[0]*1/2),(self.size[1]*1/2)))
            self.rect.center = [x,y]
        def update(self):
            self.rect.x -= self.scrolling_speed
            if self.rect.x < -30:
                self.kill()

class Ground(pygame.sprite.Sprite):
        def __init__(self,speed):
            pygame.sprite.Sprite.__init__(self)
            self.scrolling_speed = speed
            self.image = pygame.image.load('graphics\screen1\groundfinal.png')
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.topleft = [self.rect.x,495]

        def update(self):
            if self.rect.x > -400:
                self.rect.x -= self.scrolling_speed
            else:
                self.rect.x = 0

class Cloud(pygame.sprite.Sprite):
        def __init__(self,x,y,speed):
            pygame.sprite.Sprite.__init__(self)
            self.scrolling_speed = speed
            self.image = pygame.image.load('graphics\menuscreen\clound.png')
            size_x = random.randint(100,300)
            size_y = int(size_x*9/16)
            self.image = pygame.transform.scale(self.image,(size_x,size_y))
            self.rect = self.image.get_rect()
            self.rect.center = [x,y]
        def update(self):
            self.rect.x -= self.scrolling_speed
            if self.rect.x < -450:
                self.kill()   

class Mountain(pygame.sprite.Sprite):
        def __init__(self,x,y,speed):
            pygame.sprite.Sprite.__init__(self)
            self.scrolling_speed = speed
            self.image = pygame.image.load('graphics\menuscreen\mountain.png')
            size_x = random.randint(400,1000)
            size_y = int(size_x*9/16)
            self.image = pygame.transform.scale(self.image,(size_x,size_y))
            self.rect = self.image.get_rect()
            self.rect.bottomleft = [x,y]
        def update(self):
            self.rect.x -= self.scrolling_speed
            if self.rect.x < -1000:
                self.kill()

class Gen_button_from_image(pygame.sprite.Sprite):
    def __init__(self,image_part,x,y,sound=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_part)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked_sound =  pygame.mixer.Sound('sound\zipclick.flac')
        self.sound = sound
        self.click_state = False

    def update(self,cersor_pos = None,clicked = None,released = None):
        pass
                
         # Return 0 if not clicked
    def check_click(self,mouse_click,cersor_pos): #pygame.mouse.get_pressed()
        val =0
        if self.rect.collidepoint(cersor_pos):
            if mouse_click == True and self.click_state == False:
                self.click_state =True
                if self.sound:
                    self.clicked_sound.play()
                val = 1  # Return 1 when the sprite is clicked
            if mouse_click == False and self.click_state == True:
                self.click_state =False
        return val
                      
class Popup(pygame.sprite.Sprite):
    def __init__(self,image_part,x,y,top,sound=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_part)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.size = self.rect.size
        self.original_positon = (x - 0.5*self.size[0],y- 0.5*self.size[1])
        self.topup = self.original_positon[1]- top
        self.clicked_sound = pygame.mixer.Sound('sound\zipclick.flac')
        self.sound = sound
        self.click_state = False
        

    def rotation(self,kind):
        self.image = pygame.transform.rotate(self.image,kind)
    
    def update(self,cersor_pos=None):
        if cersor_pos:
            if self.rect.collidepoint(cersor_pos):
                if self.rect.y > self.topup:
                    self.rect.y -=1
                    #self.rotation(-1)
            else: 
                if self.rect.y <= self.original_positon[1]:
                    self.rect.y +=1      
            
    def check_click(self,mouse_click,cersor_pos): #pygame.mouse.get_pressed()
        val =0
        if self.rect.collidepoint(cersor_pos):
            if mouse_click == True and self.click_state == False:
                self.click_state =True
                if self.sound:
                    self.clicked_sound.play()
                val = 1  # Return 1 when the sprite is clicked
            if mouse_click == False and self.click_state == True:
                self.click_state =False
        return val

class Txt_render(pygame.sprite.Sprite):
    def __init__(self,txt,color,x,y,font_size):
        pygame.sprite.Sprite.__init__(self)
        self.font_size = font_size
        self.font = pygame.font.Font('font\Insideman-BLd2V.ttf',self.font_size)
        self.txt = txt
        self.color = color
        self.image = self.font.render(str(self.txt),True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self):
        self.image = self.font.render(str(self.txt),True,self.color)
        



        

