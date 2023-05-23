#Import Modules and Level data
import pygame
from pygame.locals import *
from pygame import mixer
from level import level_1

pygame.init()

class Sonar:
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.size=size
        self.color=(255,255,255)
        self.thickness=1
        self.deployed=False
    def display(self):
        pygame.draw.circle(screen,self.color,(self.x, self.y), self.size, self.thickness)

screen = pygame.display.set_mode((700,700))
pygame.display.set_caption("SONAR Simulator")
sonar_sound = pygame.mixer.Sound("SFX/sonar_sound.mp3")
bg_music = pygame.mixer.Sound("SFX/menu.mp3")
boat_R=pygame.image.load("img/boat-r.png")
boat_L=pygame.transform.flip(boat_R,True,False)
bg=pygame.image.load("img/bg.jpg")


clock= pygame.time.Clock()
# pygame.mixer.music.play(-1)

x=50
y=425
width=64
height=64
vel=5
Jump=False
JumpCount=10
left=False
right=False
walkCount=0
pulse=Sonar(x,y,15)

def redrawGameWindow():
    global walkCount
    screen.blit(bg, (0,0))

    if (walkCount+1 >=27):
        walkCount = 0
    print(walkCount//3)
    if(left):
        screen.blit(boat_L[walkCount//3],(x,y))
        walkCount += 1
    elif(right):
        screen.blit(boat_R[walkCount//3],(x,y))
        walkCount += 1
    else:
        if(walkCount==0):
            screen.blit(boat_R, (x,y))

    if(pulse.deployed):
        pulse.size += 2
        pulse.display()
    
    pygame.display.update()

run=True
while (run):
    clock.tick(27)
    # print (walkCount//3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT]or keys[pygame.K_a]) and x>vel:
        x-=vel
        left = True
        right = False
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x<500-width-vel:
        x += vel
        left=False
        right=True
    else:
        right=False
        left=False
        walkCount=0

    if keys[pygame.K_SPACE]:
        pulse = Sonar(x+boat_R.get_rect().size[0]/2, y+boat_R.get_rect().size[1]/2,2)
        pulse.deployed=True
        pygame.mixer.Sound(sonar_sound)
        walkCount = 0

    redrawGameWindow()

pygame.quit()