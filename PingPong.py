print ('This is a game by Samantha Moross')

import pygame, sys, random, os
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

pygame.init()
screensize = (640, 480)
screen = pygame.display.set_mode(screensize)
FPS = 200

#Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 100, 00)
red = (255, 0, 0)

class Pong(object): #CHANGE TO SPRITE?
	def __init__(self, screensize):
		self.screensize = screensize

		#place ball in the center
		self.centerx = int(screensize[0]*0.5) 
		self.centery = int(screensize[1]*0.5)

		self.radius = 8

		#create shape and sizes it
		self.rect = pygame.Rect(self.centerx-self.radius, 
			self.centery-self.radius, 
			self.radius*2, self.radius*2) 

		self.color = white
		self.direction = [1,1] #current direction to the right and up
		#list so we can access each individual part because it will change

		self.speedx = 2
		self.speedy = 5
		#ADJUST RATIO OF X & Y SPEEDS TO MAKE IT HARDER AS GAME PROGRESSES

		self.hit_left_edge = False
		self.hit_right_edge = False

	def update(self, player_paddle, ai_paddle):
		self.centerx += self.direction[0]*self.speedx
		self.centery += self.direction[1]*self.speedy

		self.rect.center = (self.centerx, self.centery)

		sound = pygame.mixer.Sound(os.path.join('ping.wav'))
		player_score = 0
		ai_score = 0

		#makes sure if ball hits top it comes back down
		if self.rect.top <= 0: 
			self.direction[1] = 1
		elif self.rect.bottom >= self.screensize[1]-1:
			self.direction[1] = -1 #bounce up and down
		elif self.rect.right >= self.screensize[0]-1:
			self.direction[0] = -1
		elif self.rect.left <= 0:
			self.direction[0] = 1

		#checks if the code above is true
		if self.rect.right >=self.screensize[0]-1: #if it's greater than width -1
			self.hit_right_edge = True
		elif self.rect.left <= 0:
			self.hit_left_edge = True
		if self.rect.top <= 0: 
			self.hit_right_edge = True
		elif self.rect.bottom >= self.screensize[1]-1:
			self.hit_left_edge = True


		#check for a collision between the rectangles
		if self.rect.colliderect(player_paddle.rect):
			self.direction[0] = -1
			player_score += 1
			sound.play()
			
		if self.rect.colliderect(ai_paddle.rect):
			self.direction[0] = 1
			ai_score += 1
			sound.play()

		#CHECK CENTER POINTS OF EACH

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

		self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

		self.color = white

		self.speed = 3
		self.direction = 0 #don't want it to move on its own
		

	def update(self):
		self.centery += self.direction*self.speed
		self.rect.center = (self.centerx, self.centery)

		#make sure paddle does not go off screen
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > self.screensize[1]-1:
			self.rect.bottom = self.screensize[1]-1 

	def render(self,screen):
		pygame.draw.rect(screen, self.color, self.rect, 0)
		pygame.draw.rect(screen, black, self.rect, 1)

def main():
	running = True

	clock = pygame.time.Clock()

	pong = Pong(screensize)
	ai_paddle = AIPaddle(screensize)
	player_paddle = PlayerPaddle(screensize)

	pygame.display.set_caption('Pong')

	pygame.mixer.music.load(os.path.join('ping.wav'))

	while running: #Main game loop	
		for event in pygame.event.get(): #handles events
			if event.type == pygame.QUIT: #Makes sure we can quit the game
				pygame.quit()
				exit()

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
		
		ai_paddle.update(pong)
		player_paddle.update()
		pong.update(player_paddle, ai_paddle)

		screen.fill(green)

		ai_paddle.render(screen)
		player_paddle.render(screen)
		pong.render(screen) #calls render function to the screen

		pygame.display.flip() #renders everything based on the update
		clock.tick(FPS) 

	pygame.quit()

if __name__=='__main__':
        main()
