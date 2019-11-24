import pygame as pg

#game settings
title="Is it GOOD?"
width = 600  #width of the window
height = 400  #height of the window
FPS = 50  #frames per second
FONT_NAME='arial'

#player properties
player_acc=0.5
player_friction=-0.05
gravity=0.98
jumpPower=20

#sprites
walkRight = [pg.image.load('Walk (1).png'), pg.image.load('Walk (2).png'),
             pg.image.load('Walk (3).png'), pg.image.load('Walk (4).png'),
             pg.image.load('Walk (5).png'), pg.image.load('Walk (6).png'),
             pg.image.load('Walk (7).png'), pg.image.load('Walk (8).png'),
             pg.image.load('Walk (9).png')]


walkLeft = [pg.image.load('Walk Left (1).png'), pg.image.load('Walk Left (2).png'),
            pg.image.load('Walk Left (3).png'), pg.image.load('Walk Left (4).png'),
            pg.image.load('Walk Left (5).png'), pg.image.load('Walk Left (6).png'),
            pg.image.load('Walk Left (7).png'), pg.image.load('Walk Left (8).png'),
            pg.image.load('Walk Left (9).png')]

#idle = [pg.image.load('idle (1).png'), pg.image.load('idle (2).png'),
#        pg.image.load('idle (3).png'), pg.image.load('idle (4).png'),
#        pg.image.load('idle (5).png'), pg.image.load('idle (6).png'),
#        pg.image.load('idle (7).png'), pg.image.load('idle (8).png'),
#        pg.image.load('idle (9).png'), pg.image.load('idle (10).png'),
#        ] #I plan to add the idle state but the logic I'm using for walking is not suitable for standing

bg = pg.image.load('background.PNG') 
character = pg.image.load('idle (1).png')


#resizing the sprites
for i in range(len(walkLeft)):
    walkLeft[i] = pg.transform.rotozoom(walkLeft[i], 0, 0.15)

for i in range(len(walkRight)):
    walkRight[i] = pg.transform.rotozoom(walkRight[i], 0, 0.15)



# the idle state if character
character = pg.transform.rotozoom(character, 0, 0.15)



#platforms
platform_list = [(0,height-40,width,40),(width/2-50,height*0.75,100,20),
(125, height-350,300,30),(350,240,100,30),(175,200,50,20)]

#colors
red=(255,0,0)
green=(0,255,0) 
blue=(0,0,255)
white=(255,255,255)
black=(0,0,0)
