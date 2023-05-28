import pygame
import os
from math import pi
pygame.init()


class Sonar:
    def __init__(self, x,y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255,255,255)
        self.thickness = 1
        self.deployed = False
    def display(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size, self.thickness)
        # pygame.draw.arc(win, "black", [210, 75, 150, 125], 0, pi/2, 2)

# pathnya ganti ke path directoy lu sendiri
path = 'C:/Users/Owen/Documents/GitHub/Semester 4/Computational Physics/shadow_zone'
win = pygame.display.set_mode((500,500))
# pygame.display.set_caption("Shadow Zone")
sonar_sound = pygame.mixer.Sound('C:/Users/Owen/Documents/GitHub/Semester 4/Computational Physics/shadow_zone/sonar_sound.mp3')
ocean_sound = pygame.mixer.music.load('C:/Users/Owen/Documents/GitHub/Semester 4/Computational Physics/shadow_zone/ocean_sound.mp3')
moveLeft = [pygame.image.load(path+'/1.png'),pygame.image.load(path+'/2.png'),pygame.image.load(path+'/3.png'),pygame.image.load(path+'/4.png'),pygame.image.load(path+'/1.png'),pygame.image.load(path+'/2.png'),pygame.image.load(path+'/3.png'),pygame.image.load(path+'/4.png'),pygame.image.load(path+'/1.png')]
moveRight = [pygame.image.load(path+'/5.png'),pygame.image.load(path+'/6.png'),pygame.image.load(path+'/7.png'),pygame.image.load(path+'/8.png'),pygame.image.load(path+'/5.png'),pygame.image.load(path+'/6.png'),pygame.image.load(path+'/7.png'),pygame.image.load(path+'/8.png'),pygame.image.load(path+'/5.png')]
bg = pygame.image.load('C:/Users/Owen/Documents/GitHub/Semester 4/Computational Physics/shadow_zone/wbg.jpg')
char = pygame.image.load(path+'/9.png')
obstacle = pygame.image.load(path+'/A.png')

clock = pygame.time.Clock()
# pygame.mixer.music.play(-1)

x = 50
y = 425 
width = 64
height = 64
vel = 5
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0
pulse = Sonar(x, y, 15)

def redrawGameWindow():
    global walkCount
    win.blit(bg, (0,0))
    
    if(walkCount + 1 >= 27):
        walkCount = 0
    print(walkCount//3)
    if(left):
        win.blit(moveLeft[walkCount//3], (x,y))
        walkCount += 1

    elif(right):
        win.blit(moveRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        if(walkCount == 0):
            win.blit(char, (x,y))


    if(pulse.deployed):
        pulse.size += 2
        pulse.display()

    pygame.display.update()

run = True
while run:
    clock.tick(27)
    #print(walkCount//3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and x > vel:
        x -= vel
        left = True
        right = False

    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x < 500 - width - vel:
        x += vel
        left = False
        right = True
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and y > vel:
        y -= vel
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and y < 500 - height - vel:
        y += vel
    else:
        right = False
        left = False
        walkCount = 0

    if keys[pygame.K_SPACE]:
        pulse = Sonar(x+char.get_rect().size[0]/2, y+char.get_rect().size[1]/2, 2)
        pulse.deployed = True
        pygame.mixer.Sound.play(sonar_sound)
        walkCount = 0

    redrawGameWindow()

pygame.quit()