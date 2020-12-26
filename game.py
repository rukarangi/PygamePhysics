import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode(size=(720, 720))

running = True

testx = 50
testRect = pygame.Rect(testx,50,100,100)
dirtyRects = []

framecounter = 0

while running:
	framecounter += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False


	screen.fill((0,0,0))

	dirtyRects.append(testRect)

	testRect = pygame.Rect(testx,50,100,100)

	pygame.draw.rect(screen, (255,50,50), testRect)
	
	
	
	if framecounter % 10 == 0:
		testx += 1
	
	dirtyRects.append(testRect)
	
	pygame.display.update(dirtyRects)

	dirtyRects = []