import pygame
import pickle
from os import path

pygame.init()

clock=pygame.time.Clock()
fps=60
screen_width=900
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
tile_size=50
level=1
main_menu = True

bg=pygame.image.load("img/bg.jpg")
bg=pygame.transform.scale(bg,(900,600))
char=pygame.image.load("img/Boat.png")
start_img=pygame.image.load('Img/start.png')
start_img=pygame.transform.scale(start_img,(200,100))
Title=pygame.image.load("Img/Title.png")
Title=pygame.transform.scale(Title,(600,200))


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
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)
        for tile in world.tile_list:
            if tile[1].colliderect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2):
                tile_index = world.tile_list.index(tile)
                if not tile[2]:  # Check if the block is visible
                    world.tile_list[tile_index] = (tile[0], tile[1], True)  # Set block visibility to True


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
                self.pulse = Sonar(self.rect.x + self.width // 2, self.rect.y + self.height // 2, 2)
                self.pulse.deployed = True
                # pygame.mixer.Sound(sonar_sound)
                self.pulse_cooldown = self.pulse_cooldown_max
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
                    self.pulse.size += 2
                    self.pulse.display()

        if self.pulse:
                if self.pulse.deployed:
                    self.pulse.size += 2
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
                    tile=(img,img_rect, False)
                    self.tile_list.append(tile)
                if tile == 2:
                    img=pygame.transform.scale(Stone,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False)
                    self.tile_list.append(tile)
                if tile == 3:
                    img=pygame.transform.scale(Sand,(tile_size//2,tile_size//2))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False)
                    self.tile_list.append(tile)
                if tile == 4:
                    img=pygame.transform.scale(Stone,(tile_size//2,tile_size//2))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False)
                    self.tile_list.append(tile)
                if tile == 5:
                    img=pygame.transform.scale(Sand,(tile_size,tile_size//18))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False)
                    self.tile_list.append(tile)
                if tile == 6:
                    img=pygame.transform.scale(Sand,(tile_size//18,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect, False)
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
        world.tile_list[index] = (tile[0], tile[1], False)  # Reset block visibility to False
    player.pulse = None  # Reset the pulse object
    return 0  # Set game_over to 0 indicating the game is not over

player=Player(screen_width//2,screen_height - 450)
start_button=Button(screen_width//2-110,screen_height//2+60,start_img)

if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world=World(world_data)

game_over=0
run=True
while (run==True):
    clock.tick(fps)
    screen.blit(bg,(0,0))
    if main_menu==True:
        screen.blit(Title,(screen_width//2-300,screen_height//2-160))
        #Displaying button to main menu screen
        if start_button.draw():
            main_menu=False
    else:
        world.draw()
        # draw_grid()
        if player.pulse:  # Check if pulse object exists
            player.pulse.display()
        game_over=player.update(game_over)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = reset_game(player, world)
    # To enable screen refresh so that everything will be visible
    pygame.display.update()

pygame.quit()