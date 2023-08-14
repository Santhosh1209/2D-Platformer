import pygame
from pygame.locals import *

clock = pygame.time.Clock()
fps = 60

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
            pygame.draw.rect(screen,(255,255,255),tile[1],2) #displays all the rectangles with white colour (255,255,255) and thickness of 2


class Player():
    def __init__(self,x,y):
        self.images_right=[]
        self.images_left=[]
        self.index = 0
        self.counter = 0 #used to control the animation speed as we can't control the loop's iteration speed
        for num in range (1,5):
            img_right = pygame.image.load(f'img/guy{num}.png') #loops b/w images guy1 -> guy4, hence forming an animation
            img_right = pygame.transform.scale(img_right,(20,40))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right) #adds all right images onto the list
            self.images_left.append(img_left) #adds all left images onto the list
        self.image = self.images_right[self.index] #first, gets the list's first element. Then, it gets all the elements based on the index
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0 #velocity of jumping in y direction 
        self.jumped = False
        self.direction = 0 #used to check if the player faces left/right 
    
    def update(self):
        
        #dy and dx denote the changes in the x and y co ordinates 
        dx = 0
        dy = 0
        walk_cooldown = 5
        
        #getting keypresses
        key = pygame.key.get_pressed() #setting up connection with the keyboard
        if key[pygame.K_UP] == True and self.jumped == False:
            self.jumped = True
            self.vel_y = -10 #-ve indicates that the characater would go UP the screen (y co ordinate)
        if key[pygame.K_UP] == False:
            self.jumped = False
        if key[pygame.K_LEFT] == True:
            dx -=5 #moves left, 5 pixels at a time
            self.counter +=1
            self.direction = -1
        if key[pygame.K_RIGHT] == True:
            dx +=5 #moves right, 5 pixels at a time
            self.counter +=1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.index = 0
            self.counter = 0
            #based on if the player is facing left or right, self.direction is updated and so, the subsequent still image is used 
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        #adding animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index +=1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        #setting up the jumping limit -> adding gravity
        self.vel_y +=1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y #more the player jumps, dy changes

        #checking for collisions
        for tile in world.tile_list:

            #checking collision in x direction
            if tile[1].colliderect(self.rect.x +dx,self.rect.y,self.width,self.height): #basically we are checking if the player's rectangle (tile[1]) is colliding with any of the tile rectangles.The tile rectangles that the player WILL HIT are specified by giving the x and y co ordinates along with the height and width of that rectangle
                dx = 0

            #checking collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y+dy,self.width,self.height):
                if self.vel_y < 0: #checking  for collision below i.e, jumping
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0: #checking for collision above i.e, falling
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
         

        #updating player co ordinates based on their movement 
        self.rect.x += dx
        self.rect.y += dy

        #making sure the player stays on the screen
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        #loading player onto the screen
        screen.blit(self.image,self.rect)



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
player = Player(100,screen_height-65)

run = True #acts as the controller to keep the make the screen visible at all times 
while run == True:

    clock.tick(fps) #fixing the frame rate so it runs the same on all devices

    #blit functions are used to display image files onto the screen
    #syntax : image,(x,y) -> x and y co ordinates
    screen.blit(bg_img,(0,0)) # fills entire screen
    screen.blit(sun_img,(50,50)) # top left
    world.draw()
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #used to close the game window

    pygame.display.update() #most important line to implement all the functions like blit
pygame.quit()