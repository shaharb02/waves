#Imports
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #Disable Pygame Greeting
import pygame
from pygame.locals import *
import time
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import keyboard


#Greeting
def greet():
    print("Welcome To Gal Omed" )
    print('You May Change The Properties Of The Standing Wave With The Corresponding Letter And + Or - Sign')
    print("'a' For Amplitude, 'f' For Frequency, 'o' For Order In Both Axes 'n' For Order In X Axis, 'm' For Order In Z Axis And 'l' For Resolution (Length Of Wave)")
    print("In Order To Move The Camera Use 'x' 'y' and 'z' In Conjunction With The + and - Signs")
    print("Print Values To Console With Corresponding Letter In Conjunction With 'p'")
    print("For Slow Motion Press 's'")
    print("To Change The Background Color Press 'c'")
    print("To Toggle A Second Wave Press 'w'")
    print("To Control The Second Wave Hold 'CTRL'")
    print("Have Fun Exploring The Realm Of The Standing Wave!")



#Change Color
def color(n, m, colcnt):
###Wave
	glColor3f(1,1,1)
	if n != m:
		 glColor3f(1,1,1)
	elif colcnt != 0:
		clrfrnt = [(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)]
		glColor3f(clrfrnt[n-1][0],clrfrnt[n-1][1],clrfrnt[n-1][2])
###Background
	clrback = [(0,0,0,0.1),(1,0.7,0.75,0.1),(0.6,1,0.6,0.1),(0.4,0.85,0.6,0.1),(0.7,1,0.2,0.1),(0.8,0.5,0.44,0.1),(0.5,0.7,0.5,0.1),(0.45,0.55,0.1,0.1)]
	glClearColor(clrback[colcnt][0],clrback[colcnt][1],clrback[colcnt][2],clrback[colcnt][3])


#Render And Calculations
def grid(t, n, a, f, l, m, xx, zz, colcnt):
	color(n,m,colcnt)				   #Change Color
	points = []                        #List Of Points
	glBegin(GL_POINTS)                 #Start Rendering
	for z in range(-l//2, l//2):       #Iterate Through z For Grid
		for x in range(-l//2, l//2):   #Iterate Through x For Grid

		#Calculation Of f(x,z,t)

			if n%2 ==0 and m%2 ==0:
				y = ((a * math.sin(n/l * x * math.pi ) * math.cos(t * f * 2 * math.pi)) * (a * math.sin(m/l * z *math.pi) ))
			elif n%2==0 and m%2==1:
				y = ((a * math.sin(n/l * x * math.pi ) * math.cos(t * f * 2 * math.pi)) * (a * math.cos(m/l * z *math.pi) ))
			elif n%2==1 and m%2==0:
				y = ((a * math.cos(n/l * x * math.pi ) * math.cos(t * f * 2 * math.pi)) * (a * math.sin(m/l * z *math.pi) ))
			elif n%2==1 and m%2==1:
				y = ((a * math.cos(n/l * x * math.pi ) * math.cos(t * f * 2 * math.pi)) * (a * math.cos(m/l * z *math.pi) ))
		
		#
			points.append((x,y,z))    #Save Points To List

	for i in points:
		glVertex3f(i[0]/(l/15)+xx,i[1],i[2]/(l/15)+zz) #Render A Point To The Screen
	glEnd()    #End Render



#Main
def main():
    pygame.init() #Initialize Pygame
    greet()     #Print Greeting

    xr = 0; yr = 0; zr = 0   #Rotation In X, Rotation In Y, Rotation In Z

    xx=0; zz = 0		#Make 0 To Center


    colcnt = 0  #Background Color Counter
    wvcnt = 0   #Wave Boolean

    m = 2       #Order Z
    n = 2       #Order X
    a = 1       #Amplitude
    f = 0.001   #Frequency
    l = 50      #Length

    m2 = 2       #Order Z
    n2 = 2       #Order X
    a2 = 1       #Amplitude
    f2 = 0.001   #Frequency

    display = (800,600)   # Size Of Screen
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)  #Use OpenGl For Pygame Screen
    pygame.display.set_caption("Gal Omed")              #Title Of Screen
    gluPerspective(45, (display[0]/display[1]), 0.1, 70.0) #Set View Frustum(Field Of View, Aspect, Zclose, Zfar)
    glTranslatef(0, 0, -40) #Multiply Matrix By A Translation Matrix(Moving Away From The Object)
    while True: #Main Loop
        for t in range(10000): #Time Loop
        	for event in pygame.event.get(): #Quit
        		if event.type == pygame.QUIT:#Quit
        			pygame.quit()            #Quit
        			quit()                   #Quit

        	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Clear Screen

        	if wvcnt == 1:   #Toggle 2nd Wave
        		xx = -10
        		grid(t, n2, a2, f2, l, m2, 10, 0, colcnt)
        	else:
        		xx = 0; zz = 0 #Center
        	grid(t,  n,  a,  f, l,  m, xx, zz, colcnt)   #Render Wave


#####################Keyboard#####################
#Length
        	if keyboard.is_pressed('l') and keyboard.is_pressed('p'):
        		print("L =", l)
        		time.sleep(0.1)

        	if keyboard.is_pressed('l') and keyboard.is_pressed('='):
        		time.sleep(0.01)
        		l += 2
        	if keyboard.is_pressed('l') and keyboard.is_pressed('-'):
        		time.sleep(0.01)
        		l -= 2
        	if l > 120:
        		l = 120
        	if l < 10:
        		l = 10
#Frequencies
#Main Wave
        	if keyboard.is_pressed('f') and keyboard.is_pressed('p') and keyboard.is_pressed('CTRL') == 0:
        		f = round(f,5)
        		print("Frequency =", f)
        		time.sleep(0.1)
        	if keyboard.is_pressed('f') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.05)
        		f += 0.0001
        	if keyboard.is_pressed('f') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.05)
        		f -= 0.0001
        	if f < 0.0001:
        		f = 0.0001
#Toggled Wave
        	if keyboard.is_pressed('f') and keyboard.is_pressed('p') and keyboard.is_pressed('CTRL'):
        		f2 = round(f,5)
        		print("Frequency =", f2)
        		time.sleep(0.1)
        	if keyboard.is_pressed('f') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.05)
        		f2 += 0.0001
        	if keyboard.is_pressed('f') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.05)
        		f2 -= 0.0001
        	if f2 < 0.0001:
        		f2 = 0.0001
#Order Main
#Main Wave
        	if keyboard.is_pressed('o') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.2)
        		m -= 1
        		n -= 1
        	if keyboard.is_pressed('o') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.2)
        		m += 1
        		n += 1
#Toggled Wave
        	if keyboard.is_pressed('o') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.2)
        		m2 -= 1
        		n2 -= 1
        	if keyboard.is_pressed('o') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.2)
        		m2 += 1
        		n2 += 1
#Order X
#Main Wave
        	if keyboard.is_pressed('n') and keyboard.is_pressed('p') and keyboard.is_pressed('CTRL') == 0:
        		print("Order In X Axis Is", n)
        		time.sleep(0.1)
        	if keyboard.is_pressed('n') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.2)
        		n += 1
        	if keyboard.is_pressed('n') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.2)
        		n -= 1
        	if n<0 or n == 0:
        		n = 1
        	if n > 7:
        		n = 7
#Toggled Wave
        	if keyboard.is_pressed('n') and keyboard.is_pressed('p') and keyboard.is_pressed('CTRL'):
        		print("Order In X Axis Is", n2)
        		time.sleep(0.1)
        	if keyboard.is_pressed('n') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.2)
        		n2 += 1
        	if keyboard.is_pressed('n') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.2)
        		n2 -= 1
        	if n2<0 or n2 == 0:
        		n2 = 1
        	if n2 > 7:
        		n2 = 7
#Order Z
#Main Wave
        	if keyboard.is_pressed('m') and keyboard.is_pressed('p') and keyboard.is_pressed('CTRL') == 0:
        		print("Order In Z Axis Is", m)
        		time.sleep(0.1)
        	if keyboard.is_pressed('m') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.2)
        		m += 1
        	if keyboard.is_pressed('m') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.2)
        		m -= 1
        	if m<0 or m == 0:
        		m = 1
        	if m > 7:
        		m = 7
#Toggled Wave
        	if keyboard.is_pressed('m') and keyboard.is_pressed('p') and keyboard.is_pressed('CTRL'):
        		print("Order In Z Axis Is", m2)
        		time.sleep(0.1)
        	if keyboard.is_pressed('m') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.2)
        		m2 += 1
        	if keyboard.is_pressed('m') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.2)
        		m2 -= 1
        	if m2<0 or m2 == 0:
        		m2 = 1
        	if m2 > 7:
        		m2 = 7
#Amplitude
#Main Wave
        	if keyboard.is_pressed('a') and keyboard.is_pressed('p') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.1)
        		a = round(a, 2)
        		print("Amplitude =", a)
        	if keyboard.is_pressed('a') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.2)
        		a += 0.1
        	if keyboard.is_pressed('a') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL') == 0:
        		time.sleep(0.2)
        		a -= 0.1
        	if a<0 or a == 0:
        		a = 1
#Toggled Wave
        	if keyboard.is_pressed('a') and keyboard.is_pressed('p') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.1)
        		a2 = round(a2, 2)
        		print("Amplitude =", a2)
        	if keyboard.is_pressed('a') and keyboard.is_pressed('=') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.2)
        		a2 += 0.1
        	if keyboard.is_pressed('a') and keyboard.is_pressed('-') and keyboard.is_pressed('CTRL'):
        		time.sleep(0.2)
        		a2 -= 0.1
        	if a2<0 or a2 == 0:
        		a2 = 1
#X Axis Rotate
        	if keyboard.is_pressed('x') and keyboard.is_pressed('='):
        		glRotatef(0.1, 1, 0, 0)
        		xr += 0.1
        	if keyboard.is_pressed('x') and keyboard.is_pressed('-'):
        		glRotatef(-0.1, 1, 0, 0)
        		xr -= 0.1
        	if keyboard.is_pressed('x') and keyboard.is_pressed('p'):
        		time.sleep(0.1)
        		xr = round(xr, 2)
        		print("Rotation in X Axis Is", xr, "Degrees")
        	if xr >360:
        		xr = 0
#Y Axis Rotate
        	if keyboard.is_pressed('y') and keyboard.is_pressed('='):
        		glRotatef(0.1, 0, 1, 0)
        		yr += 0.1
        	if keyboard.is_pressed('y') and keyboard.is_pressed('-'):
        		glRotatef(-0.1, 0, 1, 0)
        		yr -= 0.1
        	if keyboard.is_pressed('y') and keyboard.is_pressed('p'):
        		time.sleep(0.1)
        		yr = round(yr, 2)
        		print("Rotation in Y Axis Is", yr, "Degrees")
        	if yr > 360:
        		yr = 0
#Z Axis Rotate
        	if keyboard.is_pressed('z') and keyboard.is_pressed('='):
        		if keyboard.is_pressed('['):
        			glRotatef(20,0,0,1)
        		glRotatef(0.1, 0, 0, 1)
        		zr += 0.1
        	if keyboard.is_pressed('z') and keyboard.is_pressed('-'):
        		glRotatef(-0.1, 0, 0, 1)
        		zr -= 0.1
        	if keyboard.is_pressed('z') and keyboard.is_pressed('p'):
        		time.sleep(0.1)
        		zr = round(zr, 2)
        		print("Rotation in Z Axis Is", zr, "Degrees")
        	if zr > 360:
        		zr = 0 
#Stop In Place
        	if keyboard.is_pressed('SPACE'):
        		time.sleep(1)
#Slow Motion
        	if keyboard.is_pressed('s'):
        		time.sleep(0.03)
#Color Count
        	if keyboard.is_pressed('c'):
        		colcnt += 1
        		time.sleep(0.3)
        	if colcnt == 8:
        		colcnt = 0

        	if keyboard.is_pressed('w'):
        		wvcnt += 1
        		time.sleep(0.3)
        	if wvcnt > 1:
        		wvcnt = 0
#Update Screen
        	pygame.display.flip() #Update Screen
        pygame.time.wait(10)      #QOL

main() #Call Main