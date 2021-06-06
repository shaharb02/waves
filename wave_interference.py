#Imports
from collections import deque
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #Disable Pygame Greeting
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import keyboard
import numpy
import math
import time

points = deque([0 for _ in range(260)])
points2 = deque([0 for _ in range(260)])
global spd, c
c = -1
spd = 0.03
pos = (0,0)

def init():
	pygame.init()
	display = (800,600)   # Size Of Screen
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)  #Use OpenGl For Pygame Screen
	pygame.display.set_caption("Wave interference")              #Title Of Screen
	gluPerspective(45, (display[0]/display[1]), 0.1, 100.0) #Set View Frustum(Field Of View, Aspect, Zclose, Zfar)
	glTranslatef(0, 0, -60) #Multiply Matrix By A Translation Matrix(Moving Away From The Object)
	glRotatef(50,1,0,0) #Rotate Around The X Axis
def draw(points):
	for z in range(12):
		glBegin(GL_LINE_STRIP)
		for i in range(0, len(points)):	
			glVertex3f((i-120)/5,2*points[i],z) #Render A Point To The Screen
		glEnd()    #End Render
def key():
	if keyboard.is_pressed('q'):     #SINE RIGHT
		for i in range(24):
			points[i] += math.sin(0.25*i)
		time.sleep(0.1)
	if keyboard.is_pressed('w'):     #SINE LEFT
		for i in range(1, 25):
			points2[-i] += math.sin(0.25*i)
		time.sleep(0.1)
	if keyboard.is_pressed('a'):     #SQUARE RIGHT
		for i in range(24):
			points[i] += 2
		time.sleep(0.1)
	if keyboard.is_pressed('s'):     #SQUARE LEFT
		for i in range(1,25):
			points2[-i] += 2
		time.sleep(0.1)	
	if keyboard.is_pressed('z'):	 #TRIANGLE RIGHT
		for i in range(24):
			if i<12:
				points[i] += i/5
			else:
				points[i] += 2*12/5-i/5
		time.sleep(0.1)
	if keyboard.is_pressed('x'):	 #TRIANGLE LEFT
		for i in range(0,25):
			if i<13:
				points2[-i] += i/5
			else:
				points2[-i] += 2*13/5-i/5
		time.sleep(0.1)
def speed(pos):
	global spd
	global points, points2, points3
	y = 15; l = 5

	for x in range(-16,17,8):
		if(pos[1]> 91 and pos[1] < 157):
			if(x == -16 and pos[0] < 231 and pos[0] > 153):
				glColor3d(1,0,0)
				spd = 0.2
			if(x == -8 and pos[0] < 350 and pos[0] > 274):
				glColor3d(1,0,0)
				spd = 0.1
			if(x == 0 and pos[0] < 475 and pos[0] > 400):
				glColor3d(1,0,0)
				spd = 0.03
			if(x == 8 and pos[0] < 600 and pos[0] > 530):
				glColor3d(1,0,0)
				spd = 0.01
			if(x == 16 and pos[0] < 720 and pos[0] > 650):
				glColor3d(1,0,0)
				spd = 0.005
		glBegin(GL_POLYGON)
		glVertex3f(x, y, 0)
		glVertex3f(x + l, y, 0)
		glVertex3f(x + l, y +l, 0)
		glVertex3f(x , y + l,0)
		glEnd()
		glColor3d(1,0,0)
		glBegin(GL_POLYGON)
		glVertex3f(-16,-40,-10)
		glVertex3f(16,-40,-10)
		glVertex3f(16,-50,0)
		glVertex3f(-16,-50,0)
		glEnd()
		if(pos[0] < 520 and pos[0] > 280 and pos[1] < 536 and pos[1] > 435):
			points = deque([0 for _ in range(260)])
			points2 = deque([0 for _ in range(260)])
			points3 = deque([0 for _ in range(260)])
		glColor3d(1,1,1)
def main():
	global c
	init()
	while True:
		pos = (0,0)
		#EVENTS
		for event in pygame.event.get(): #Quit
		        		if event.type == pygame.QUIT:#Quit
		        			pygame.quit()            #Quit
		        			quit()
		        		if event.type == pygame.MOUSEBUTTONUP:
		        			pos = pygame.mouse.get_pos()

		key() #Check For Key Press
		if keyboard.is_pressed('SPACE') and not keyboard.is_pressed('CTRL'): #STANDING WAVE
			c+=1
			points[0] += math.sin(0.25*c)
			points2[-1] += math.sin(0.25*c)
		if keyboard.is_pressed('SPACE') and keyboard.is_pressed('CTRL'): #NOTSTANDING WAVE
			c+=1
			points[0] += math.sin(0.25*c)
			points2[-1] += math.sin(0.1*c)
		
		#SMART STUFF
		points3 = deque([0 for _ in range(260)]) #Reset The Shown Wave Queue
		points.rotate(1) #Move "Left Wave" Right
		points[0] = 0  #Kill First Part Of "Left Wave"
		points2.rotate(-1) #Move "Right Wave" Left
		points2[len(points2)-1] = 0 #Kill First Part Of "Right Wave"
		
		for i in range(len(points3)):
			points3[i] += points2[i]+points[i]  #Wave Interference

	#RENDERING
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Clear Screen
		speed(pos)
		draw(points3) #Render The Points
		pygame.display.flip() #Update Screen
		time.sleep(spd)
main()