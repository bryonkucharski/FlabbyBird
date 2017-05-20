'''
Bryon Kucharski
Fall 2016
Flabby Bird - a Flappy Bird Replica

'''

import pygame, sys
import time
from pygame.locals import *
from random import randint

pygame.init()  

def obstacleTop(xlocation, ylocation, x, y): #a functions that draws the top rectangle
	pygame.draw.rect(DISPLAYSURF, GREEN, Rect((xlocation,ylocation),(x,y)))

def obstacleBottom(xlocation, ylocation, x, y): # a function that draws the bottom rectangle
	pygame.draw.rect(DISPLAYSURF, GREEN, Rect((xlocation,ylocation),(x, y)))


def gameOver(): #displays the game over message and final score 
	myfont = pygame.font.SysFont("monospace", 50)
	scoreFont = pygame.font.SysFont("monospace", 20)
	label = myfont.render("Game Over", 1, (BLACK))
	finalscore = scoreFont.render("Your Final Score Was: " + str(score), 1, BLACK)
	DISPLAYSURF.blit(label, (100, 100))
	DISPLAYSURF.blit(finalscore, (100, 150))
	pygame.display.update()
	print('in gameover function')

def displayScore(addAmount): # displays the current score
	myfont = pygame.font.SysFont("monospace", 25)
	score = myfont.render("Score: " + str(addAmount), 1, (BLACK))
	DISPLAYSURF.blit(score, (450, 50))

FPS = 30
fpsClock = pygame.time.Clock()

display_width = 600
display_height = 400
DISPLAYSURF = pygame.display.set_mode((display_width, display_height), 0 ,32)
pygame.display.set_caption('Flabby Bird')

#sound variables
crash = pygame.mixer.Sound("Sounds/die.ogg")
fly = pygame.mixer.Sound("Sounds/wing.ogg")
point = pygame.mixer.Sound("Sounds/point.ogg")

WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
BabyBlue = (124,147,239)

#constant bird variables
bird_height = 49
bird_width = 49
bird_speed = 5

#############################################################################################################################################################################	
def main():
	#image and coordantes of bird
	bird = pygame.image.load('bird1.png')
	birdx = display_width/2
	birdy = display_height/2

	#coordantes and size of bottom box
	bottomBox_x = 50
	bottomBox_y = -randint(50, 150)
	bottomLocationx = display_width - bottomBox_x
	bottomLocationy = display_height

	#coordantes and size of top box
	topBox_x = 50
	topBox_y = randint(50,150)
	topLocationx = display_width - topBox_x
	topLocationy = 0

	score = 0
	obstacleSpeed = 10
	scoreAvailable = True

	#main game loop
	gameLoop = True
	#game over loop
	end = False
	while gameLoop:

		while end == True:
			print('in end')
			DISPLAYSURF.fill(BLACK)

			#game over text
			gameOverFont = pygame.font.SysFont("monospace", 50)
			gameOver = gameOverFont.render("Game Over", 1, (WHITE))
			DISPLAYSURF.blit(gameOver, (0,0))

			#score text
			scoreFont = pygame.font.SysFont("monospace", 20)
			finalscore = scoreFont.render("Your Final Score Was: " + str(score), 1, WHITE)
			DISPLAYSURF.blit(finalscore, (0,50))

			#play again font
			endFont = pygame.font.SysFont("monospace", 20)
			endMessage = endFont.render("Press B to play again or N to exit", 1, (WHITE))
			DISPLAYSURF.blit(endMessage, (0,100))

			#checks if user wants to play again
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_b:
						end = False
						main()
					elif event.key == pygame.K_n:	
						end = False
						gameLoop = False
						break;
			pygame.display.update()		

		DISPLAYSURF.fill(BabyBlue)
		DISPLAYSURF.blit(bird, (birdx, birdy))

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
		 		sys.exit()

		# constatnly displays the score
		displayScore(score)

		# constantly decreses the y value of the bird 
		birdy = birdy + bird_speed

		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_UP]:
			bird = pygame.image.load('bird2.png')
			fly.play()
			birdy += -8
		else:
			bird = pygame.image.load('bird1.png')


		#draws the top and bottom obstacles
		obstacleTop(topLocationx,topLocationy, topBox_x, topBox_y)
		obstacleBottom(bottomLocationx, bottomLocationy ,bottomBox_x, bottomBox_y)

		#top and bottom are same speed
		topLocationx -= obstacleSpeed
		bottomLocationx -= obstacleSpeed

		#if obstacles go outside screen, create new obstacles with random heights
		if topLocationx and bottomLocationx < -50:
			topLocationx = display_width
			topBox_y = randint(50,170)
			bottomLocationx = display_width 
			bottomBox_y = -randint(50,170)
			scoreAvailable = True

		#adds to the score if bird passes the obstacle
		if birdx > topLocationx + 50 and birdx > bottomLocationx + 50 and scoreAvailable == True:
			point.play()
			score += 1
			displayScore(score)
			scoreAvailable = False
			obstacleSpeed += 1

		#checks if bird is off screen
		if birdy + bird_height  > display_height or birdy < 0:
			crash.play()
			end = True
	
		#colliison detection for top box
		if birdy < topBox_y + topLocationy:
			if birdx > topLocationx and birdx < topLocationx + topBox_x or birdx+bird_width> topLocationx and birdx + bird_width < topLocationx + topBox_x:
				crash.play()
				end = True
			
		#colliison detection for bottom box
		if birdy + bird_height > bottomBox_y + bottomLocationy:
			if birdx > bottomLocationx and birdx < bottomLocationx + bottomBox_x or birdx+bird_width> bottomLocationx and birdx + bird_width < bottomLocationx + bottomBox_x:
				crash.play()
				end = True
	
		pygame.display.update()
		fpsClock.tick(FPS)
#############################################################################################################################################################################		
main()
print "END"
