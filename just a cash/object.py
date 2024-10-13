import pygame
import random 
import math 
from detect4 import MediapipeThread,MountTracking,HandTracking,NoseTracking
pygame.init() #initialize pygame


class hippo(pygame.sprite.Sprite): #inharited from sprite parents (make this class be a part of pygame)
  
    def __init__(self,x,y,flying,game_over):   
        
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
        
        self.flying = flying
        self.game_over = game_over
        #prepare for draw require
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #get properties of ractangle like to refer address
        self.rect.center = [x,y] #pass positon (x,y)<center of rec> to rec

        #for gravity
        self.velocity = 0

        self.mount = False

        self.sound = pygame.mixer.Sound('sound\clicksound01.wav')

    def update(self): #overdrive update
        
            #for animation
        self.counter +=1
        reset = 15

        if self.flying == True:   
            #for gravity
            self.velocity +=0.5
            if self.velocity > 5: #take limit
                self.velocity == 5
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) #y-coodinate of rect and image

        if self.game_over == False:
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
                self.sound.play()
                self.mount = True
            if self.mount_tracking.mount_state == 'closed' and self.mount == True:
                self.mount = False

                #img rotation
            self.image = pygame.transform.rotate(self.images[self.index],self.velocity *-1.5) #radiouse to rotate 
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-75) 

class snake(pygame.sprite.Sprite): #inharited from sprite parents (make this class be a part of pygame)
    def __init__(self,x,y,flying,game_over):   
        pygame.sprite.Sprite.__init__(self)
        self.finger_tracking = HandTracking()
        self.mediapipe_thread = MediapipeThread(self.finger_tracking)
        #load image
        self.images = []
        for i in range(1,5):
            image = pygame.image.load(f'graphics/{i}.png')
            self.images.append(image)

        self.index = 0
        self.counter = 0
        
        self.flying = flying
        self.game_over = game_over

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

        if self.flying == True:   
            #for gravity
            self.velocity +=0.5
            if self.velocity > 5: #take limit
                self.velocity == 5
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) #y-coodinate of rect and image          
        if self.game_over == False:
            #15 frame per one im 
            if self.counter >= reset:
                self.index +=1 
                self.counter = 0
                if self.index >= len(self.images): #reset when iterable idex will cautch en index out of range
                    self.index = 0
            self.image = self.images[self.index] #just update it 

            #flape
            if self.finger_tracking.hand_landmarks:
                    
                self.rect.x = self.finger_tracking.index_finger_position_x
                self.rect.y = self.finger_tracking.index_finger_position_y

            self.image = pygame.transform.rotate(self.images[self.index],self.velocity *-1.5) #radiouse to rotate 
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-75) 

class mosquitoe(pygame.sprite.Sprite): #inharited from sprite parents (make this class be a part of pygame)
    def __init__(self,x,y,flying,game_over):   
        pygame.sprite.Sprite.__init__(self)
        self.nose_tracking = NoseTracking()
        self.mediapipe_thread = MediapipeThread(self.nose_tracking)
        #load image
        self.images = []
        for i in range(1,7):
            image = pygame.image.load(f'graphics\character\doggy\{i}.png') 
            image_size = image.get_size()
            image = pygame.transform.scale(image,(image_size[0]*1/3,image_size[1]*1/3))
            self.images.append(image)

        self.index = 0
        self.counter = 0
        
        self.flying = flying
        self.game_over = game_over

        #prepare for draw require
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #get properties of ractangle like to refer address
        self.rect.center = [x,y] #pass positon (x,y)<center of rec> to rec

        #for gravity
        self.velocity = 0

        self.mount = False

        self.prev_y = 0
        self.prev_x = 0
    def update(self): #overdrive update
        #for animation
        self.counter +=1
        reset = 15

        if self.flying == True:   
            #for gravity
            self.velocity +=0.5
            if self.velocity > 5: #take limit
                self.velocity == 5
            if self.rect.bottom < 540: #make it fallen
                self.rect.y += int(self.velocity) #y-coodinate of rect and image          
        if self.game_over == False :
            
            #15 frame per one im 
            if self.counter >= reset:
                self.index +=1 
                self.counter = 0
                if self.index >= len(self.images): #reset when iterable idex will cautch en index out of range
                    self.index = 0
            self.image = self.images[self.index] #just update it 

            #flape
            if self.nose_tracking.face_landmarks:
                    
                self.rect.x = self.nose_tracking.nose_position_x
                self.rect.y = self.nose_tracking.nose_position_y

            '''
            if self.rect.x - self.prev_x !=0 and abs(self.rect.y - self.prev_y)>15:
                slope = (self.rect.y - self.prev_y)/(self.rect.x - self.prev_x)
                self.prev_y = self.rect.y 
                self.prev_x = self.rect.x 
                self.image = pygame.transform.rotate(self.images[self.index],-100*(slope)) #radiouse to rotate 
                print(slope)
            else:
                pass
                #self.image = pygame.transform.rotate(self.images[self.index],-75) 
            '''

'''
class horizon_obstacle(pygame.sprtie.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
        for i in range(1,5):
            image = pygame.image.load(f'graphics\horiob/horiob{i}')
            self.images.append(image)
        self.image = rd.Random.choice(self.images)
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.
'''
class FloatingObstacle(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed, movement_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics\horiob\horiob01.png')  # Example image for the obstacle

        #create list for store different image obstacle
        self.image = pygame.transform.scale(self.image, (80, 80))  # Resize as needed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.movement_type = movement_type  # Different movement patterns
        self.angle = 0  # For circular movement
        self.direction = 1
        self.teleport_timer = pygame.time.get_ticks()
        self.type = {'horizon_rock':[-7,0,0],
                     'oscillating': [0,int(5 * math.sin(self.angle)),0.1],
                     'sinusoidal': [0,int(20 * math.sin(self.angle)),0.05],             
                     'vertical_rock': [0,7,0.05],             
        }
    def update(self):
        self.rect.x -= self.speed
        # Movement patterns based on type 

        if self.movement_type == 'horizon_rock':  # Rotating around a point
            self.rect.x -=5   
        elif self.movement_type == 'vertical_rock':  # Rotating around a point
            self.rect.y -=5
        elif self.movement_type == 'sinusoidal':  # Floating in a wave-like pattern
            self.rect.y += int(20 * math.sin(self.angle))
            self.angle += 0.05 
        elif self.movement_type == 'oscillating':  # Floating up and down
            self.rect.y += int(5 * math.sin(self.angle))
            self.angle += 0.1
        elif self.movement_type == 'rotating':  # Rotating around a point
            self.angle += 5
        
        elif self.movement_type == 'zigzag':
            self.rect.x -= self.speed
            self.rect.y += self.direction * 5  # Move up or down
            if self.rect.y <= 20 or self.rect.y >= 550:  # Switch direction when hitting the bounds
                self.direction *= -1
           

        elif self.movement_type == 'accelerate':
            self.rect.x -= self.speed
            self.speed += 0.3

        elif self.movement_type == 'teleport':
            self.rect.x -= self.speed
            current_time = pygame.time.get_ticks()
            if current_time - self.teleport_timer > 2000:  # Teleport every 2 seconds
                self.rect.x = random.randint(-100, 800)  # Teleport to a new random x position
                self.teleport_timer = current_time

            self.image = pygame.transform.rotate(self.image, self.angle)
        elif self.movement_type == 'rotating':  # Rotating around a point
            self.angle += 5
            self.image = pygame.transform.rotate(self.image, self.angle)
        
        if self.rect.x < -60 or 600<self.rect.y <0:  # Remove when out of the screen
            
            self.kill()
    

class ZigzagObstacle(pygame.sprite.Sprite):
    def __init__(self,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics\horiob\horiob01.png')
        self.rect = self.image.get_rect()
        self.rect.x = 860
        self.rect.y = random.randint(20,560)
        self.speed = speed
        self.direction = 1  # 1 for down, -1 for up

    def update(self):
        self.rect.x -= self.speed
        self.rect.y += self.direction * 5  # Move up or down
        if self.rect.y <= 50 or self.rect.y >= 550:  # Switch direction when hitting the bounds
            self.direction *= -1
        if self.rect.x < -self.rect.width:
            self.kill()  # Remove obstacle when off-screen


class Obstacle(pygame.sprite.Sprite): #forn home2.2
    def __init__(self,speed, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.width = 80
        self.height = 80
        self.image = pygame.image.load(image_path)  # Load image specific to movement type
        self.image = pygame.transform.scale(self.image, (self.width,self.height))  # Resize image
        self.rect = self.image.get_rect()
        self.speed = speed
    def update(self):
        #self.rect.x -= self.speed  # Common behavior: move left
        if self.rect.x < -60 or self.rect.y > 700 :  # Remove when off-screen
            self.kill()

class HorizonRock(Obstacle):
    def __init__(self,speed):
        super().__init__(speed, 'graphics\obstacle\driftwood.png')  # Specific image for Horizon Rock
        self.rect.y = random.randint(40,550)
        self.rect.x = 860
    def update(self):
        super().update()
        self.rect.x -= self.speed # Move horizontally

class Diagonal(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics\obstacle/rock.png')  # Specific image for Vertical Rock
        self.rect.x = random.randint(150,800)
    def update(self):
        super().update()
        self.rect.x -=7
        self.rect.y += 7  # Move vertically

class VerticalRock(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics\obstacle/fallingrock.png')  # Specific image for Vertical Rock
        self.rect.x = random.randint(150,800)
        self.rect.y  = -40
    def update(self):
        super().update()
        self.rect.x -= 5
        self.rect.y += self.speed  # Move vertically

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
        self.rect.x = 840 # Starting position x
        self.rect.y = random.randint(30, 550)  # Random vertical start position
        self.direction = 1  # 1 for down, -1 for up
       

    def update(self):
        super().update()  # Call the parent class' update method to handle movement to the left
        # Zigzag movement: Move up or down
        self.rect.y += self.direction * 5
        self.rect.x -= self.speed
        # Switch direction when hitting vertical bounds
        if self.rect.y <= 40 or self.rect.y >= 550:
            self.direction *= -1
class Accelerating(Obstacle):
    def __init__(self, speed):
        super().__init__(speed, 'graphics\obstacle\missilewithF.png')  # Image for accelerating movement
        self.rect.x = 860
        self.rect.y = random.randint(30, 560)
    def update(self):
        super().update()
        # Gradually increase speed
        self.rect.x -= self.speed
        self.speed += 0.25 # Accelerate the obstacle over time
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
        super().__init__(speed, 'graphics/horiob/horiob01.png')  # Image for rotating around a point
        self.center_x = 860  # Starting x position for circular movement
        self.center_y = random.randint(100, 500)  # Random starting y point
        self.radius = 40  # Radius of the circular path
        self.angle = 0  # Angle for circular movement

    def update(self):
        # Rotate in a circular path around the center point
        self.center_x-= self.speed
        self.rect.x = self.center_x + int(self.radius * math.cos(self.angle))
        self.rect.y = self.center_y + int(self.radius * math.sin(self.angle))
        
        self.angle += 0.05  # Increase angle to rotate
        super().update()  # Call parent update to move left and handle off-screen logic

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
            self.sound = pygame.mixer.Sound('sound/clicksound01.wav')
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

            self.sound = pygame.mixer.Sound('sound/clicksound01.wav')
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
            self.sound = pygame.mixer.Sound('sound/clicksound01.wav')
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
            self.sound = pygame.mixer.Sound('sound/clicksound01.wav')
        def update(self):
            self.rect.x -= self.scrolling_speed
            if self.rect.x < -1000:
                self.kill()

class Gen_button_from_image(pygame.sprite.Sprite):
    def __init__(self,image_part,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_part)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        cersor_pos = pygame.mouse.get_pos() #index got x and y coordinate
        if self.rect.collidepoint(cersor_pos) and pygame.mouse.get_pressed()[0] == 1:
            return 1
        
class Popup(pygame.sprite.Sprite):
    def __init__(self,image_part,x,y,top):
        pygame.sprite.Sprite.__init__(self)
       
        self.image = pygame.image.load(image_part)
        self.rect = self.image.get_rect()
        
        self.rect.center = (x,y)
        self.size = self.rect.size
        self.original_positon = (x - 0.5*self.size[0],y- 0.5*self.size[1])
        self.topup = self.original_positon[1]- top
        self.click_sound1 = pygame.mixer.Sound('sound\zipclick.flac')
    def rotation(self,kind):
        self.image = pygame.transform.rotate(self.image,kind)

    def update(self):
        cersor_pos = pygame.mouse.get_pos() #index got x and y coordinate
        if self.rect.collidepoint(cersor_pos) and pygame.mouse.get_pressed()[0] == 1:
            self.click_sound1.play()
            return 1
        if self.rect.collidepoint(cersor_pos) and self.rect.y > self.topup:
            
            self.rect.y -=1
            #self.rotation(-1)
            
        if self.rect.collidepoint(cersor_pos) == False and self.rect.y <= self.original_positon[1] :
            self.rect.y +=1
            #self.rotation(1)

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
        



        

