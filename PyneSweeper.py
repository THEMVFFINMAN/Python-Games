from random import randint

def createBoard():
	
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

def setMines(secretBoard, board, x2, y2):
	mines = 0

	while mines <= 19:
		x = randint(1,10)
		y = randint(1,10)

		if secretBoard[y][x] != "*" and not (x2 == x and y2 == y) :
			secretBoard[y][x] = "*"
			mines = mines + 1

	for x in range(1, 11):
		for y in range(1, 11):
			closeMines = 0
			if secretBoard[x][y] != "*":
				for x1 in range (-1, 2):
					for y1 in range (-1, 2):
						if secretBoard[x + x1][y + y1] == "*":
							closeMines = closeMines + 1

				secretBoard[x][y] = str(closeMines)

	board[y2][x2] = secretBoard[y2][x2]
	if secretBoard[y2][x2] == "0":
		cleanHouse(board, secretBoard, x2, y2)
	return secretBoard, board

def start():
	Menu =        "  +=====================+\n"
	Menu = Menu + "  |                     |\n"
	Menu = Menu + "  |     PyneSweeper     |\n"
	Menu = Menu + "  |                     |\n"
	Menu = Menu + "  +=====================+\n\n"
		
	print Menu

def printBoard(board):
	for x in range (len(board)):
		row = str(board[x])
		print "  " + row.replace("\'", "").replace(",", "").replace("[", "").replace("]", "")
		
def printBoards(board1, board2):
	printBoard(board1)
	printBoard(board2)

def getY(y):
	y = ord(str(y).lower()) - 96
	if y < 11 and y > 0:
		return y
	else:
		return -1

def validGuess(first):
	while True:
		flag = False

		guess = raw_input("Guess = A1, b4, c8, etc.\nFlag = fb3, Fc6, fH7, etc.\n\n >> ")
		if guess == "q" or guess == "Q":
			exit(0)

		if len(guess) != 2:
			if len(guess) != 3:
				continue
			elif getY(guess[0]) == 6 and first == False:
				guess = guess[1:len(guess)]
				flag = True
			else:
				continue
		y = getY(guess[0])
		try:
			x = int(guess[1])
		except Exception, e:
			continue
		if y == -1:
			continue
		elif x < 0 or x > 9:
			continue
		if x == 0:
			x = 10

		return (x, y, flag)

def cleanHouse(board, secretBoard, x, y):
	# It's so pretty :')

	for x1 in range (-1, 2):
		for y1 in range(-1, 2):

			if board[y + y1][x + x1] == '_' and 0 < y + y1 < 11 and 0 < x + x1 < 11:
				board[y + y1][x + x1] = secretBoard[y + y1][x + x1]
				if secretBoard[y + y1][x + x1] == "0":
					cleanHouse(board, secretBoard, x + x1, y + y1)

def main():
	start()
	board = createBoard()
	printBoard(board)
	secretBoard = createBoard()
	x, y, flag = validGuess(True)
	secretBoard, board = setMines(secretBoard, board, x, y)

	printBoard(board)

	while True:
		x, y, flag = validGuess(False)
		if flag:
			board[y][x] = "F"
			if checkWin(board, secretBoard):
				win(board)
		elif secretBoard[y][x] != "*":
			if secretBoard[y][x] != "0":
				board[y][x] = secretBoard[y][x]
			else:
				board[y][x] = secretBoard[y][x]
				cleanHouse(board, secretBoard, x, y)
		else:
			lose(board,secretBoard)

		printBoard(board)

def checkWin(board, secretBoard):
	for x in range (1, 11):
		for y in range(1, 11):
			if secretBoard[y][x] != board[y][x]:
				if not (secretBoard[y][x] == "*" and board[y][x] == "F"):
					return False

	return True

def win(board):
	for x in range(1, 11):
		for y in range(1, 11):
			if secretBoard[x][y] == "*":
				board[x][y] = "X"

	printBoard(board)
	print "\n You Winq!\n"
	exit(1)

def lose(board, secretBoard):
	for x in range(1, 11):
		for y in range(1, 11):
			if secretBoard[x][y] == "*":
				board[x][y] = "*"

	printBoard(board)
	print "\n KABOOM!\n"
	exit(1)

if __name__ == "__main__":
	main()
