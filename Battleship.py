#!/usr/bin/env python
# -*- coding: utf-8 -*- 
 
import curses
import time
import battleshipClass
from battleshipClass import *
from random import randint, choice

screen = curses.initscr() 
curses.noecho() 
curses.curs_set(2) 
screen.keypad(1) 
userBoard = createBoard()
enemyBoardR = createBoard()
enemyBoardF = createBoard()
userPieces = battleships()
enemyPieces = battleships()
over = False
playerHits = 0
playerMisses = 0
enemyHits = 0
enemyGuesses = []
enemyMisses = 0
hitData = ""
backwards = False


def mainMenu():
	# I know it looks bad but curses was giving me issues with spacing
	Menu =        "  +======================+\n"
	Menu = Menu + "  |                      |\n"
	Menu = Menu + "  |      PyttleShip      |\n"
	Menu = Menu + "  |                      |\n"
	Menu = Menu + "  +======================+\n\n"
	Menu = Menu + "\t1. Start Game \n"
	Menu = Menu + "\t2. Credits \n"
	Menu = Menu + "\t3. Quit\n\n"
	Menu = Menu + " >> "


	screen.addstr(Menu)
	screen.refresh()

	while True:
		event = screen.getch() 
		if event == ord(str(1)): 
			screen.clear()
			return
		if event == ord(str(2)):
			screen.clear()
			credits()
		if event == ord(str(3)):
			curses.endwin()
			quit(1)

def credits():
	Credits = "\n   Author: JJ Lowe\n   Email: joshuajordanlowe@gmail.com\n   Github: THEMVFFINMAN\n\n"
	Credits = Credits + "    1. Main Menu \n"
	Credits = Credits + "    2. Quit\n\n"
	Credits = Credits + " >> "

	screen.addstr(Credits)
	screen.refresh()

	while True:
		event = screen.getch() 
		if event == ord(str(1)): 
			screen.clear()
			mainMenu()
		if event == ord(str(2)):
			curses.endwin()
			quit(1)

def placePieces():
	x = 4
	y = 2

	coords = [coordinate(y, x), coordinate(y, x + 2), coordinate(y, x + 4), coordinate(y, x + 6), coordinate(y, x + 8)]
	aircraft = ship(coords)
	placePiecesLoop(aircraft, x, y,)

	coords = [coordinate(y, x), coordinate(y, x + 2), coordinate(y, x + 4), coordinate(y, x + 6)]
	battleship = ship(coords)
	placePiecesLoop(battleship, x, y)

	coords = [coordinate(y, x), coordinate(y, x + 2), coordinate(y, x + 4)]
	submarine = ship(coords)
	placePiecesLoop(submarine, x, y)
	placePiecesLoop(submarine, x, y)

	coords = [coordinate(y, x), coordinate(y, x + 2)]
	patrolBoat = ship(coords)
	placePiecesLoop(patrolBoat, x, y)

	return

def placePiecesLoop(boat, x, y):
	global userPieces

	printBoard(userBoard, screen, 0, 0)
	screen.addstr("\n  Place your {0}\n  Press 'R' to Rotate, \n  'WASD' to move and 'E' to place".format(shipName(boat.length)))
	screen.move(y, x)

	boat.printShip(y, x, userBoard, screen)	
	while True: 
		event = screen.getch() 
		if event == ord('w') or event == ord('W'): 
			if (y != 2):
				y = y - 1
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('a') or event == ord('A'): 
			if (x != 4):
				x = x - 2 
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('s') or event == ord('S'): 
			if ((y != 11 and boat.right) or (y != (7 + (5 - boat.length)) and not boat.right)):
				y = y + 1
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('d') or event == ord('D'): 
			if ((x != 22 and not boat.right) or (x != (14 + 2 * (5 - boat.length)) and boat.right)):
				x = x + 2
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('r'):
			if (y <= (7 + (5 - boat.length)) and boat.right):
				boat.right = False
			elif (x <= (14 + 2 * (5 - boat.length)) and not boat.right):
				boat.right = True
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('e'):
			interlap = False
			for i in range(0, boat.length):
				x2 = boat.coords[i][0] - 1
				y2 = boat.coords[i][1] - 1
				realY = (y2 - (y2 - 1)/2) - 1
				if userBoard[x2][realY] != 'O':
					interlap = True

			if not interlap:
				coords = []
				for i in range(0, boat.length):
					x2 = boat.coords[i][0] - 1
					y2 = boat.coords[i][1] - 1
					realY = (y2 - (y2 - 1)/2) - 1
					userBoard[x2][realY] = str(boat.length)
					coords.append(coordinate(realY, x2))

				userPieces.addShip(ship(coords))

				printBoard(userBoard, screen, 0, 0)
				screen.move(y, x)
				return
		elif event == ord('q'):
			curses.endwin()
			quit(1)


def enemyPiecePlacer():
	placeEnemyShip(5)
	placeEnemyShip(4)
	placeEnemyShip(3)
	placeEnemyShip(3)
	placeEnemyShip(2)

def placeEnemyShip(shipLength):
	while True:
		x = randint(1, 10)
		y = randint(1, 10)
		right = choice([True, False])
		
		if not right and (x >= (6 + (5 - shipLength))):
			continue
		elif x == 10 or y == 10:
			continue
		elif right and (y >= (6 + (5 - shipLength))):
			continue
		
		if enemyBoardR[x][y] != 'O':
			continue

		if not isValidPlacement(enemyBoardR, x, y, right, shipLength):
			continue

		testx = x
		testy = y
		coords = []

		for z in range(0, shipLength):
			enemyBoardR[testx][testy] = str(shipLength)
			coords.append(coordinate(testy, testx))
			if right:
				testy = testy + 1
			else:
				testx = testx + 1

		enemyPieces.addShip(ship(coords))
		break

def printGame(endGame):
	screen.clear()
	printBoard(enemyBoardR, screen, 0, 0)
	screen.addstr("\n{0}\n\n   P1 M:{1} H:{2} CP M:{3} H:{4}\n\n\n".format(hitData, playerMisses, playerHits, enemyMisses, enemyHits))
	printBoard(userBoard, screen, 19, 0)
	if not endGame:
		screen.addstr("\n Press \'E\' to send missile and \n \'WASD\' to move, \'Q\' to quit")
		screen.move(6,13)
	else:
		screen.addstr("\n   Press any key to exit")

def makeGuess(x, y):
	screen.move(y, x)
	while True: 
		event = screen.getch() 
		if event == ord('w') or event == ord('W'): 
			if y != 2:
				y = y - 1
			screen.move(y,x)
		elif event == ord('a') or event == ord('A'): 
			if x != 4:
				x = x - 2 
			screen.move(y,x)
		elif event == ord('s') or event == ord('S'): 
			if y != 11:
				y = y + 1
			screen.move(y,x)
		elif event == ord('d') or event == ord('D'): 
			if x != 22:
				x = x + 2
			screen.move(y,x)
		elif event == ord('e') or event == ord('E'):
			return attack(x, y)
		elif event == ord('q') or event == ord('Q'):
			curses.endwin()
			quit(1)

def attack(x, y):
	global hitData
	global playerHits

	oldX = x
	oldY = y

	x = (x - 3)/2 + 1
	y = y - 1
	if enemyBoardR[y][x] != 'X':
		hitData = enemyPieces.hitMiss(y, x)
		if hitData == True:
			hitData = "\t  Hit!! {0}{1}".format(chr(y + 64), x)
			playerHits = playerHits + 1
		elif hitData == False:
			hitData = "\t  Miss! {0}{1}".format(chr(y + 64), x)
		enemyBoardR[y][x] = 'X'
		
		if playerHits == 17:
			gameWin(True)

		printGame(False)
		curses.curs_set(0) 
		screen.move(16,0)
		screen.addstr("  Press any key for AI hit")
		event = screen.getch()
		curses.curs_set(2) 
		return (oldX, oldY)

	else:
		hitData = "     Already Marked {0}{1}".format(chr(y + 64), x)
		printGame(False)
		return makeGuess(oldX, oldY)

def enemyGuess():
	global hitData
	global enemyHits
	global enemyGuesses
	global backwards

	guessX = randint(1, 10)
	guessY = randint(1, 10)

	screen.move(40, 0)
	count = 0
	for cork in enemyGuesses:
		count = count + 1
		#screen.addstr("{0} x: {1} y: {2} Alive: {3}\n".format(count, cork.x, cork.y, str(cork.alive)))

	#event = screen.getch()
	if len(enemyGuesses) > 0 and enemyGuesses[-1].alive == True:
		if backwards == True:
			guessX = guessX = enemyGuesses[-1].x - 1
		else:
			guessX = enemyGuesses[-1].x + 1
		guessY = enemyGuesses[-1].y

		if guessX == 11 or userBoard[guessY][guessX] == 'X':
			guessX = enemyGuesses[-1].x - 2

			if userBoard[guessY][guessX] == 'X':
				guessX = enemyGuesses[-1].x + 1

			if userBoard[guessY][guessX] == 'X':
				guessX = randint(1, 10)
				guessY = randint(1, 10)
		elif guessX == 0:
			guessX = randint(1, 10)
			guessY = randint(1, 10)

	elif len(enemyGuesses) > 1 and enemyGuesses[-2].alive == True and enemyGuesses[-1].alive == False:
		guessX = enemyGuesses[-1].x
		guessY = enemyGuesses[-1].y
		backwards = True
		while userBoard[guessY][guessX] == 'X':

			guessX = guessX - 1
			if guessX <= 0:
				guessX = randint(1, 10)
				guessY = randint(1, 10)
				break

	newCoord = coordinate(guessY, guessX)

	if userBoard[guessY][guessX] != 'X':
		hitData = userPieces.hitMiss(guessY, guessX)
		if hitData == True:
			hitData = "        AI Hit!! {0}{1}".format(chr(guessY + 64), guessX)
			enemyHits = enemyHits + 1
			enemyGuesses.append(newCoord)
		elif hitData == False:
			hitData = "       AI Missed! {0}{1}".format(chr(guessY + 64), guessX)
			newCoord.alive = False
			backwards = False
			if len(enemyGuesses) > 0:
				enemyGuesses.append(newCoord)

		userBoard[guessY][guessX] = 'X'

		if len(enemyGuesses) > 4 and enemyGuesses[-1].alive == False and enemyGuesses[-2].alive == False and enemyGuesses[-3].alive == False and enemyGuesses[-4].alive == False:
			enemyGuesses = []

		if enemyHits == 17:
				gameWin(False)
	else:
		enemyGuess()
		return

	printGame(False)

def printShipCoordinates(battleships):
	screen.move(34,6)
	for ship in battleships.ships:
		screen.addstr(str(shipName(ship.length)) + '\n')
		x = 0
		for coord in ship.coords:
			screen.addstr("{0}: x:{1} y:{2}\t".format(str(x), str(coord.x), str(coord.y)))
			x = x + 1
		screen.addstr("\n\n")

def gameWin(playerWon):
	curses.curs_set(0) 
	global hitData

	if playerWon:
		hitData = "   Player Won the Game!"
	else:
		hitData = "  Computer Won the Game!"

	printGame(True)
	z = 2

	for q in range (0, 2):
		screen.move(z, 4)
		for j in range(0, 10):
			for i in range(0, 10):
				if i == 9:
					screen.addstr("X")
				else:
					screen.addstr("X ")
			z = z + 1
			screen.move(z, 4)

		z = 21
	
	event = screen.getch() 
	curses.endwin()
	quit(1)


def playGame():
	return

def main():
	mainMenu()
	placePieces()
	enemyPiecePlacer()
	printGame(False)
	x, y = makeGuess(14, 7)

	while True:
		enemyGuess()
		x, y = makeGuess(x, y)

	while True: 
		event = screen.getch() 
		curses.endwin()
		quit(1)

if __name__ == "__main__":
	main()