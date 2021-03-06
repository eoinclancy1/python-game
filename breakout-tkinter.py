# -*- coding:Utf-8 -*-
"breakout game"

#libraries
from tkinter import *
from random import choice
from sys import exit

#datas
TITLE = "Breakout Game"

COLORS = ['white', 'tomato', 'sandy brown', 'goldenrod', 'gold', 'yellow green', 'cadet blue'] #used to get random color for bricks

WIDTH, HEIGHT = 400, 600

#variables
nb, bricks = 30, [] #bricks number and list
brickDic = {} #bricks dictionnary with coordinates

bx, by, br = 200, 564, 8 #ball coordinates and radius
dx, dy = 2, -2 #ball directions
px, py, pw, ph = 200, 580, 80/2, 16/2 #x y rectangle coordinates, half width and half height

flag = "stop"

#functions
def newGame():
	global flag, px, bx, by
	flag = "play"
	px = 200
	bx, by = 200, 554
	gameScreen.coords(paddle, px+pw, py+ph, px-pw, py-ph)
	gameScreen.coords(ball)
	ballMovement()

def setGrid():
	gameScreen.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
	butNew.grid(row=1, column=0, padx= 5, pady= 10)
	butStop.grid(row=1, column=1)
	butContinue.grid(row=1, column=2)
	butQuit.grid(row=1, column=3)


def configWindow():
	root.title(TITLE)
	root.update_idletasks()
	width = root.winfo_width()
	height = root.winfo_height()
	x = (root.winfo_screenwidth()//2) - width//2
	y = (root.winfo_screenheight()//2) - height//2
	root.geometry("{}x{}+{}+{}".format(width, height, x, y))

def paddleMovement(direction):
	"determine movement with direction key left and right"
	global px

	if flag == "play":
		if direction == "right":
			if px+pw == 400: #fix for the outlinepixel
				px += 1
			if px+pw < 400:
				px += 10
		if direction == "left":
			if px+pw == 401: #fix for the outline pixel
				px -= 1
			if px-pw > 0:
				px -= 10
		# print(px, px+pw, px-pw)
		gameScreen.coords(paddle, px+pw, py+ph, px-pw, py-ph)
	else:
		pass

def ballMovement():
	"determine the ball movement"
	global bx, by, dx, dy

	if flag == "play":
		#change direction if ball reach an edge
		if bx+br >= WIDTH or bx-br <= 0:
			dx = -dx
		if by+br >= HEIGHT or by-br <=0:
			dy = -dy

		#change direction if the ball reach a brick
		if by-br <= 250:
			if checkBrickImpact():
				dy = -dy


		#change direction if impact with the paddle
		if by+br ==  py-(16/2):  #the y coord of contact surface of the paddle
			if checkPaddleImpact():
				dy = -dy

		bx += dx
		by += dy
		gameScreen.coords(ball, bx+br, by+br, bx-br, by-br)
		gameScreen.after(20, ballMovement)	
	else:
		pass

def createBricks():
	"create bricks and store them in list"
	w, h = 60, 20 #size of one brick
	x, y, hw, hh = 0, 0, w/2, h/2 # coordinates x, y and half size w, h
	c = 0
	cIndex = 0 #color index
	color = COLORS[cIndex]

	while c < nb:
		x += 71
		if c%5 == 0:
			cIndex += 1
			color = COLORS[cIndex]
			x = 60
			y += 40

		brick = gameScreen.create_rectangle(x-hw, y-hh, x+hw, y+hh, fill=color, width=0)
		bricks.append(brick)
		brickDic[brick] = [x-hw, y-hh, x+hw, y+hh]
		
		c += 1


def checkBrickImpact():
	"return true if the ball touch a brick (brick destroyed and removed from bricks and brickDic)"
	#check if impact with a brick

	for brick in bricks:
		if by-br == brickDic[brick][3] and bx >= brickDic[brick][0] and bx <= brickDic[brick][2]:
			print("Impact brick!", brick)
			#delete the brick in brickDic
			gameScreen.delete(brick)
			bricks.remove(brick)
			brickDic.pop(brick, None)
			return True

		if by+br == brickDic[brick][1] and bx >= brickDic[brick][0] and bx <= brickDic[brick][2]:
			print("Impact brick!", brick)
			#delete the brick in brickDic
			gameScreen.delete(brick)
			bricks.remove(brick)
			brickDic.pop(brick, None)
			return True

		if bx+br == brickDic[brick][0] and by >= brickDic[brick][1] and by <= brickDic[brick][3]:
			print("Impact brick!", brick)
			#delete the brick in brickDic
			gameScreen.delete(brick)
			bricks.remove(brick)
			brickDic.pop(brick, None)
			return True

		if bx-br == brickDic[brick][2] and by >= brickDic[brick][1] and by <= brickDic[brick][3]:
			print("Impact brick!", brick)
			#delete the brick in brickDic
			gameScreen.delete(brick)
			bricks.remove(brick)
			brickDic.pop(brick, None)
			return True

def checkPaddleImpact():
	"check if ball impact with the paddle"
	pxMax = px+(80/2)
	pxMin = px-(80/2)
	if bx >= pxMin and bx <= pxMax:
		print("Impact paddle !", pxMax, pxMin)
		return True
	

def checkBricks():
	"check coords of each bricks"
	print(bricks)
	print(brickDic)
	c = 0
	while c < len(bricks):
		print(bricks[c])
		print(gameScreen.coords(bricks[c]))
		print(brickDic[bricks[c]][0])
		print(brickDic[bricks[c]][1])
		print(brickDic[bricks[c]][2])
		print(brickDic[bricks[c]][3])
		c+=1

def stopGame():
	global flag
	flag = "stop"

def continueGame():
	global flag
	flag = "play"
	ballMovement()

def exit(event):
	sys.exit()

#program
if __name__ == "__main__":
	root = Tk()
	root.bind("<Escape>", exit)

	#create gamescreen
	gameScreen = Canvas(root, width=WIDTH, height=HEIGHT, bg="ivory", highlightthickness=1, highlightbackground="black")
	
	#create button
	butQuit = Button(root, text="Quit", command=root.quit)
	butStop = Button(root, text="Stop", command=stopGame)
	butContinue = Button(root, text="Continue", command=continueGame)
	butNew = Button(root, text="New Game", command=newGame)


	#create a rectangle that will serve as game paddle and bind arrow keys
	paddle = gameScreen.create_rectangle(px+pw, py+ph, px-pw, py-ph, fill="dodger blue", width=0)

	gameScreen.bind("<Right>", lambda e: paddleMovement("right"))
	gameScreen.bind("<Left>", lambda e: paddleMovement("left"))
	gameScreen.focus_set()


	#create a cercle that will serve as the game ball
	ball = gameScreen.create_oval(bx+br, by+br, bx-br, by-br, fill="tomato", outline="firebrick")

	#create the bricks
	createBricks()
	# checkBricks()

	setGrid()
	configWindow()

	root.mainloop()