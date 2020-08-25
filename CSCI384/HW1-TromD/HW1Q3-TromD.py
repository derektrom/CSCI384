"""
Derek Trom
HW1 Q
"""

class move:
    """
    The class of which the list board is stored
    """
    
    def __init__(self,board,cost):
        
        self.board = board
        self.cost = cost     


class node:
    """
    node for the board
    """
    
    def __init__(self,move):
        
        self.move = move

        

def display(n):
    """
    display board
    :param n: node object being printed
    :return: print board
    """
    
    print("Current node: ", n.move.board, "step cost:", n.move.cost)
            

def isequal(move, goal):
    """
    test if a win is reached
    :param move: the possible win
    :param goal: the goal config
    :return: True if found and false if not
    """
    for i in range(len(move.board)):
            if move.board[i] != goal[i]:
                return False
    return True
    

def locateBlank(board):
    """
    find blank tile
    :param board: board being searched
    :return: index of blank tile
    """
    # find 0
    index = -1
    for i in range(len(board)):
        if board[i] == ' ':
            index = i
            break
    return index
 

def swap(board,index,space):
    """

    :param board: the board to be swapped
    :param index: index of the black or white tile to be swapped
    :param space: location of the blank space
    :return: return the new board created
    """

    # copy board
    board2 = [' ']*len(board)
    for i in range(len(board)):
        board2[i] = board[i]
        
    
    t = board2[space]
    board2[space] = board2[index]
    board2[index] = t  
    cost = int(abs(space-index))
    return move(board2, cost)


def getNextBMoves(move):
    """
    get Black possible moves
    :param move: 1,2,3 move over tiles or one space over with associated costs
    :return:
    """
    board = move.board

    # find blank index
    blank = locateBlank(board)

    moves = []

    # for all possible move
    # swap tile with blank
    n = int(len(board) / 2)

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
    
# solve function
def solve(graph, graph2,explored,explored2, cost,depth, MAX_DEPTH):
    start=0
    maxdepth = "MAX DEPTH Reached for IDS"
    # return on max depth
    if MAX_DEPTH == 0:
        return maxdepth


    # get board
    n = graph.pop()
    moves = getNextBMoves(n.move)
    # add cost of this move

    
    # add node to explre list
    explored.append(n)
    explored2.append(n.move.board)
    
    # print curent node
    display(n)
    
    # print explored nodes
    print("number of explored nodes: ", len(explored))



        # put all moves in queue
    for m in moves:
        cost += m.cost
        moves = getNextBMoves(m)
        if isequal(m,goal):
            print ("goal found at depth: ",depth,"optimum cost",cost)
            return turn
        
            # add move node 
        if n.move in graph2 or n.move in explored2:
            continue
        graph.append(node(move(m.board, cost)))
        graph2.append(m)
        start += 1
        return solve(graph, graph2, explored, explored2,  cost, depth + 1, MAX_DEPTH - 1)

    # call solve recursion

if __name__=="__main__":
    # solve puzzle
    print ("Iterative deepening search method\n ")
    MAX_DEPTH = 50
    # intial board
    board = ['W', 'W', 'W', 'W', ' ', 'B', 'B', 'B', 'B']
    # initial goal
    goal = ['B', 'B', 'B', 'B', ' ', 'W', 'W', 'W', 'W']
    # set first turn


    # print goal
    print("goal")
    print(goal)
    g = 0
    graph = []
    graph2 = []
    explored = []
    explored2 = []
    graph.append(node(move(board,0)))
    depth = 0
    cost = 0
    solved = solve(graph, graph2, explored, explored2, cost, depth, MAX_DEPTH)
    print(solved)



    
    
                
            
    
    
    
    
    
                
    
    

