import pygame
from pygame.locals import *

pygame.init() #initialising pygame
screen_height = 500
screen_width =  500

screen = pygame.display.set_mode((screen_width,screen_height)) #displays blank pygame screen
pygame.display.set_caption("2D Platformer")

#defining game variables
tile_size = 25

#loading images before entering the screen
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')

def draw_grid(): #used to draw a bunch of white lines on the screen with x,y co ordinates
    for line in range(0,21):
        pygame.draw.line(screen,(255,255,255),(0,line * tile_size),(screen_width,line * tile_size))
        pygame.draw.line(screen,(255,255,255),(line * tile_size,0),(line * tile_size,screen_height))

class World():
    def __init__(self,data): #constructor that takes the list as input 
        #based on the value present in the list, each tile is filled with the appropriate image
        #data -> world data ultra list

        self.tile_list=[]

        #images
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    #this is used to make the pic fit into the tile space
                    img = pygame.transform.scale(dirt_img,(tile_size,tile_size)) #here tile_size = x and y axis
                    img_rect = img.get_rect() #creates a rectangle for every image based on it's size
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile) #self.tile is a list and all the selected stuff, here that is the values which equal to 1, are appended to it

                if tile == 2:
                    img = pygame.transform.scale(grass_img,(tile_size,tile_size)) 
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)

                column_count+=1
            row_count+=1
            
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])          


world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)

run = True #acts as the controller to keep the make the screen visible at all times 
while run == True:

    # blit functions are used to display image files onto the screen
    # syntax : image,(x,y) -> x and y co ordinates
    screen.blit(bg_img,(0,0)) # fills entire screen
    screen.blit(sun_img,(100,100)) # top left
    world.draw()
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #used to close the game window

    pygame.display.update() #most important line to implement all the functions like blit
pygame.quit()