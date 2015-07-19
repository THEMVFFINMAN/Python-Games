#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# I was going to call this file BattleshipSchool because that's where we 
# Keep the battleship classes, but I'm too mature for that kind of stuff

class battleships:
	def __init__(self):
		self.ships = []

	def addShip(self, ship):
		if ship.length == 5:
			self.aircraft = ship
		elif ship.length == 4:
			self.battleship = ship
		elif ship.length == 3 and not hasattr(ship, "submarine1"):
			self.submarine1 = ship
		elif ship.length == 3 and hasattr(ship, "submarine1"):
			self.submarine2 = ship
		elif ship.length == 2:
			self.patrol = ship
		
		self.ships.append(ship)

	def hitMiss(self, y, x):
		for ship in self.ships:
			if ship.hitMiss(y, x):
				return True
		return False

class ship:
	def __init__(self, coords):
		self.length = len(coords)
		self.coords = []
		for i in range (0, len(coords)):
			self.coords.append(coordinate(coords[i].x, coords[i].y))
		self.hits = 0
		self.right = True

	def hitMiss(self, y, x):
		for z in range(0, self.length):
			if self.coords[z].x == x and self.coords[z].y == y:
				self.coords[z].alive = False
				return True

		return False

	def printShip(self, y, x, userBoard, screen):
		screen.move(y, x)
		if self.right:
			self.coords = []
			for i in range (0, self.length):
				self.coords.append((y, x + (2 * i)))
		else:
			self.coords = []
			for i in range (0, self.length):
				self.coords.append((y + i,x))
		printBoard(userBoard, screen, 0, 0)
		for i in range(0, self.length):
			screen.addstr(self.coords[i][0], self.coords[i][1], str(self.length))
		screen.move(y, x)
		screen.refresh()

class coordinate:
	def __init__(self, y, x):
		self.x = x
		self.y = y
		self.alive = True

def isValidPlacement(board, x, y, right, shipLength):
	for z in range(0, shipLength):
		if board[x][y] != 'O':
			return False

		if right:
			y = y + 1
		else:
			x = x + 1
	return True

def printBoard(board, screen, x, y):
	screen.move(x, y)
	for i in range(0,12):
		if i == 1:
			screen.addstr('    ___________________\n')
		elif i == 11:
			screen.addstr('    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n')
		screen.addstr(' ')
		for j in range(0,12):
			if j == 1 and i != 0 and i != 11:
				screen.addstr('|')
			if j == 10 and i != 0 and i != 11:
				screen.addstr(str(board[i][j]) + '| ')
			else:
				screen.addstr(str(board[i][j]) + ' ')
		screen.addstr('\n')

# Clearly the most efficient way to create the boards
def createBoard():
	
	board = [	['+', ' 1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+'],
				['A', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'A'],
				['B', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B'],
				['C', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'C'],
				['D', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'D'],
				['E', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'E'],
				['F', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'F'],
				['G', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'G'],
				['H', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'H'],
				['I', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'I'],
				['J', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'J'],
				['+', ' 1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+']
			]

	return board

# This was just for slight cleanliness purposes
def shipName(shipLength):
	if shipLength == 5:
		return "Aircraft Carrier"
	elif shipLength == 4:
		return "Battleship"
	elif shipLength == 3:
		return "Submarine"
	elif shipLength == 2:
		return "Patrol Boat"