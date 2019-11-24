import pygame as pg
import random
from settings import*
from sprites import*

#SO far I'm using Chris Bradfield's "doodle jump" game starting template

class Game:
        def __init__(self):
                #initializing game window
                pg.init()
                pg.mixer.init()
                self.screen=pg.display.set_mode((width,height))
                pg.display.set_caption(title)
                self.clock=pg.time.Clock()
                self.gameIsON=True
                self.font_name=pg.font.match_font(FONT_NAME)
                self.score=0

        def new(self):
                #once you dye restart window
                #creating groups of sprites to detect collisions
                self.all_sprites=pg.sprite.Group()
                self.platforms=pg.sprite.Group()
                self.characters=pg.sprite.Group()
                self.player=Player(self,walkLeft,walkRight)
                self.all_sprites.add(self.player)
                self.characters.add(self.player)
                for plat in platform_list:
                        #creating objects and adding to the sprites group
                        p=Platform(*plat)
                        self.all_sprites.add(p)
                        self.platforms.add(p)
                for cat in walkLeft:
                        catLeft=Player(self,walkLeft,walkRight)
                        self.all_sprites.add(p)
                        self.platforms.add(p)
                for cat in walkRight:
                        catRight=Player(self,walkLeft,walkRight)
                        self.all_sprites.add(p)
                        self.platforms.add(p)
#                for cat in idle:
#                        catRight=Player(self,walkLeft,walkRight,idle)
#                        self.all_sprites.add(p)
#                        self.platforms.add(p)

                self.gameON()

        def gameON(self):
                #game loop
                self.playing = True
                while self.playing:
                        self.clock.tick(FPS)
                        self.events()
                        self.update()
                        self.draw()

        def update(self):
                #updaeing game loop
                self.all_sprites.update()
                #only falling, hitting a platform
                if self.player.vel.y>0:
                        hits=pg.sprite.spritecollide(self.player,self.platforms,False)
                        if hits:
                                self.player.pos.y=hits[0].rect.top
                                self.player.vel.y=0

                #if player reaches end of the screen scroll it 
                if self.player.rect.right >=abs(width/4):
                        self.player.pos.x -= abs(self.player.vel.x)
                        for plat in self.platforms:
                                plat.rect.x-=abs(self.player.vel.x)
                                if plat.rect.right<=0:
                                        plat.kill()
                                        self.score+=10
                                        
                for cat in self.characters:
                        #creating cat walk animation, with killing the cat sprites 
                        #which were created for previous locations                        
                        cat=Player(self,walkLeft,walkRight)
                        if cat.rect.left<=self.player.pos.x:
                                cat.kill()
                                
                
                #make new platforms
                while len(self.platforms)<6:
                        #generating random platforms on random locations within a range
                        platWidth = random.randrange(50,100)
                        p = Platform(random.randrange(0,width-platWidth),random.randrange(300,400),platWidth,20)
                        #adding all the platforms to the platforms and all sprites groups
                        #to detects the collisions between them
                        self.platforms.add(p)
                        self.all_sprites.add(p)

                if self.player.rect.bottom>=height:
                        #if cat dissapears from the screen the cat is dead
                        self.playing = False
                        #reset the score back to zero
                        self.score=0


        def events(self):
                #events in the game loop
                for event in pg.event.get():
                        #closing the screen window either during playing or before starting a game
                        if event.type==pg.QUIT:
                                if self.playing:
                                        self.playing=False
                                self.gameIsON=False

                        if event.type==pg.KEYDOWN:
                                if event.key==pg.K_UP:
                                        self.player.jump()

        def draw(self):
                #drawing in the game loop
                self.screen.fill(black)
                self.all_sprites.draw(self.screen)
                pg.display.flip()
                self.draw_text(str(self.score),22,blue,width/2,15)
                pg.display.flip()
                
        def draw_text(self,text,size,color,x,y):
                font=pg.font.Font(self.font_name,size)
                text_surface=font.render(text,True,color)
                text_rect=text_surface.get_rect()
                text_rect.midtop=(x,y)
                self.screen.blit(text_surface,text_rect)

        def the_start_screen(self):
                #start screen
                self.screen.fill(black)
                self.draw_text(title,48,white,width/2,height/4)
                self.draw_text("make the game",22,white,width/2,height/2)
                self.draw_text("press a key to start",22,white,width/2,height*3/4)
                pg.display.flip()
                self.wait_for_key()

        def wait_for_key(self):
                waiting=True
                while waiting:
                        self.clock.tick(FPS)
                        for event in pg.event.get():
                                if event.type==pg.QUIT:
                                        waiting=False
                                        gameIsON=False
                                if event.type==pg.KEYUP:
                                        waiting=False


        def the_gameOver_screen(self):
                if not self.gameIsON:
                        return
                self.screen.fill(black)
                self.draw_text("game over, LOSER!",48,white,width/2,height/4)
                self.draw_text("score:"+str(self.score),22,white,width/2,height/2)
                self.draw_text("press a key to restart",22,white,width/2,height*3/4)
                pg.display.flip()
                self.wait_for_key()

g=Game()
g.the_start_screen()
while g.gameIsON:
	g.new()
	g.the_gameOver_screen()

pg.quit()
