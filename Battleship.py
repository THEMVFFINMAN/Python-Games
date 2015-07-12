#!/usr/bin/env python
# -*- coding: utf-8 -*- 
 
import curses
import time

screen = curses.initscr() 
curses.noecho() 
curses.curs_set(2) 
screen.keypad(1) 

def createBoards():
	enemyBoard = [	['+', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '+'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['+', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '+']
				]

	userBoard = [	['+', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '+'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['|', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '|'],
					['+', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '+']
				]
	return (enemyBoard, userBoard)

def mainMenu(screen):
	# I know it looks bad but curses was giving me issues
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
			break
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

mainMenu(screen)

'''
for i in range(0,12):
	screen.addstr(' ')
	for j in range(0,12):
		screen.addstr(enemyBoard[i][j] + ' ')
	screen.addstr('\n')

y = 1
x = 3
screen.move(y, x)
screen.refresh()
'''

while True: 
	event = screen.getch() 
	if event == ord("w"): 
		if (y != 1):
			y = y - 1
		screen.move(y, x)
		screen.refresh()
	if event == ord("a"): 
		if (x != 3):
			x = x - 2 
		screen.move(y, x)
		screen.refresh()
	if event == ord("s"): 
		if (y != 10):
			y = y + 1
		screen.move(y, x)
		screen.refresh()
	if event == ord("d"): 
		if (x != 21):
			x = x + 2
		screen.move(y, x)
		screen.refresh()
	if event == ord("q"): break 
