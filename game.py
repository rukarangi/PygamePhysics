import pygame
from pygame.locals import *
import math

pygame.init()

wWidth = 1000
wHeight = 1000

screen = pygame.display.set_mode(size=(wWidth, wHeight))

running = True

testx = 500
testy = 850
testRect = pygame.Rect(testx,testy,20,20)
dirtyRects = []

xModifier = 10
yModifier = 0

gravity = 0.01

framecounter = 0
xRebound = 0
yRebound = 0

mouseStartx = 0
mouseStarty = 0
mouseEndx = 0
mouseEndy = 0

mouseAngle = 0
mouseDistance = 0

throw = False
throwMult = 3

while running:
	framecounter += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseStartx = event.pos[0]
			mouseStarty = event.pos[1]

			print(mouseStartx, mouseStarty)

		if event.type == pygame.MOUSEBUTTONUP:
			mouseEndx = event.pos[0]
			mouseEndy = event.pos[1]

			throw = True

			#print(mouseEndx, mouseEndy)

	# Mouse angle, distance 180/pi
	# math.atan(y dist / x dist)
	
	if throw:
		mouseDistancex = (mouseStartx - mouseEndx) if (mouseStartx - mouseEndx) != 0 else 1
		mouseDistancey = (mouseStarty - mouseEndy)

		#print(mouseDistancex, mouseDistancey)

		mouseAngle = math.atan(mouseDistancey / mouseDistancex) * (180/math.pi) * -1
		#print(mouseAngle)

		mouseDistance = math.sqrt(abs(mouseDistancex ** 2) + abs(mouseDistancey ** 2))
		#print(mouseDistance)

		xModifier += (mouseDistancex / mouseDistance) * throwMult
		yModifier += (mouseDistancey / mouseDistance) * throwMult

		#xModifier += math.sin(90 - mouseAngle)
		#yModifier += math.cos(90 - mouseAngle)

		#print((math.sin(90 - mouseAngle)), (math.cos(90 - mouseAngle)))



	throw = False
	# Fill, and rect update

	screen.fill((0,0,0))

	dirtyRects.append(testRect)

	testRect = pygame.Rect(testx,testy,20,20)

	pygame.draw.rect(screen, (5,5,250), testRect)
	
	# Modifiers

	yModifier += gravity

	yModifier *= 0.9999
	xModifier *= 0.9999

	#if xModifier < 0.01:
	#	xModifier = 0
	#if yModifier < 0.01:
	#	yModifier = 0

	#print(xModifier, yModifier)

	if (framecounter - xRebound) > 400:
		if testx > wWidth - 20:
			xModifier *= -1
			xRebound = framecounter
		elif testx < 0:
			xModifier *= -1
			xRebound = framecounter

	if (framecounter - yRebound) > 400:
		if testy > wHeight - 20:
			yModifier *= -1
			yRebound = framecounter

	if framecounter % 10 == 0:
		testx += xModifier
		testy += yModifier
	
	# Tidy and update

	dirtyRects.append(testRect)
	
	pygame.display.update(dirtyRects)

	dirtyRects = []