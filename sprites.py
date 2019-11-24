import pygame as pg
from settings import*

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
	def __init__(self,game,walkLeft,walkRight):
		pg.sprite.Sprite.__init__(self)
		self.game=game
		self.i=0
		self.image=character
		self.walkRight=walkRight
		self.walkLeft=walkLeft
		self.rect=self.image.get_rect()
		self.rect.center=(width/2,height/2)
		self.pos=vec(width/2,height/2)
		self.vel=vec(0,0)
		self.acc=vec(0,0)

	def jump(self):
		#in life you can not jump twice from one jump
		self.rect.x += 1
		hits = pg.sprite.spritecollide(self,self.game.platforms,False)
		self.rect.x -= 1
		if hits:
			self.vel.y=-jumpPower
	

	def update(self):
		self.acc=vec(0,gravity)
		keys=pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.acc.x = -player_acc
			#if self.i+1>=10:
				#self.i=0
			#for i in range(len(walkLeft)):
			self.image=walkLeft[self.i]
			self.i= (self.i+1)%len(walkLeft)

		if keys[pg.K_RIGHT]:
			self.acc.x = player_acc	
			self.image=walkRight[self.i]
			self.i= (self.i+1)%len(walkRight)

		


        #the equations of friction, velocity and acceleration
		self.acc.x += self.vel.x*player_friction	
		self.vel += self.acc
		self.pos += self.vel + 0.5*self.acc

		self.rect.midbottom = self.pos

		#if self.pos.x > width:
			#self.pos.x=width

		if self.pos.x<0:
			self.pos.x=0

		#we died?! oh on!


class Platform(pg.sprite.Sprite):
	def __init__(self,x,y,w,h):
		pg.sprite.Sprite.__init__(self)
		self.image=pg.Surface((w,h))
		self.image.fill(white)
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
