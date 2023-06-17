import pygame
import pickle
import subprocess
import pygame.font
import re
from os import path
from pygame import mixer



pygame.init()

clock=pygame.time.Clock()
fps=60
screen_width=900
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
tile_size=50
level=1
main_menu = True
input_rect = pygame.Rect(10, 20, 10, 20)
rate = 2
input_active = False
rate_input = ""
maxSize = 200
input_active2 = False
freq_input = ""

bg=pygame.image.load("img/bg.png")
bg=pygame.transform.scale(bg,(900,900))
char=pygame.image.load("img/Boat.png")
start_img=pygame.image.load('Img/start.png')
start_img=pygame.transform.scale(start_img,(300,300))
editor_img=pygame.image.load('Img/editor.png')
editor_img=pygame.transform.scale(editor_img,(380,380))
Title=pygame.image.load("Img/Title.png")
Title=pygame.transform.scale(Title,(600,200))
font = pygame.font.Font(None, 24)

depth0 = font.render("0m", True, (255, 255, 255))
depth0_rect = depth0.get_rect()
depth0_rect.topright = (900,151)
depth1 = font.render("50m", True, (255, 255, 255))
depth1_rect = depth1.get_rect()
depth1_rect.topright = (900,201)
depth2 = font.render("100m", True, (255, 255, 255))
depth2_rect = depth2.get_rect()
depth2_rect.topright = (900,251)
depth3 = font.render("150m", True, (255, 255, 255))
depth3_rect = depth3.get_rect()
depth3_rect.topright = (900,301)
depth4 = font.render("200m", True, (255, 255, 255))
depth4_rect = depth4.get_rect()
depth4_rect.topright = (900,351)
depth5 = font.render("250m", True, (255, 255, 255))
depth5_rect = depth5.get_rect()
depth5_rect.topright = (900,401)
depth6 = font.render("300m", True, (255, 255, 255))
depth6_rect = depth6.get_rect()
depth6_rect.topright = (900,451)
depth7 = font.render("350m", True, (255, 255, 255))
depth7_rect = depth7.get_rect()
depth7_rect.topright = (900,501)
depth8 = font.render("400m", True, (255, 255, 255))
depth8_rect = depth8.get_rect()
depth8_rect.topright = (900,551)
depth9 = font.render("450m", True, (255, 255, 255))
depth9_rect = depth9.get_rect()
depth9_rect.topright = (900,601)


pygame.mixer.music.load("SFX/ocean_sound.mp3")
pygame.mixer.music.play(-1,0.0,5000)
sonar_sound = pygame.mixer.Sound("SFX/sonar_sound.mp3")
sonar_sound.set_volume(0.2)



def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
                
class Button():
    def __init__(self,x,y,image):
        self.image= image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.clicked=False
    #To draw buttons onto game screen
    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        #Setting collision points between mouse cursor and button area
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==True and self.clicked==False:
                action=True
                self.clicked=True

        if pygame.mouse.get_pressed()[0]==False:
            self.clicked=False
        screen.blit(self.image,self.rect)
        return action
    
class Sonar:
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.size=size
        self.color=(255,255,255)
        self.thickness=1
        self.deployed=False
        self.start_time = 0 
    def display(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)
        for tile in world.tile_list:
            if tile[1].colliderect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2):
                tile_index = world.tile_list.index(tile)
                if not tile[2] and tile[3]:  # Check if the block is visible and changeable
                    world.tile_list[tile_index] = (tile[0], tile[1], True, elapsed_time)  # Set block visibility and elapsed time
            if tile[2]:  # Check if the block is visible
                elapsed_time_text = str(tile[3] // 1000) + "s"  # Convert elapsed time to seconds and create text
                text_surface = pygame.font.Font(None, 20).render(elapsed_time_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=tile[1].center)
                screen.blit(text_surface, text_rect)
            

x=50
y=425
pulse=Sonar(x,y,15)
class Player():
    def __init__(self,x,y):
        self.reset(x,y)
        self.pulse = None
        self.pulse_cooldown = 0
        self.pulse_cooldown_max = 300
    
    def update(self,game_over):
        dx=0
        dy=0
        walk_cooldown=10
        if self.pulse_cooldown > 0:
            self.pulse_cooldown -= 1
        if game_over==0:
            #Adding keypresses for movement using pygame function
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.pulse_cooldown == 0:
                sonar_sound.play()
                self.pulse = Sonar(self.rect.x + self.width // 2, self.rect.y + self.height // 2, 2)
                self.pulse.deployed = True
                self.pulse_cooldown = self.pulse_cooldown_max
                self.pulse.start_time = pygame.time.get_ticks()
            if key[pygame.K_a]:
                dx -= 2
                self.direction=-1
                self.counter+=1
            if key[pygame.K_d]:
                dx += 2
                self.direction=1
                self.counter+=1
            if key[pygame.K_d]==False and key[pygame.K_a]==False:
                self.counter=0
                self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction== -1:
                    self.image=self.images_left[self.index]
            
            
            #Animation Process
            if self.counter > walk_cooldown:
                self.counter=0
                self.index+=1
                if self.index>= len(self.images_right):
                    self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction== -1:
                    self.image=self.images_left[self.index]
                
            # Adding Gravity           
            self.vel_y+=1
            if self.vel_y>20:
                self.vel_y=20
            dy+=self.vel_y
            self.in_air=True

            #Adding collision for blocks in world data
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                    dx=0
                if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                    if self.vel_y>=0:
                        dy=tile[1].top-self.rect.bottom
                        self.vel_y=0
                        self.in_air=False

            self.rect.x += dx
            self.rect.y += dy
            
            if self.pulse_cooldown > 0:
                self.pulse_cooldown -= 1

            
            if self.pulse:
                if self.pulse.deployed:
                    self.pulse.x = self.rect.x + self.width // 2
                    self.pulse.y = self.rect.y + self.height // 2
                    if self.pulse.size < maxSize:  # Check if pulse size is within the limit
                        self.pulse.size += rate
                    self.pulse.display()


        screen.blit(self.image,self.rect)
        return game_over
    #For reseting player after change of levels
    def reset(self,x,y):
        self.images_right=[]
        self.images_left=[]
        self.index=0
        self.counter=0
        #Adding walk animation keyframes into lists which is itterated and drawn onto screen in the main game loop
        for num in range(1,5):
            img_right=pygame.image.load('Img/Boat.png')
            img_right=pygame.transform.scale(img_right,(50,60))
            img_left=pygame.transform.flip(img_right,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image=self.images_right[self.index]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.vel_y=0
        self.direction=0


       
class World():
    def __init__(self,data):
        self.tile_list=[]

        Sand = pygame.image.load('Img/sand.png')
        Stone = pygame.image.load('Img/stone.png')
        row_counter = 0

        for row in data:
            column_counter=0
            for tile in row:
                if tile == 1:
                    img=pygame.transform.scale(Sand,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False, True)
                    self.tile_list.append(tile)
                if tile == 2:
                    img=pygame.transform.scale(Stone,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False, True)
                    self.tile_list.append(tile)
                if tile == 3:
                    img=pygame.transform.scale(Sand,(tile_size//2,tile_size//2))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False, True)
                    self.tile_list.append(tile)
                if tile == 4:
                    img=pygame.transform.scale(Stone,(tile_size//2,tile_size//2))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False, True)
                    self.tile_list.append(tile)
                if tile == 5:
                    img=pygame.transform.scale(Sand,(tile_size,tile_size//18))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False, False)
                    self.tile_list.append(tile)
                if tile == 6:
                    img=pygame.transform.scale(Sand,(tile_size//18,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False, False)
                    self.tile_list.append(tile)
                if tile == 7:
                    img=pygame.transform.scale(Sand,(tile_size//18,tile_size))
                    img = pygame.transform.flip(img, True, False)
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size + 48
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False, False)
                    self.tile_list.append(tile)
                column_counter+=1
            row_counter+=1
    
    def draw(self):
        for tile in self.tile_list:
            if tile[2]:  # Check if the block is visible
                screen.blit(tile[0], tile[1])

def reset_game(player, world):
    player.reset(screen_width // 2, screen_height - 450)
    for index, tile in enumerate(world.tile_list):
        if len(tile) >= 3:  # Check if tile has enough elements
            visibility = tile[2]
            changeability = tile[3] if len(tile) >= 4 else True
            if changeability:
                visibility = False  # Reset block visibility
            world.tile_list[index] = (tile[0], tile[1], visibility, changeability)
    player.pulse = None  # Reset the pulse object
    return 0  # Set game_over to 0 indicating the game is not over

def run_level_editor():
    subprocess.run(['python', 'level_editor.py'])

player=Player(screen_width//2,screen_height - 450)
start_button=Button(screen_width//2+60,screen_height//2+30,start_img)
level_editor=Button(screen_width//2-400,screen_height//2-18,editor_img)
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world=World(world_data)

game_over=0
run=True
while (run==True):
    clock.tick(fps)
    screen.blit(bg,(0,-255))
    if main_menu==True:
        screen.blit(Title,(screen_width//2-300,screen_height//2-200))
        #Displaying button to main menu screen
        if start_button.draw():
            main_menu=False
        if level_editor.draw():
            run_level_editor()
    else:
        world.draw()
        # draw_grid()
        screen.blit(depth0,depth0_rect)
        screen.blit(depth1,depth1_rect)
        screen.blit(depth2,depth2_rect)
        screen.blit(depth3,depth3_rect)
        screen.blit(depth4,depth4_rect)
        screen.blit(depth5,depth5_rect)
        screen.blit(depth6,depth6_rect)
        screen.blit(depth7,depth7_rect)
        screen.blit(depth8,depth8_rect)
        screen.blit(depth9,depth9_rect)
        if player.pulse:  # Check if pulse object exists
            player.pulse.display()
        game_over=player.update(game_over)

    input_surface = font.render("Rate: " + rate_input, True, (255, 255, 255))
    input_rect = input_surface.get_rect()
    input_rect.topleft = (10, 10)
    freq_surface = font.render("Frequency: " + freq_input, True, (255, 255, 255))
    freq_rect = freq_surface.get_rect()
    freq_rect.topleft = (100, 10)
    screen.blit(input_surface, input_rect)
    screen.blit(freq_surface, freq_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = reset_game(player, world)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click occurred within the input field
            if input_rect.collidepoint(event.pos):
                input_active1 = True
                input_active2 = False  # Deactivate the other input field
            else:
                input_active = False
            if freq_rect.collidepoint(event.pos):
                input_active2 = True
                input_active = False  # Deactivate the other input field
            else:
                input_active2 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_active:
                    rate_match = re.search(r'\d+', rate_input)
                    if rate_match:
                        rate = int(rate_match.group())
                    rate_input = ""
                    input_active = False
                if input_active2:
                    freq_match = re.search(r'\d+', freq_input)
                    if freq_match:
                        maxSize = int(freq_match.group())
                    freq_input = ""
                    input_active2 = False
            if event.key == pygame.K_BACKSPACE:
                if input_active:
                    rate_input = rate_input[:-1]
                elif input_active2:
                    freq_input = freq_input[:-1]
            else:
                if input_active and event.unicode.isdigit():
                    rate_input += event.unicode
                elif input_active2 and event.unicode.isdigit():
                    freq_input += event.unicode
        

    # To enable screen refresh so that everything will be visible
    pygame.display.update()

pygame.quit()