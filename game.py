import pygame
from pygame.locals import *
import math

pygame.init()

wWidth = 1000
wHeight = 1000

screen = pygame.display.set_mode(size=(wWidth, wHeight))

class Vector2d:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

class MouseInfo:
	def __init__(self, start, end, current):
		self.start = start
		self.end = end
		self.current = current

running = True

gravityEnable = False
frictionEnable = True
ceilingEnable = True

coords = Vector2d(500,850)
testRect = pygame.Rect(coords.x,coords.y,20,20)
mouseRect1 = pygame.Rect(-100,-100,20,20)
mouseRect2 = pygame.Rect(-100,-100,20,20)
angleInfoRect = pygame.Rect(-100,-100,20,20)
dirtyRects = []

modifier = Vector2d()

physicalEffects ={
	"gravity": 0.01,
	"friction": 0.9999,
	"elasticty": 1
}

framecounter = 0

mouse = MouseInfo(Vector2d(), Vector2d(), Vector2d())

mouseAngle = 0
mouseDistance = [0,0,0]

throw = False
aiming = False
throwMult = 3

font = pygame.font.SysFont("Arial", 20)

def mouseDistances(targetPoint):
	"""Returns a Verctor2D of the Horiozntal and Vertical distance"""
	mouseDistancex = (mouse.start.x - targetPoint.x) if (mouse.start.x - targetPoint.x) != 0 else 1
	mouseDistancey = (mouse.start.y - targetPoint.y)
	return Vector2d(mouseDistancex, mouseDistancey)

def pythagoras(horizontal, vertical):
	"""Return the hypotunuse of a right-angle trianlge"""
	distance = math.sqrt(abs(horizontal ** 2) + abs(vertical ** 2))
	return distance

def applyEffects():
	"""Apply Gravity and Friction to modifier"""
	if gravityEnable:
		modifier.y += physicalEffects.get("gravity")

	if frictionEnable:
		modifier.x *= physicalEffects.get("friction")
		modifier.y *= physicalEffects.get("friction")

def checkBorders():
	"""Check for border collicsion and repel"""
	if coords.x > wWidth - 20:
		modifier.x *= -1 * physicalEffects.get("elasticty")
		coords.x = wWidth - 21
	elif coords.x < 0:
		modifier.x *= -1 * physicalEffects.get("elasticty")
		coords.x = 1

	if coords.y > wHeight - 20:
		modifier.y *= -1 * physicalEffects.get("elasticty")
		coords.y = wHeight - 21

	if ceilingEnable:
		if coords.y < 0:
			modifier.y *= -1 * physicalEffects.get("elasticty")
			coords.y = 1

def drawScreen():
	"""Fills screen and draws the box as well as the angle and aiming boxes"""
	screen.fill((0,0,0))

	pygame.draw.rect(screen, (5,5,250), testRect)

	if aiming:
		pygame.draw.rect(screen, (255,255,255), mouseRect1)
		pygame.draw.rect(screen, (255,255,255), mouseRect2)
		screen.blit(text, angleInfoRect)

while running:
	framecounter += 1

	# Mouse and exit event handling

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse.start.x = event.pos[0]
			mouse.start.y = event.pos[1]

			aiming = True

		if event.type == pygame.MOUSEBUTTONUP:
			mouse.end.x = event.pos[0]
			mouse.end.y = event.pos[1]

			throw = True
			aiming = False

	if aiming:
		mouse.current.x = pygame.mouse.get_pos()[0]
		mouse.current.y = pygame.mouse.get_pos()[1]

		mouseDistance = mouseDistances(mouse.current)
		mouseAngle = math.atan(mouseDistance.y / mouseDistance.x) * (180/math.pi) * -1

		dirtyRects.append(mouseRect1)
		dirtyRects.append(mouseRect2)
		dirtyRects.append(angleInfoRect)

		mouseRect1 = pygame.Rect(mouse.start.x, mouse.start.y, 20, 20)
		mouseRect2 = pygame.Rect(mouse.current.x, mouse.current.y, 20, 20)
		angleInfoRect = pygame.Rect(mouse.start.x + 50, mouse.start.y, 100, 100)
		text = font.render(str(math.floor(mouseAngle)), False, (255,255,255))

		dirtyRects.append(mouseRect1)
		dirtyRects.append(mouseRect2)
		dirtyRects.append(angleInfoRect)

	
	if throw:
		mouseDistance = mouseDistances(mouse.end)

		mouseDistanceReal = pythagoras(mouseDistance.x, mouseDistance.y)

		modifier.x += (mouseDistance.x / mouseDistanceReal) * throwMult * (abs(mouseDistanceReal)/200)
		modifier.y += (mouseDistance.y / mouseDistanceReal) * throwMult * (abs(mouseDistanceReal)/200)


	applyEffects()
	checkBorders()

	coords.x += modifier.x / 10
	coords.y += modifier.y / 10

	dirtyRects.append(testRect)
	testRect = pygame.Rect(coords.x,coords.y,20,20)
	dirtyRects.append(testRect)


	drawScreen()

	pygame.display.update(dirtyRects)

	throw = False
	dirtyRects = []