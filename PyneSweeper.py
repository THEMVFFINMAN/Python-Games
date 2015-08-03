import curses
from random import randint

# Setting up the curses screen
screen = curses.initscr() 
curses.noecho() 
curses.curs_set(2) 
screen.keypad(1) 

def createBoard():
	#Clearly the most efficient way to initiate this

	board = [	['+', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+'],
				['A', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'A'],
				['B', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'B'],
				['C', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'C'],
				['D', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'D'],
				['E', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'E'],
				['F', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'F'],
				['G', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'G'],
				['H', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'H'],
				['I', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'I'],
				['J', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'J'],
				['+', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+']
			]

	return board

def setMines(secretBoard, board, ox, oy):
	# Will probably add setting to allow a prespecified mine amount

	mines = 0

	# Making it so the screen and array play nice with each otehr
	sy = oy - 6
	sx = (ox-2)/2

	# The actual amount of mines
	while mines <= 14:
		rx = randint(1,10)
		ry = randint(1,10)

		# If the selected piece isn't a mine and it's not the imputted coordinate
		if secretBoard[ry][rx] != "*" and not (sx == rx and sy == ry) :
			secretBoard[ry][rx] = "*"
			mines = mines + 1

	# This goes through and figures the numbering out based on the surrounding mines
	for lx in range(1, 11):
		for ly in range(1, 11):
			closeMines = 0
			if secretBoard[lx][ly] != "*":
				for lx1 in range (-1, 2):
					for ly1 in range (-1, 2):
						if secretBoard[lx + lx1][ly + ly1] == "*":
							closeMines = closeMines + 1

				secretBoard[lx][ly] = str(closeMines)

	screen.move(oy, ox)
	screen.addstr(secretBoard[sy][sx])

	board[sy][sx] = secretBoard[sy][sx]

	if secretBoard[sy][sx] == "0":
		cleanHouse(board, secretBoard, sx, sy)

	screen.move(oy, ox)
	return secretBoard, board

def start(board):
	# This is the default screen
	Menu =        "  +=====================+\n"
	Menu = Menu + "  |                     |\n"
	Menu = Menu + "  |     PyneSweeper     |\n"
	Menu = Menu + "  |                     |\n"
	Menu = Menu + "  +=====================+\n\n"
	screen.move(0, 0)
	screen.addstr(Menu)

	printBoard(board)

	screen.refresh()

def printBoard(board):
	for x in range (len(board)):
		row = str(board[x])
		prettyRow = "  " + row.replace("\'", "").replace(",", "").replace("[", "").replace("]", "") + '\n'
		screen.addstr(prettyRow)

	#formatting = "\n       'WASD' to move\n\t'E' to Step\n\t'F' to Flag\n\t'Q' to Quit"
	#screen.addstr(20, 0, formatting)

def printBoards(board1, board2):
	printBoard(board1)
	printBoard(board2)

def cleanHouse(board, secretBoard, x, y):
	# This is the recursive algorithm that opens up the field when a 0 is hit
	# It was much prettier before I added the curses implementation :(

	for x1 in range (-1, 2):
		for y1 in range(-1, 2):

			if board[y + y1][x + x1] == '_' and 0 < y + y1 < 11 and 0 < x + x1 < 11:
				sx = ((x + x1) * 2) + 2
				sy = (y + y1) + 6
				screen.move(sy, sx)
				screen.addstr(secretBoard[y + y1][x + x1])
				board[y + y1][x + x1] = secretBoard[y + y1][x + x1]
				if secretBoard[y + y1][x + x1] == "0":
					cleanHouse(board, secretBoard, x + x1, y + y1)

def makeGuess(x, y):
	# This part is a test just for the first guess, could probably all be reworked later
	if (x != -1 and y != -1):
		screen.move(y, x)
	else:
		coord = curses.getsyx()
		y = coord[0]
		x = coord[1]

	# Simple boundary checking
	while True: 
		event = screen.getch() 
		if event == ord('w') or event == ord('W'): 
			if y > 7:
				y = y - 1
			screen.move(y,x)
		elif event == ord('a') or event == ord('A'): 
			if x > 4:
				x = x - 2
			screen.move(y,x)
		elif event == ord('s') or event == ord('S'): 
			if y < 16:
				y = y + 1
			screen.move(y,x)
		elif event == ord('d') or event == ord('D'): 
			if x < 22:
				x = x + 2
			screen.move(y,x)
		elif event == ord('e') or event == ord('E'):
			return (x, y, False)
		elif event == ord('f') or event == ord('F'):
			return (x, y, True)
		elif event == ord('q') or event == ord('Q'):
			curses.endwin()
			quit(1)

def main():	
	# Sets everything up including the first guess
	board = createBoard()
	secretBoard = createBoard()
	start(board)
	x, y, flag = makeGuess(4, 7)

	# Ensures you don't guess a bomb first try
	secretBoard, board = setMines(secretBoard, board, x, y)

	# The main loop
	while True:
		sx, sy, flag = makeGuess(-1, -1)
		x = (sx - 2) / 2
		y = sy - 6
		if flag and board[y][x] == '_':
			board[y][x] = 'F'
			screen.addstr('F')
		elif secretBoard[y][x] != '*' and not flag:
			screen.addstr(secretBoard[y][x])
			board[y][x] = secretBoard[y][x]

			if secretBoard[y][x] == '0':
				cleanHouse(board, secretBoard, x, y)
				
		elif not flag:
			lose(secretBoard)

		if checkWin(board):
			win(secretBoard)

		screen.move(sy, sx)

def checkWin(board):
	screen.move(20,0)

	for x in range(1, 11):
		for y in range(1, 11):
			if board[y][x] == "_":
				return False

	return True

def win(board):
	screen.move(6, 0)

	printBoard(board)

	screen.addstr("\n          You Win!\n   Press any key to quit")
	event = screen.getch() 
	curses.endwin()
	exit(1)

def lose(board):
	screen.move(6, 0)

	printBoard(board)

	screen.addstr("\n          KABOOM!\n   Press any key to quit")
	event = screen.getch() 
	curses.endwin()
	exit(1)

if __name__ == "__main__":
	main()
