"""
Derek Trom
CSCI 384
HW 1 Q2C&E
Heuristic 1 # of out of place tiles and
Heuristic 2 # of whites to right of blacks

"""


class boardNode:
    """
    boardNode class to create  and store each boardNode for a possible move within the state space
    """

    def __init__(self, move, f, h, g):
        self.move = move
        self.f = f
        #self.turn = turn
        self.h = h
        self.g = g


    def __str__():
        return self.move + " f: " + str(self.f) + " turn: " + self.turn


class move:
    """
    stores move costs and layout
    """

    def __init__(self, layout, cost):
        """
        :rtype: object
        """
        self.layout = layout
        self.cost = cost

    def __str__():
        return self.layout + " cost: " + str(self.cost)



def getNextBMoves(move):
    """
    get all possible moves
    :param move: 1,2,3 move over tiles or one space over with associated costs
    :return: 
    """
    board = move.layout

    # find blank index
    blank = locateBlank(board)
    #list to store all moves
    moves = []

    # for all possible move
    # swap tile with blank

    for i in range(len(board)):
        if board[i] == 'B':
            m = swap(board, i, blank)
            if m.cost <= 3:
                moves.append(m)
            else:
                continue
    for i in range(len(board)):
        if board[i] == 'W':
            m = swap(board, i, blank)
            if m.cost <= 3:
                moves.append(m)
            else:
                continue

    # return moves
    return moves


def display(n,depth):
    """
    Shows board stats
    :param n: boardNode 
    :return: print out move board with stats
    """
    print(n.move.layout,
          "Depth: %d f(n) = g(n) + h(n)|| %d = %d + %d  move cost: %d" % (depth, n.f, n.g, n.h, n.move.cost))


# remove if move equals goal
def winningBoard(move, goals):
    """

    :param move: board of moves
    :param goal1: the goal board
    :return: Boolean True if the board matches goal state
    """
    for i in goals:
        if move == i:
            return True
    return False

# return location of blank space
def locateBlank(board):
    """
    Fine the blank space
    :param board: tile board
    :return: index of blank tile
    """
    index = -1
    for i in range(len(board)):
        if board[i] == ' ':
            index = i
            break
    return index


def swap(board, index, space):
    """
    perform the swap
    :param board: take in 'parent' board
    :param index: index of black or white to swap
    :param space: space index location
    :return: move node from parent board
    """
    # create a copy of board
    board2 = [' '] * len(board)

    for i in range(len(board)):
        board2[i] = board[i]

    # swap the W or B and the blank space
    #TODO: fix cost function here
    t = board2[space]
    board2[space] = board2[index]
    board2[index] = t
    cost = int(abs(space - index))

    return move(board2, cost)



def calcf(board, g):

    """
    Number of whites to left of right most black
    :param board: board being calculated
    :param g: cost so far
    :return: f and h value of board
    """
    blackCount = 0
    whiteCount = 0
    while blackCount < 4:
        for i in board:
            if i == "B":
                blackCount += 1
            if i == "W":
                whiteCount += 1
            else:
                continue
    totalH = whiteCount
    f = g + totalH
    return f, totalH



def getFValue(board, g):
    """
    get the f(n) value for number of out of place tiles
    :param board: board created from moves
    :param goal1: goal state 
    :param g: past cost
    :param cost: cost of move
    :return: tuple of f and h
    """

    blackCount = 0
    for i in range(4, len(board)):
        if board[i] == " ":
            continue
        elif board[i] == "B":
            blackCount += 1

    h = 2* blackCount
    # calculate f
    f = h + g
    return f, h



def solveH1():
    """
    main solving function
    :return: winner or not
    """
    # initial setup
    start = 0
    found = False
    numberNodes = 0
    print("Goal Boards")
    for i in goals:
        print(i, "\n")
    g = 0
    frontier = []  # frontier
    explored = []  # explored
    frontier2 = []
    explored2 = []

    frontier.append(boardNode(move(board, 0), 0, 0, 0))


    # loop until goal found
    while (found == False):
        # get layout move
        #frontier.sort(key=lambda x: x.f, reverse=True)
        n = frontier.pop()
        # add boardNode to explored list
        if n.move.layout not in explored2:

            explored.append(n)
            explored2.append(n.move.layout)
        g += n.move.cost
        n.f,n.h = getFValue(n.move.layout, g)

        #print("Current:")
        display(n, start)

        # get next moves for all tiles
        moves = getNextBMoves(n.move)
        numberNodes += len(moves)
        moves.sort(key=lambda x: x.cost, reverse = True)
        # sort by heuristic

        minimum = moves[0].cost
        for m in moves:
            if m.cost < minimum:

            if winningBoard(m.layout, goals):
                f, h = getFValue(m.layout, g)
                print(" * " * 30)
                print("\nGoal Met :)")
                print(m.layout)
                print("Number of states left in frontier set: ", len(frontier))
                print("Number of states left in explored set: ", len(explored))
                print("f(goal): %d" % f)
                print("Number of nodes expanded: %d\n"% numberNodes)
                print(" * " * 30)
                found = True
            # calculate f
            f, h = getFValue(m.layout, g)
            if (m.layout in frontier2) or (m.layout in explored2):
                #print("Skipping")
                continue
            if start == 0:
                frontier.append(boardNode(m, f, h, g))
                frontier2.append(m.layout)
                continue

            else:

                frontier.append(boardNode(m, f, h, g))
                frontier2.append(m.layout)


        start+=1

def solveH2():
    """
        main solving function
        :return: winner or not
        """
    # initial setup
    numberNodes = 0
    start = 0
    found = False
    print("Goal Boards")
    for i in goals:
        print(i, "\n")
    g = 0
    frontier = []  # frontier
    explored = []  # explored
    frontier2 = [] #used to check if already in frontier
    explored2 = [] #used to check if already in explored

    frontier.append(boardNode(move(board, 0), 0, 0, 0))

    # loop till goal found
    while found == False:
        # get layout move
        frontier.sort(key=lambda x: x.f, reverse=True)
        n = frontier.pop()

        # print (n.move.layout, "Popped")
        # print ("Cost: ", n.move.cost)
        # add boardNode to explored list
        if n.move.layout not in explored2:
            explored.append(n)
            explored2.append(n.move.layout)

        # print curent state
        # print("Current:")
        g += n.move.cost
        n.f, n.h = calcf(n.move.layout, g)
        display(n, start)

        # get next moves for Black tiles
        moves = getNextBMoves(n.move)
        numberNodes += len(moves)
        # sort by heuristic
        for m in moves:
            # check for win

            f, h = calcf(m.layout, g)


            if winningBoard(m.layout, goals):
                #f, h = getFValue(m.layout, g, m.cost)
                print(" * "*30)
                print("\nGoal Met :)")
                print(m.layout)
                print("Number of states left in frontier set: ", len(frontier))
                print("Number of states left in explored set: ", len(explored))
                print("f(goal): %d" % f)
                print("Number of nodes expanded: %d\n" % numberNodes)
                print(" * " * 30)
                found = True
            # print (m.layout, m.cost)
            # calculate f
            if start == 0:
                frontier.append(boardNode(m, f, h, g))
                frontier2.append(m.layout)
                continue
            if (m.layout in frontier2) or (m.layout in explored2):
                # print("Skipping")
                continue

            else:

                frontier.append(boardNode(m, f, h, g))
                frontier2.append(m.layout)

        start += 1
# main
if __name__ == '__main__':
    # initial state
    board = ['W', 'W', 'W', 'W', ' ', 'B', 'B', 'B', 'B']
    # initial goal states
    goals = ([[' ', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W'],
              ['B', ' ', 'B', 'B', 'B', 'W', 'W', 'W', 'W'],
              ['B', 'B', ' ', 'B', 'B', 'W', 'W', 'W', 'W'],
              ['B', 'B', 'B', ' ', 'B', 'W', 'W', 'W', 'W'],
              ['B', 'B', 'B', 'B', ' ', 'W', 'W', 'W', 'W'],
              ['B', 'B', 'B', 'B', 'W', ' ', 'W', 'W', 'W'],
              ['B', 'B', 'B', 'B', 'W', 'W', ' ', 'W', 'W'],
              ['B', 'B', 'B', 'B', 'W', 'W', 'W', ' ', 'W'],
              ['B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', ' ']])

    print("Heuristic 1: # of out of place tiles")
    print("Heuristic 2: # of whites to left of rightmost black")

    choice = input("Enter 1 for Heuristic 1\nEnter 2 for Heuristic 2\nQ to quit:\n")
    while choice != "Q":
        if choice == "1":
            solveH1()
        if choice == "2":
            solveH2()

        choice = input("Enter 1 for Heuristic 1\nEnter 2 for Heuristic 2\nQ to quit:\n")
