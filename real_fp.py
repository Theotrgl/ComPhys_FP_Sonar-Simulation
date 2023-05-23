import pygame
from level import level_1

pygame.init()

clock=pygame.time.Clock()
fps=60
screen_width=900
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
tile_size=50

bg=pygame.image.load("img/bg.jpg")
bg=pygame.transform.scale(bg,(900,600))
char=pygame.image.load("img/charaR1.png")


def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
                
class World():
    def __init__(self,data):
        self.tile_list=[]

        floor_img= pygame.image.load('Img/pixel-platformer-blocks/Tiles/Sand/tile_0025.png')
        row_counter = 0

        for row in data:
            column_counter=0
            for tile in row:
                if tile == 1:
                    img=pygame.transform.scale(floor_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img=pygame.transform.scale(floor_img,(tile_size//2,tile_size//18))
                    img_rect=img.get_rect()
                    img_rect.x=column_counter*tile_size
                    img_rect.y=row_counter*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                column_counter+=1
            row_counter+=1
    
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])

world_data=level_1
world=World(world_data)
run=True
while (run==True):
    clock.tick(fps)
    screen.blit(bg,(0,0))
    world.draw()
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # To enable screen refresh so that everything will be visible
    pygame.display.update()

pygame.quit()