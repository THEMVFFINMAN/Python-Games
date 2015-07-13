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

	def hitMiss(self, coord):
		for x in range (0, 5):
			ships[x].hitMiss(coord)

class ship:
	def __init__(self, coords):
		self.length = len(coords)
		self.coords = []
		for i in range (0, len(coords)):
			self.coords.append(coordinate(coords[i].x, coords[i].y))
		self.hits = 0
		self.right = True

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

	def hitMiss(self, coord):
		for x in range (0, self.length):
			if coord == coords[x] and coords[x].alive == True:
				hits = hits + 1

				if hits == self.length:
					print "BLOW UP FUNCTION"

				return true
		return false

class coordinate:
	def __init__(self, y, x):
		self.x = x
		self.y = y
		self.alive = True

def printBoard(board, screen, x, y):
	screen.move(x, y)
	for i in range(0,12):
		screen.addstr(' ')
		for j in range(0,12):
			screen.addstr(board[i][j] + ' ')
		screen.addstr('\n')

# Clearly the most efficient way to create the boards
def createBoards():
	enemyBoardV = [	['+', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '+'],
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

	enemyBoardI = [	['+', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '+'],
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
	return (enemyBoardV, enemyBoardI, userBoard)

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