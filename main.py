import pygame
from pygame.locals import *
import pickle
from os import path


pygame.init() #initialising pygame

clock = pygame.time.Clock()
fps = 60

screen_height = 500
screen_width =  500

screen = pygame.display.set_mode((screen_width,screen_height)) #displays blank pygame screen
pygame.display.set_caption("2D Platformer")

#defining game variables
tile_size = 25
game_over = 0 #change this based on the events that take place in the game
main_menu = True
level = 1
max_levels = 7

#loading images before entering the screen
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
start_img = pygame.transform.scale(start_img, (150,100))
exit_img = pygame.image.load('img/exit_btn.png')
exit_img = pygame.transform.scale(exit_img, (150,100))

def reset_level(level):
    player.reset(100,screen_height-65)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()

    #loading level data and creating world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data','rb')
        world_data = pickle.load(pickle_in)
        world = World(world_data)

    return world

class Button(): #for adding all kinds of buttons
    def __init__(self,x,y,image): #self represents a class's instance and is required to access any variables or methods within the class
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #geting mouse position
        pos = pygame.mouse.get_pos()

        #check mousover and clicking conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
                #Based on the no specified inside the square brackets, we can deteck clicks
                # [0] -> left click
                # [1] -> right click
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0: #user has released the left key after previously clicking it 
            self.clicked = False


        #draws restart button onto the screen (when the player is dead)
        screen.blit(self.image,self.rect)
        return action


class Player():
    def __init__(self,x,y):
        self.reset(x,y) #everytime the player class is used, init function is called and this contains the reset function
    
    def update(self,game_over):
        
        #dy and dx denote the changes in the x and y co ordinates 
        dx = 0
        dy = 0
        walk_cooldown = 5
        
        if game_over == 0:
            #getting keypresses
            key = pygame.key.get_pressed() #setting up connection with the keyboard
            if key[pygame.K_UP] == True and self.jumped == False and self.in_air == False:
                self.jumped = True
                self.vel_y = -12 #-ve indicates that the characater would go UP the screen (y co ordinate)
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

            #checking for collisions with tiles
            self.in_air = True
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
                        self.in_air = False #i.e., he has hit a tile
        
        #checking for collisions with enemies
            if pygame.sprite.spritecollide(self,blob_group,False):
               game_over = -1
        #checking for collision with lava
            if pygame.sprite.spritecollide(self,lava_group,False):
               game_over = -1
        #checking for collision with exit
            if pygame.sprite.spritecollide(self,exit_group,False):
               game_over = 1
        
        #updating player co ordinates based on their movement 
            self.rect.x += dx
            self.rect.y += dy

        elif (game_over == -1):
            self.image = self.dead_image
            if self.rect.y > 200 :
                self.rect.y -= 5

        #loading player onto the screen
        screen.blit(self.image,self.rect)

        return game_over
    
    def reset(self,x,y):
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
        self.dead_image = pygame.image.load('img/ghost.png')
        self.dead_image = pygame.transform.scale(self.dead_image,(30,30))
        self.image = self.images_right[self.index] #first, gets the list's first element. Then, it gets all the elements based on the index
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0 #velocity of jumping in y direction 
        self.jumped = False
        self.direction = 0 #used to check if the player faces left/right
        self.in_air = True #used to check if the user is touching a tile or he's still mid air

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
                if tile == 3:
                    blob = Enemy(column_count * tile_size, row_count * tile_size + 10)
                    blob_group.add(blob) #every blob occurance is added to this group
                if tile == 6:
                    lava = Lava(column_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 8:
                    exit = Exit(column_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                column_count+=1
            row_count+=1
            
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen,(255,255,255),tile[1],2) #displays all the rectangles with white colour (255,255,255) and thickness of 2

#Creating an Ememy class and making it a child of the Sprite class (already present in pygame module)
class Enemy(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/blob.png')
        self.image = pygame.transform.scale(img,(20,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1 #to check if the blob should move in the left or right direction
        self.move_counter = 0
    
    def update(self): #for movement of blob
        self.rect.x += self.move_direction #movement in right direction
        self.move_counter += 1
        if abs(self.move_counter) > 25:
            self.move_direction *= -1 #movement in left direction (from -25 to 24 and then the cycle repeats)
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img,(tile_size,tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1 #to check if it should move in the left or right direction
        self.move_counter = 0

class Exit(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img,(tile_size,tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1 #to check if it should move in the left or right direction
        self.move_counter = 0


player = Player(100,screen_height-65)

blob_group = pygame.sprite.Group() #Groups are like lists for the Sprite class
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#loading level data to create world
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data','rb')
    world_data = pickle.load(pickle_in)
    world = World(world_data)

#buttons
restart_button = Button(screen_width//2 - 25,screen_height//2 +50, restart_img)
start_button = Button(screen_width//2 - 175, screen_height//2, start_img)
exit_button = Button(screen_width//2 + 50,screen_height//2, exit_img)

run = True #acts as the controller to keep the make the screen visible at all times 
while run == True:

    clock.tick(fps) #fixing the frame rate so it runs the same on all devices

    #blit functions are used to display image files onto the screen
    #syntax : image,(x,y) -> x and y co ordinates
    screen.blit(bg_img,(0,0)) # fills entire screen
    screen.blit(sun_img,(50,50)) # top left

    if main_menu == True:
        if exit_button.draw() == True:
            run = False
        if start_button.draw() == True:
            main_menu = False
    else:
        world.draw()
        if game_over == 0:
            blob_group.update() #this way, the blobs stop moving when game_over != 0

        blob_group.draw(screen) #sprite already has a draw method that's been pre definedd
        lava_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over) #once game_over is -1, the game halts

        if game_over == -1: #player has died
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0

        if game_over == 1:#played has completed that level
            level+=1
            if level <= max_levels:
                #reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #used to close the game window

    pygame.display.update() #most important line to implement all the functions like blit
pygame.quit()