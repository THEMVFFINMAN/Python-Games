#!/usr/bin/env python
# -*- coding: utf-8 -*- 
 
import curses
import time
import battleshipClass
from battleshipClass import *

screen = curses.initscr() 
curses.noecho() 
curses.curs_set(2) 
screen.keypad(1) 


def mainMenu(screen):
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
			placePieces(screen)
		if event == ord(str(2)):
			screen.clear()
			credits(screen)
		if event == ord(str(3)):
			curses.endwin()
			quit(1)

def credits(screen):
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
			mainMenu(screen)
		if event == ord(str(2)):
			curses.endwin()
			quit(1)

def placePieces(screen):
	x = 3
	y = 1
	eneymyBoardV, enemyBoardI, userBoard = createBoards()

	userPieces = battleships()

	coords = [coordinate(y, x), coordinate(y, x + 2), coordinate(y, x + 4), coordinate(y, x + 6), coordinate(y, x + 8)]
	aircraft = ship(coords)
	placePiecesLoop(screen, aircraft, x, y, userBoard, userPieces)

	coords = [coordinate(y, x), coordinate(y, x + 2), coordinate(y, x + 4), coordinate(y, x + 6)]
	battleship = ship(coords)
	placePiecesLoop(screen, battleship, x, y, userBoard, userPieces)

	coords = [coordinate(y, x), coordinate(y, x + 2), coordinate(y, x + 4)]
	submarine = ship(coords)
	placePiecesLoop(screen, submarine, x, y, userBoard, userPieces)
	placePiecesLoop(screen, submarine, x, y, userBoard, userPieces)

	coords = [coordinate(y, x), coordinate(y, x + 2)]
	patrolBoat = ship(coords)
	placePiecesLoop(screen, patrolBoat, x, y, userBoard, userPieces)

	print userPieces

def placePiecesLoop(screen, boat, x, y, userBoard, userPieces):
	
	printBoard(userBoard, screen, 0, 0)
	screen.addstr("\n   Place your {0}\n   Press 'R' to Rotate, 'E' to place".format(shipName(boat.length)))
	screen.move(y, x)

	boat.printShip(y, x, userBoard, screen)	
	while True: 
		event = screen.getch() 
		if event == ord('w'): 
			if (y != 1):
				y = y - 1
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('a'): 
			if (x != 3):
				x = x - 2 
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('s'): 
			if ((y != 10 and boat.right) or (y != (6 + (5 - boat.length)) and not boat.right)):
				y = y + 1
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('d'): 
			if ((x != 21 and not boat.right) or (x != (13 + 2 * (5 - boat.length)) and boat.right)):
				x = x + 2
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('r'):
			if (y <= (6 + (5 - boat.length)) and boat.right):
				boat.right = False
			elif (x <= (13 + 2 * (5 - boat.length)) and not boat.right):
				boat.right = True
			boat.printShip(y, x, userBoard, screen)
		elif event == ord('e'):
			interlap = False
			for i in range(0, boat.length):
				x2 = boat.coords[i][0]
				y2 = boat.coords[i][1]
				realY = (y2 - (y2 - 1)/2) - 1
				if userBoard[x2][realY] != 'O':
					interlap = True

			if not interlap:
				coords = []
				for i in range(0, boat.length):
					x2 = boat.coords[i][0]
					y2 = boat.coords[i][1]
					realY = (y2 - (y2 - 1)/2) - 1
					userBoard[x2][realY] = str(boat.length)
					coords.append(coordinate(realY, x))

				userPieces.addShip(ship(coords))

				printBoard(userBoard, screen, 0, 0)
				screen.move(y, x)
				return
		elif event == ord('q'):
			curses.endwin()
			quit(1)

mainMenu(screen)