import pygame
from pygame.locals import *

pygame.init() #initialising pygame

screen_height = 600
screen_width = 600

screen = pygame.display.set_mode((screen_width,screen_height)) #displays blank pygame screen
pygame.display.set_caption("2D Platformer")

#loading images before entering the screen
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')

run = True #acts as the controller to keep the make the screen visible at all times 
while run == True:

    # blit functions are used to display image files onto the screen
    # syntax : image,(x,y) -> x and y co ordinates
    screen.blit(bg_img,(0,0)) #fills entire screen
    screen.blit(sun_img,(100,100)) #top left

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #used to close the game window

    pygame.display.update() #most important line to implement all the functions like blit
pygame.quit()