import pygame 
from math import*

#game settings.
title="Cat Swing"
width = 1000 #width of the window
height = 626  #height of the window
FPS = 40  #frames per second
FONT_NAME='Curlz MT'

#player properties
player_acc=8
player_friction=-0.5
gravity=0.98
jumpPower=15

#sprites for the game
walkRight = [pygame.image.load('Walk (1).png'),
             pygame.image.load('Walk (2).png'),
             pygame.image.load('Walk (3).png'),
             pygame.image.load('Walk (4).png'),
             pygame.image.load('Walk (5).png'),
             pygame.image.load('Walk (6).png'),
             pygame.image.load('Walk (7).png'),
             pygame.image.load('Walk (8).png'),
             pygame.image.load('Walk (9).png')]

walkLeft = [pygame.image.load('Walk Left (1).png'),
            pygame.image.load('Walk Left (2).png'),
            pygame.image.load('Walk Left (3).png'),
            pygame.image.load('Walk Left (4).png'),
            pygame.image.load('Walk Left (5).png'),
            pygame.image.load('Walk Left (6).png'),
            pygame.image.load('Walk Left (7).png'),
            pygame.image.load('Walk Left (8).png'),
            pygame.image.load('Walk Left (9).png')]

platforms = pygame.image.load('platform1.png')

bg = pygame.image.load('background.PNG') 

character = pygame.image.load('idle (1).png')

gameOver = pygame.image.load('ugh.PNG')

startScreen = pygame.image.load('startScreen.jpg')

instructions = pygame.image.load('instructions.png')

nextlevel = pygame.image.load('nextlevel.png')

platformsmall = pygame.image.load('platform2.png')

#resizing the sprites
for i in range(len(walkLeft)):
    walkLeft[i] = pygame.transform.rotozoom(walkLeft[i], 0, 0.15)

for i in range(len(walkRight)):
    walkRight[i] = pygame.transform.rotozoom(walkRight[i], 0, 0.15)

# the idle state if character
character = pygame.transform.rotozoom(character, 0, 0.15)

II=pygame.image.load('instructions.png') #instructionImage

spike=pygame.image.load('spike.png')
spike=pygame.transform.rotozoom(spike, 0, 0.15)

Bigcoin=pygame.image.load('catcoin.png')
coin=pygame.transform.rotozoom(Bigcoin, 0, 0.15)

big_coin=pygame.image.load('redcoin.PNG')
big_coin=pygame.transform.rotozoom(big_coin, 0, 0.5)

ropestation=pygame.image.load('ropestation.png')
ropestation=pygame.transform.rotozoom(ropestation, 0, 0.1)

levels=pygame.image.load('levels.png')

#level 2 lists,
#lists to create objects in the levels and blit them on the screen accordingly
platform_list2 = [(323,323),(723,400),(1123,250)]
coin_list2=[(390,320),(523,200),(770,250),(923,240)]
ropestation_list2=[(400,100),(520,180),(823,130),(1023,110)]
spike_list2=[(560,523),(1173,300)]
big_coin_list2=[(1123,200)]

#level 3 lists
#level 3 lists fof objects
platform_list3= [(323,323),(523,600),(723,500),(923,400),(11,350)]
coin_list3=[(523,500),(750,450),(923,400),(950,350)]
ropestation_list3=[(823,130),(1023,110)]
spike_list3=[(560,323),(790,390)]
big_coin_list3=[(1023,200)]

#level 1 lists
platform_list = [(350,250),(480,300),(660,250),(920,350),(1025,400)]
coin_list=[(350,175),(500,275),(685,220),(923,320)]
ropestation_list=[(853,120)]
big_coin_list=[(1050,300)]

#level 4 lists
platform_list4 = [(323,323),(523,350),(723,400),(923,300),(1123,250)]
coin_list4=[(350,300),(523,200),(750,290),(923,240)]
ropestation_list4=[(500,100),(823,130),(1023,110)]
spike_list4=[(600,343),(790,390),(1010,300),(1173,300)]
big_coin_list4=[(1123,200)]


#colors
bluish=(228,244,244)
red=(25,5,0,0)
green=(0,255,0) 
blue=(0,0,255)
white=(255,255,255)
black=(0,0,0)

#math vector to keep velovity and acceleretaion on the x and y 
vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        #initilalizing the player group
        pygame.sprite.Sprite.__init__(self)
        self.game=game
        self.i=0
        self.image=character
        self.rect=self.image.get_rect()
        self.rect.center=(width/2,height/2)
        self.position=vector(width*3/8,height/2)
        self.velocity=vector(0,0)
        self.acc=vector(0,0)
        self.aVel=0.0
        self.aAcc=0.0
        self.angle=0.0
        ropestation=Ropestations(500,100)
        self.acceleration=False
        self.bool_swing = False
        self.swinging=True
        self.limit=0.5*pi
        self.delta=0.009


    def jump(self):
        #in life you can not jump twice from one jump
        #if there is a surface underneath you can jump
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.x -= 1
        if hits:
            self.velocity.y=-jumpPower        

    def nearest_ropestations(self):
        #if the player is not already swinging calculate the nearest distance and choose the nearst ropestation
        if self.bool_swing==False:
            #the nearest value is some big number, and we are thrying to find the smallest, from the distances from guven ropestation coordinaates
            nearest_dis = 100000
            for rope in self.game.rope_stations:
                a=sqrt(pow((rope.rect.x-self.position.x),2)+pow((rope.rect.y-self.position.y),2))
                if  a<nearest_dis:
                    nearest_dis=abs(a)
                    nearest_ropestation=rope                   
            return nearest_ropestation

     #while the player swings the angle is changing which changes the velocity and acceleration,
     #to put a limit on swinging we have to restrict the angle between plus and minus values of the first angle so we have to keep the value    
    def firstangle(self):
            rope_st=self.nearest_ropestations()
            length=sqrt(pow(rope_st.rect.x-self.position.x,2)+pow(rope_st.rect.y-self.position.y,2))
            anglelimit=asin((self.position.x-rope_st.rect.x)/length)
            return anglelimit

    def swing(self):
        Aacc=0
        vel=0
        #acess the nearest ropestation coordinates
        #clculate the angle and distance
        rope_st=self.nearest_ropestations()
        length=sqrt(pow(rope_st.rect.x-self.position.x,2)+pow(rope_st.rect.y-self.position.y,2))
        angle=asin((self.position.x-rope_st.rect.x)/length)
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            #player is swinging as long as the user presses the space bar
            self.bool_swing = True
            self.acc=vector(0,0)
            #give the starting acceleration according to the angle
            Aacc=-0.009*sin(angle)
            vel+=Aacc
            angle= angle +self.delta
            #self.velocity=vector(vel,0)
            if angle >=abs(self.limit):
                #change the angle between given oundaries with some delta 
                self.delta = -0.009
            elif angle <= self.limit:
                self.delta = 0.009
            #with the given angle , and station coordinates we can find out the path of the pendulum
            self.position.x=round(rope_st.rect.x+ length * sin(angle))
            self.position.y=round(rope_st.rect.y+ length *cos(angle))
            #make the "rope", between players coordinates and the stations coordinates
            pygame.draw.lines(self.game.screen,(0,0,255), False, [(rope_st.rect.x,rope_st.rect.y), (self.position.x, self.position.y)], 2)
        #if the player is not swinging any more make the bool value False    
        self.bool_swing = False
        pygame.display.update()
        
            
    def update(self):
        self.acc=vector(0,gravity)
        #check which key is ressed on the keyboard
        # if it's the left key move the player left, and blit the matching sprites
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x -= player_acc
            self.image=walkLeft[self.i]
            self.i= (self.i+1)%len(walkLeft)
        # if it's the right key move the player right, and blit sprites accordingly
        if keys[pygame.K_RIGHT]:
            self.velocity.x += player_acc 
            self.image=walkRight[self.i]
            self.i= (self.i+1)%len(walkRight)

        if keys[pygame.K_SPACE]:
            #if its the space bar calculate the first angle to detect the boundaries and find out the path of the swing
            if  self.swinging:
                self.limit = self.firstangle()
                self.swinging = False
            self.swing()
#according to the physics equations give the player velocity and acceleration, use friction slow down the acceleration
        self.acc.x += self.velocity.x*player_friction   
        self.velocity += self.acc
        #change the position according to displacement
        self.position += self.velocity+ 0.5*self.acc
        self.rect.midbottom = self.position
        
#platforms class to use sprites easily, screate and trac the coordinates easily.
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=platforms
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
#ropestation class to create objects and use the coordinates to findthe nearest distance
class Ropestations(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((5,5))
        self.image.fill(green)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#Class for instructions on the main screen
#game rules and levels, use coordinates to blit them on the right place
class Instructions(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=II
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#coins class which helps to detect collisions (with sprite groups) and colllect them,
#coordiantes to scroll them with the window
class coins(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=coin
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#the main red coin, which is the  winning coin, As long as you get the coin you can move to the next level
class Maincoin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=big_coin
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#spikes as obstacles for the player
        #scroll it with the window
class Spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=spike
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#gems-something which is supposed to be on top of the ropestation rectangle
class Gems(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=ropestation
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#small platforms 
class smallPlatforms(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=platformsmall
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        

#main loop of the game


        
class Game:
        def __init__(self):
                #initializing game window
                pygame.init()
                pygame.mixer.init()
                self.screen=pygame.display.set_mode((width,height))
                self.screen.fill(bluish)
                pygame.display.set_caption(title)
                self.clock=pygame.time.Clock()
                self.gameIsON=True
                self.font_name=pygame.font.match_font(FONT_NAME)
                self.score=0
                self.acceleration=False
                self.rope_stations = []
                self.level=1

        def new(self):
            #find out on which level are we, create the objects the level owns
            #once you dye restart window
            #creating groups of sprites to detect collisions
            self.all_sprites=pygame.sprite.Group()
            #platform group
            self.platforms=pygame.sprite.Group()
            #ropestations group
            self.ropestations=pygame.sprite.Group()
            #coins group
            self.coins=pygame.sprite.Group()
            #Mainoin group
            self.Mcoins=pygame.sprite.Group()
            #spike group
            self.spikes=pygame.sprite.Group()
            #ropestation-gem group
            self.gem=pygame.sprite.Group()
            #the player
            self.player=Player(self) 
            self.all_sprites.add(self.player)
            #creating platforms, adding to platforms and all_sprites groups
            for plat in platform_list:
                p = Platform(*plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            #creating coins, adding to coins and all_sprites groups
            for coin in coin_list:
                c = coins(*coin)
                self.all_sprites.add(c)
                self.coins.add(c)
            #creating ropestations, adding to ropestations and all_sprites groups
            for rope in ropestation_list:
                r = Ropestations(*rope)
                self.rope_stations += [r]
                self.all_sprites.add(r)
                self.platforms.add(r)
            #main coin
            for Mcoin in big_coin_list:
                    m=Maincoin(*Mcoin)
                    self.all_sprites.add(m)
                    #self.coins.add(m)
                    self.Mcoins.add(m)
            #ropes
            for gem in ropestation_list:
                    g=Gems(gem[0]-3,gem[1]-3)
                    self.gem.add(g)
                    self.all_sprites.add(g)
            self.gameON()

        def drawLevel2(self):
            #once you dye restart window
            #creating groups of sprites to detect collisions
            self.all_sprites=pygame.sprite.Group()
            #platform group
            self.platforms=pygame.sprite.Group()
            #ropestations group
            self.ropestations=pygame.sprite.Group()
            #coins group
            self.coins=pygame.sprite.Group()
            #Mainoin group
            self.Mcoins=pygame.sprite.Group()
            #spike group
            self.spikes=pygame.sprite.Group()
            #ropestation-gem group
            self.gem=pygame.sprite.Group()
            #the player
            self.player=Player(self) 
            self.all_sprites.add(self.player)
            #creating platforms, adding to platforms and all_sprites groups
            for plat in platform_list2:
                p = Platform(*plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            #creating coins, adding to coins and all_sprites groups
            for coin in coin_list2:
                c = coins(*coin)
                self.all_sprites.add(c)
                self.coins.add(c)
            #creating ropestations, adding to ropestations and all_sprites groups
            for rope in ropestation_list2:
                r = Ropestations(*rope)
                self.rope_stations += [r]
                self.all_sprites.add(r)
                self.platforms.add(r)
            #main coin
            for Mcoin in big_coin_list2:
                    m=Maincoin(*Mcoin)
                    self.Mcoins.add(m)
                    #self.coins.add(m)
                    self.all_sprites.add(m)
  
            for spike in spike_list2:
                    s=Spikes(*spike)
                    self.all_sprites.add(s)
                    self.spikes.add(s)
            for gem in ropestation_list2:
                    g=Gems(gem[0]-3,gem[1]-3)
                    self.gem.add(g)
                    self.all_sprites.add(g)
            self.gameON()                
                
        def drawLevel3(self):
            #once you dye restart window
            #creating groups of sprites to detect collisions
            self.all_sprites=pygame.sprite.Group()
            #platform group
            self.platforms=pygame.sprite.Group()
            #ropestations group
            self.ropestations=pygame.sprite.Group()
            #coins group
            self.coins=pygame.sprite.Group()
            #Mainoin group
            self.Mcoins=pygame.sprite.Group()
            #spike group
            self.spikes=pygame.sprite.Group()
            #ropestation-gem group
            self.gem=pygame.sprite.Group()
            #the player
            self.player=Player(self) 
            self.all_sprites.add(self.player)
            #creating platforms, adding to platforms and all_sprites groups
            for plat in platform_list3:
                p = Platform(*plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            #creating coins, adding to coins and all_sprites groups
            for coin in coin_list3:
                c = coins(*coin)
                self.all_sprites.add(c)
                self.coins.add(c)
            #creating ropestations, adding to ropestations and all_sprites groups
            for rope in ropestation_list3:
                r = Ropestations(*rope)
                self.rope_stations += [r]
                self.all_sprites.add(r)
                self.platforms.add(r)
            #main coin
            for Mcoin in big_coin_list3:
                    m=Maincoin(*Mcoin)
                    self.all_sprites.add(m)
                    #self.coins.add(m)
                    self.Mcoins.add(m)
            for gem in ropestation_list3:
                    g=Gems(gem[0]-3,gem[1]-3)
                    self.gem.add(g)
                    self.all_sprites.add(g)
            self.gameON()
                
        def drawLevel4(self):
            #once you dye restart window
            #creating groups of sprites to detect collisions
            self.all_sprites=pygame.sprite.Group()
            #platform group
            self.platforms=pygame.sprite.Group()
            #ropestations group
            self.ropestations=pygame.sprite.Group()
            #coins group
            self.coins=pygame.sprite.Group()
            #Mainoin group
            self.Mcoins=pygame.sprite.Group()
            #spike group
            self.spikes=pygame.sprite.Group()
            #ropestation-gem group
            self.gem=pygame.sprite.Group()
            #the player
            self.player=Player(self) 
            self.all_sprites.add(self.player)
            #creating platforms, adding to platforms and all_sprites groups
            for plat in platform_list4:
                p = Platform(*plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            #creating coins, adding to coins and all_sprites groups
            for coin in coin_list4:
                c = coins(*coin)
                self.all_sprites.add(c)
                self.coins.add(c)
            #creating ropestations, adding to ropestations and all_sprites groups
            for rope in ropestation_list4:
                r = Ropestations(*rope)
                self.rope_stations += [r]
                self.all_sprites.add(r)
                self.platforms.add(r)
            #main coin
            for Mcoin in big_coin_list4:
                    m=Maincoin(*Mcoin)
                    self.all_sprites.add(m)
                    #self.coins.add(m)
                    self.Mcoins.add(m)
            for spike in spike_list4:
                    s=Spikes(*spike)
                    self.all_sprites.add(s)
                    self.spikes.add(s)
            for gem in ropestation_list4:
                    g=Gems(gem[0]-3,gem[1]-3)
                    self.gem.add(g)
                    self.all_sprites.add(g)
            self.gameON()
            
        def gameON(self):
                #game loop
                self.playing = True
                while self.playing:
                        self.clock.tick(FPS)
                        self.events()
                        self.update()
                        self.draw()
#updaeing game loop
        def update(self):
            self.all_sprites.update()
            #only falling, hitting a platform
            if self.player.velocity.y>0:
                #detecting the collisions , not deleting the sprite
                #if we hit a platform we moe on top of it
                    hits=pygame.sprite.spritecollide(self.player,self.platforms,False)
                    if hits and not self.player.bool_swing:
                            self.player.position.y=hits[0].rect.top
                            self.player.velocity.y=0
            #if we hit a coin we delete the sprite of the coin and increase the coin count, score
            hitCoin=pygame.sprite.spritecollide(self.player,self.coins,True)
            #print(hitCoin)
            if hitCoin:
                self.score+=1
                if self.score>=4:
                    self.next_level_screen()
                    self.level+=1
                    if self.level == 1:
                        self.score=0
                        self.drawLevel2()
                        self.score=0
                    if self.level == 2:
                        self.score=0
                        self.drawLevel3()
                        self.score=0
                    if self.level==3:
                        self.score=0
                        self.drawLevel4()
                        self.score=0
                        
#uf we collected the MainCoin we are done with the level and gained 5 extra points
            Maincoin=pygame.sprite.spritecollide(self.player,self.Mcoins,False)
##                if Maincoin!=[]:
##                    print(Maincoin)
            if Maincoin:
                    self.score+=5
                    #display the nect level screen
                    self.next_level_screen()
                    #move to the next level
                    self.score=0
                    self.level+=1
                    if self.level == 1:
                        self.score=0                        
                        self.drawLevel2()
                        self.score=0

                    if self.level == 2:
                        self.score=0
                        self.drawLevel3()
                        self.score=0
                    if self.level==3:
                        self.score=0
                        self.drawLevel4
                        self.score=0
#if we hit the spike we die
            spikehit=pygame.sprite.spritecollide(self.player,self.spikes,False)
            if spikehit:
                #game is over
                     self.playing = False
                     self.the_gameOver_screen()
                    

                #if player is past half  of the screen from the right scroll it in left direction
            if self.player.rect.right >=abs(width/2):
                    if self.player.velocity.x>0:
                            #scrolling the ropestations
                            self.player.position.x -= abs(self.player.velocity.x)
                            for ropestation in self.ropestations:
                                  ropestation.rect.x-=abs(self.player.velocity.x)
                            #scrolling the coins
                            for coin in self.coins:
                                    coin.rect.x-=abs(self.player.velocity.x)
                            #scrolling the platforms
                            for plat in self.platforms:
                                    plat.rect.x-=abs(self.player.velocity.x)
                            for spike in self.spikes:
                                    spike.rect.x-=abs(self.player.velocity.x)
                            for gem in self.gem:
                                    gem.rect.x-=abs(self.player.velocity.x)
                                        
                #if player is past half  of the screen from the left scroll it in right direction
            if self.player.rect.left<abs(width/2):
                    if self.player.velocity.x<0:
                            self.player.position.x +=abs(self.player.velocity.x)
                            #scrolling the platforms
                            for plat in self.platforms:
                                    plat.rect.x+=abs(self.player.velocity.x)
                            #scrolling the coins
                            for coin in self.coins:
                                    coin.rect.x+=abs(self.player.velocity.x)
                            #scrolling the ropestations
                            for ropestation in self.ropestations:
                                  ropestation.rect.x+=abs(self.player.velocity.x) 
                            for spike in self.spikes:
                                    spike.rect.x+=abs(self.player.velocity.x)                                
                            for gem in self.gem:
                                    gem.rect.x+=abs(self.player.velocity.x)
                                        
            if self.player.rect.bottom>height:
                    #if cat dissapears from the screen the cat is dead
                    self.playing = False
                    self.the_gameOver_screen()

        def events(self):
                #events in the game loop
                for event in pygame.event.get():
                        #closing the screen window either during playing or before starting a game
                        if event.type==pygame.QUIT:
                                if self.playing:
                                        self.playing=False
                                self.gameIsON=False
                                pygame.quit()
                                pygame.init()

                        if event.type==pygame.KEYDOWN:
                                if event.key==pygame.K_UP:
                                        self.player.jump()
                                if event.key==pygame.K_DOWN:
                                        self.pressed=False

                              
        def draw(self):
                #drawing in the game loop
                self.screen.fill(bluish)
                #draw all the sprites on the screen
                self.all_sprites.draw(self.screen)
                pygame.display.flip()
                #the score
                self.draw_text(str(self.score),22,blue,width/2,15)
                pygame.display.flip()
                
        def draw_text(self,text,size,color,x,y):
            #drawing the text on the screen, text surface , font and getting the rectangle of the text
                font=pygame.font.Font(self.font_name,size)
                text_surface=font.render(text,True,color)
                text_rect=text_surface.get_rect()
                text_rect.midtop=(x,y)
                self.screen.blit(text_surface,text_rect)

        def the_start_screen(self):
                #start screen
                self.screen.blit(startScreen,(width//2-315,0))
                self.draw_text(title,48,black,width/2,height*31/64)
                self.draw_text("press S to start",22,black,width/2,height*9/10)
                button = pygame.draw.rect(self.screen,(0,0,240),(785,600,20,20))
                self.draw_text("?",22,black,793,602)
                button = pygame.draw.rect(self.screen,(0,0,240),(185,600,75,20))
                self.draw_text("levels",22,black,225,602)
                pygame.display.flip()
                #waiting fo the user to either start game or close the window
                self.wait_for_key()

        def getHelp(self):
            #instruction image
                instruction=self.screen.blit(instructions,(250,100))
                #button=pygame.draw.rect(self.screen,(255,0,0),(613,480,50,50))
                pygame.display.flip()
                      
        def wait_for_key(self):
                waiting=True
                while waiting:
                        self.clock.tick(FPS)
                        #waiting for the user to take an action, either close the window, or press s and start game
                        for event in pygame.event.get():
                                if event.type==pygame.QUIT:
                                        waiting=False
                                        gameIsON=False
                                if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_s:
                                            #if s is pressed we are not waiting anymore
                                                waiting=False
                                        
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                x = pygame.mouse.get_pos()[0]
                                                y = pygame.mouse.get_pos()[1]
                                                
                                           #the coordinates of the buttons on the screen
                                            #assigning different functions to the buttons
                                                if x>=785 and x<=805:
                                                    if y>=600 and y<=620:
                                                        self.getHelp()
                                                
##                                                if pygame.mouse.get_pos() >= (785,600):
##                                                        if pygame.mouse.get_pos() <= (805,620):
##                                                                print('1')
##                                                                self.getHelp()
                                                        
                                                if x>=613 and x<=663:
                                                    if y>=480 and y<=530:
                                                        self.the_start_screen()
                                                                
##                                                if pygame.mouse.get_pos() >= (613,480):
##                                                        if pygame.mouse.get_pos() <= (663,530):
##                                                                print('2')
##                                                                self.the_start_screen()
                                                        
                                                if x>=185 and x<=600:
                                                    if y>=250 and y<=620:
                                                        self.goto_level()                                                
                                                        
##                                                if pygame.mouse.get_pos() >= (185,600):
##                                                        if pygame.mouse.get_pos() <= (250,620):
##                                                                print('3')
##                                                                self.goto_level()
                                                        
                                                if x>=383 and x<=500:
                                                    if y>=247 and y<=289:
                                                        self.level=1
                                                        self.score=0
                                                        self.new()
                                                        
##                                                if pygame.mouse.get_pos() >= (383,247):
##                                                        if pygame.mouse.get_pos() <= (500,289):
##                                                                self.level=1
##                                                                print('4')
##                                                                self.new()
                                                        
                                                if x>=524 and x<=641:
                                                    if y>=248 and y<=289:
                                                        self.level=2
                                                        self.score=0
                                                        self.drawLevel2()
                                                        
##                                                if pygame.mouse.get_pos() >= (524,248):
##                                                        if pygame.mouse.get_pos() <= (641,289):
##                                                                self.level=2
##                                                                self.new()
                                                        
                                                if x>=384 and x<=498:
                                                    if y>=331 and y<=372:
                                                        self.level=3
                                                        self.score=0
                                                        self.drawLevel3()
                                                        
##                                                if pygame.mouse.get_pos() >= (384,331):
##                                                        if pygame.mouse.get_pos() <= (498,372):
##                                                                self.level=3
##                                                                self.new()
                                                        
                                                if x>=524 and x<=639:
                                                    if y>=329 and y<=373:
                                                        self.level=4
                                                        self.score=0
                                                        self.drawLevel4()
                                                        
##                                                if pygame.mouse.get_pos() >= (524,329):
##                                                        if pygame.mouse.get_pos() <= (639,373):
##                                                            self.level=4
##                                                            self.new()
                                                        
                                                if x>=495 and x<=535:
                                                    if y>=20 and y<=40:
                                                        self.playing=False
                                                        self.the_start_screen()                                                       
                                                            
##                                                if pygame.mouse.get_pos() >= (385,20):
##                                                        if pygame.mouse.get_pos() <= (435,40):
##                                                            print('here')
##                                                            self.playing=False
##                                                            self.the_start_screen()


        def next_level_screen(self):
            #if we won, we see the next level screen, showing our score and option to ether go back to menu or continue the game
                self.screen.blit(nextlevel,(0,0))
                btn=pygame.draw.rect(self.screen,(0,0,240),(495,20,50,20))
                self.draw_text("Menu",18,white,515,20)
                self.draw_text("You won, Another level?",39,white,width/2,height/4-10)
                self.draw_text("score:"+str(self.score),25,white,width/2,height*3/4)
                self.draw_text("press S to continue",18,white,width/2,height*4/5)
                pygame.display.flip()
                self.wait_for_key()
                                        
        def the_gameOver_screen(self):
                if not self.gameIsON:
                        return
                #the game over screen, giving us the score before we lost
                self.screen.blit(gameOver,(0,0))
                btn=pygame.draw.rect(self.screen,(255,255,255),(495,20,50,20))
                self.draw_text("Menu",18,bluish,515,20)
                self.draw_text("Game over, Want to try again?",39,white,width/2,height/8)
                self.draw_text("score:"+str(self.score),25,white,width/2,height/4-40)
                self.draw_text("press S to restart",18,white,width/2,height*4/5)
                pygame.display.flip()
                self.wait_for_key()
                self.score=0
                
        def goto_level(self):
            #a window to choose any level
            instruction=self.screen.blit(levels,(250,100))
            pygame.display.flip()
    
 

g=Game()
g.the_start_screen()
while g.gameIsON:
	g.new()
	g.the_gameOver_screen()
pygame.quit()
