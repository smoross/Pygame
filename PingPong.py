print ('This is a game by Samantha Moross')

import pygame, sys, random, time
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

#Defines colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

FPS = 200

class Pong(object): #CHANGE TO SPRITE
	def __init__(self, screensize):
		#showTextScreen('Pong')
		self.screensize = screensize

		self.centerx = int(screensize[0]*0.5) #places object in the center
		self.centery = int(screensize[1]*0.5)

		self.radius = 8

		#create rectangle and sizes it
		self.rect = pygame.Rect(self.centerx-self.radius, 
			self.centery-self.radius, 
			self.radius*2, self.radius*2) 

		self.color = white
		self.direction = [1,1] #current direction to the right and up
		#list so we can access each individual part because it will change

		self.speedx = 2
		self.speedy = 5
		#ADJUST RATIO OF X & Y SPEEDS TO MAKE IT HARDER AS GAME PROGRESSES

		self.hit_left = False
		self.hit_right = False

	def update(self, player_paddle, ai_paddle):
		self.centerx += self.direction[0]*self.speedx
		self.centery += self.direction[1]*self.speedy

		self.rect.center = (self.centerx, self.centery)

		if self.rect.top <= 0: #makes sure if ball hits top it comes back down
			self.direction[1] = 1
		elif self.rect.bottom >= self.screensize[1]-1:
			self.direction[1] = -1 #bounce up and down

		#checks if the code above is true
		if self.rect.right >=self.screensize[1]-1: #if it's greater than width -1
			self.hit_right = True
		elif self.rect.left <= 0:
			self.hit_left = True

		#CHANGE DIRECTION OF PONG BASED ON WHERE IT HITS PADDLES
		#CHECK CENTER POINTS OF EACH

		#check for a collision between the rectangles
		if self.rect.colliderect(player_paddle.rect):
			pygame.mixer.music.Sound('ping.WAV').play()
			self.direction[0] = -1
		if self.rect.colliderect(ai_paddle.rect):
			pygame.mixer.music.Sound('ping.WAV').play()
			self.direction[0] = 1

	def render(self, screen):
		pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
		#creates black outline of the circle
		pygame.draw.circle(screen, black, self.rect.center, self.radius, 1)

class AIPaddle(object):
	def __init__(self, screensize):
		self.screensize = screensize

		self.centerx = 5
		self.centery = int(screensize[1]*0.5)

		self.height = 100
		self.width = 10
		#ADJUST SIZE OF PADDLE AS MATCH PROGRESSES TO MAKE IT HARDER

		self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

		self.color = white
		self.speed = 3 #how fast the AI will react to the pong position

	def update(self, pong):
		if pong.rect.top < self.rect.top:
			self.centery -= self.speed
		elif pong.rect.bottom > self.rect.bottom:
			self.centery += self.speed

		self.rect.center = (self.centerx, self.centery)

	def render(self,screen):
		pygame.draw.rect(screen, self.color, self.rect, 0)
		pygame.draw.rect(screen, (0,0,0), self.rect, 1)

class PlayerPaddle(object):
	def __init__(self, screensize):
		self.screensize = screensize

		self.centerx = screensize[0]-5
		self.centery = int(screensize[1]*0.5)

		self.height = 100
		self.width = 10
		#ADJUST SIZE OF PADDLE AS MATCH PROGRESSES TO MAKE IT HARDER

		self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

		self.color = white

		self.speed = 3
		self.direction = 0 #dont want it to move on its own

	def update(self):
		self.centery += self.direction*self.speed
		self.rect.center = (self.centerx, self.centery)

		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > self.screensize[1]-1:
			self.rect.bottom = self.screensize[1]-1 #makes sure paddle does not go off screen

	def render(self,screen):
		pygame.draw.rect(screen, self.color, self.rect, 0)
		pygame.draw.rect(screen, black, self.rect, 1)

def main():
	running = True
	pygame.init()

	screensize = (640, 480)

	screen = pygame.display.set_mode(screensize)

	clock = pygame.time.Clock()

	pong = Pong(screensize)
	ai_paddle = AIPaddle(screensize)
	player_paddle = PlayerPaddle(screensize)

	pygame.display.set_caption('Pong')
	font = pygame.font.Font('freesansbold.ttf', 24)

	while running: #Main game loop
			
		for event in pygame.event.get(): #handles events
			if event.type == pygame.QUIT: #Makes sure we can quit the game
				running = False

			if event.type == KEYDOWN:
				if event.key == K_UP:
					player_paddle.direction = -1
				elif event.key == K_DOWN:
					player_paddle.direction = 1

			if event.type == KEYUP: 
				if event.key == K_UP and player_paddle.direction == -1:
					player_paddle.direction = 0 

				elif event.key == K_DOWN and player_paddle.direction == 1:
					player_paddle.direction = 0 
		
		ai_paddle.update(pong) #update paddle before pong 
		player_paddle.update()
		pong.update(player_paddle, ai_paddle)

		if pong.hit_left: #MAKE TXT ON SCREEN OVER EVERYTHING ELSE SYAING YOU LOST/WON AND EXIT ON KEYPRESS
			print ('You Won') #ALLOW RESTARTING OF THE GAME. by recreating pongs/paddles
			running = False
		elif pong.hit_right:
			print ('You Lose')
			running = False

		screen.fill(black)

		ai_paddle.render(screen)
		player_paddle.render(screen)
		pong.render(screen) #calls render function to the screen

		pygame.display.flip() #renders everything based on the update
		FPS = clock.tick(FPS) 


if __name__=='__main__':
        main()
