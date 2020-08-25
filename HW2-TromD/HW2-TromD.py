"""
Derek Trom
CSCI 384
HW2
AB Prune Connect 4
"""

import numpy as np
import pygame
import sys
import math
import random

# colors for board and pieces
BLUE = (0, 0, 255)
BLACK = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (0, 0, 0)
# dimensions of board
numRows = 6
numColumns = 7
# random globals
player = 0
computer = 1
playerPiece = 1
computerPiece = 2
windowLength = 4


def makeBoard():
    """
    creates multidimension array from numpy
    :return: array board
    """
    board = np.zeros((numRows, numColumns))
    return board


def placePiece(board, row, col, piece):
    """
    Placing a piece in the board
    :param board: Current board to place a piece
    :param row: row to drop in
    :param col: column to drop in
    :param piece: player or computer piece
    :return: new board
    """
    board[row][col] = piece


def validMove(board, col):
    """
    Checks for valid move
    :param board: board to check
    :param col: column to check
    :return: True if open and false if full
    """
    return board[numRows - 1][col] == 0


def getOpenRow(board, col):
    """
    get the nex open row
    :param board: board being checked
    :param col: column of board being checked
    :return: row open
    """
    for r in range(numRows):
        if board[r][col] == 0:
            return r


def printBoard(board):
    """
    Uses pygame to display board
    :param board: board to be printed
    :return: board
    """
    print(np.flip(board, 0))


def isWin(board, piece):
    """
    Check if a move is a win
    :param board: board to be checked
    :param piece: player's turn
    :return: True if a win or False if not win
    """
    # Check horizontal locations for win
    for c in range(numColumns - 3):
        for r in range(numRows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece \
                    and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(numColumns):
        for r in range(numRows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece \
                    and board[r + 3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(numColumns - 3):
        for r in range(numRows - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece \
                    and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(numColumns - 3):
        for r in range(3, numRows):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece \
                    and board[r - 3][c + 3] == piece:
                return True


def checkWindow(window, piece):
    """
    checks a window of 4 pieces and counts number of pieces according to the scores given below
    :param window: set of 4 blocks
    :param piece: whose turn it is
    :return: score of that window
    """
    score = 0
    # if move would be a win 100
    if window.count(piece) == 4:
        score += 100
    # if it connects 3 in a row
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 4
    # if 2 in a row not as important
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    # if opponent is close to winning block
    if window.count(playerPiece) == 3 and window.count(0) == 1:
        score -= 3
    return score


def getScores(board, piece):
    """
    get the scores of moves
    :param board: current board being explored
    :param piece: computer piece
    :return: score of possible moves
    """
    score = 0
    # center
    centerList = [int(i) for i in list(board[:, numColumns // 2])]
    centerCount = centerList.count(piece)
    score += centerCount * 3
    # horizontal stuff
    for r in range(numRows):
        rowList = [int(i) for i in list(board[r, :])]
        if piece == player:
            rowList.sort()
        else:
            rowList.sort(reverse=True)
        for c in range(numColumns - 3):
            window = rowList[c:c + windowLength]
            score += checkWindow(window, piece)
    # vertical spots
    for col in range(numColumns):
        colList = [int(i) for i in list(board[:, col])]
        if piece == player:
            rowList.sort()
        else:
            rowList.sort(reverse=True)
        for r in range(numRows - 3):
            window = colList[r:r + windowLength]
            score += checkWindow(window, piece)
    # positive diagonol
    for r in range(numRows - 3):
        for c in range(numColumns - 3):
            window = [board[r + i][c + i] for i in range(windowLength)]
            score += checkWindow(window, piece)
    # negative diagonal
    for r in range(numRows - 3):
        for c in range(numColumns - 3):
            window = [board[r + 3 - i][c + i] for i in range(windowLength)]
            score += checkWindow(window, piece)

    return score


def isTerminal(board):
    """
    checks if move is a leaf node
    :param board: board being loooked at
    :return: True or False
    """
    return isWin(board, playerPiece) or isWin(board, computerPiece) or len(getGoodMove(board)) == 0


def minimaxAB(board, depth, alpha, beta, maxPlayer):
    """
    Minimax with ab prune method
    :param board: Board being checked
    :param depth: depth to search ahead to
    :param alpha: the low for maximizing player
    :param beta: the high for the minimizing player
    :param maxPlayer: The player trying to maximize the move
    :return: minimax value and the column in which to choose next
    """
    validSpots = getGoodMove(board) # get moves
    terminal = isTerminal(board) # check if terminal board
    if depth == 0 or terminal:
        #base case
        if terminal:
            if isWin(board, computerPiece):
                return (None, 100000000000000)
            elif isWin(board, playerPiece):
                return (None, -100000000000000)
            else:
                return (None, 0)
        else:
            return (None, getScores(board, computerPiece))
    if maxPlayer:
        # initialize value to - infinity and start with random value for column
        value = -math.inf
        column = random.choice(validSpots)
        validSpots.sort(reverse=True)
        for col in validSpots:
            row = getOpenRow(board, col) # get open row to drop
            tempBoard = board.copy() # make copy
            placePiece(tempBoard, row, col, computerPiece) # drop piece in temp board
            newScore = minimaxAB(tempBoard, depth - 1, alpha, beta, False)[1] # recurse for opponent moves
            if newScore > value:  # get max score
                value = newScore
                column = col
            alpha = max(alpha, value)  # choose best choice
            if alpha >= beta:  # prune bad branch
                break
        return column, value
    else:
        # do reverse of above to simulate next player moves
        value = math.inf
        column = random.choice(validSpots)
        validSpots.sort()
        for col in validSpots:
            row = getOpenRow(board, col)
            tempBoard = board.copy()
            placePiece(tempBoard, row, col, playerPiece)
            newScore = minimaxAB(tempBoard, depth - 1, alpha, beta, True)[1] #recurse for computer moves
            if newScore < value:
                value = newScore
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def getGoodMove(board):
    """
    Get a list of posible drop locations
    :param board: board being examined
    :return: list of locations
    """
    validLocations = []
    for col in range(numColumns):
        if validMove(board, col):
            validLocations.append(col)

    return validLocations


def getBest(board, piece):
    """
    Get the best move for the board
    :param board: board being examined
    :param piece: piece that is being placed
    :return: the best column to be placed in
    """
    highestChoice = -1000000
    validSpots = getGoodMove(board)
    bestCol = random.choice(validSpots)
    for col in validSpots:
        row = getOpenRow(board, col)
        temp = board.copy()
        placePiece(temp, row, col, piece)
        score = getScores(temp, piece)
        if score > highestChoice:
            highestChoice = score
            bestCol = col
    return bestCol


def drawBoard(board):
    """
    Pygame functinality for drawing the board to a window
    :param board: board to write out to screen
    :return: window with game board GUI
    """
    for c in range(numColumns):
        for r in range(numRows):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(numColumns):
        for r in range(numRows):
            if board[r][c] == playerPiece:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == computerPiece:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


if __name__ == "__main__":
    chooseTurn = input("Computer or player start? ('C' for computer/'P' for player): ")
    while chooseTurn != "C" and chooseTurn != "P":
        chooseTurn = input("Computer or player start? ('C' for computer/'P' for player): ")
    if chooseTurn == "C":
        turn = computer
    elif chooseTurn == "P":
        turn = player
    board = makeBoard()  # create board
    printBoard(board)  # print the initial board
    game_over = False  # set game to false


    pygame.init()

    SQUARESIZE = 75 #window size

    width = numColumns * SQUARESIZE
    height = (numRows + 1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size) #make window
    drawBoard(board) #draw the board as a list in the console
    pygame.display.update() #draw the board in pygame window

    myfont = pygame.font.SysFont("monospace", 75)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_over: #exit calls
                pygame.time.wait(1000)
                sys.exit()

            if event.type == pygame.MOUSEMOTION and not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == player:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update() #update the board

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # Ask for Player 1 Input
                if turn == player:
                    posx = event.pos[0] #mouse over
                    col = int(math.floor(posx / SQUARESIZE))

                    if validMove(board, col): #check for valid drop
                        row = getOpenRow(board, col)
                        placePiece(board, row, col, playerPiece) #put in board

                        if isWin(board, playerPiece): #check for a win
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True #end game
                            print("Player won")
                        #go between player and computer
                        turn += 1
                        turn = turn % 2
                        printBoard(board)
                        drawBoard(board)


        #computer moves
        if turn == computer and not game_over:
            pygame.time.wait(500)
            col, minimaxScore = minimaxAB(board, 6, -math.inf, math.inf, True) #call minimax
            if validMove(board, col): #check valid move
                row = getOpenRow(board, col) #check for next open row
                placePiece(board, row, col, computerPiece) #drop in that row
                if isWin(board, computerPiece): #check for a win
                    label = myfont.render("Computer wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    print("Computer won")
                    game_over = True #game over
                printBoard(board)
                drawBoard(board)
                #increment and get player turn
                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(5000)


