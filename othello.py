import copy
import random
import math
import sys
CORNERWEIGHT = 1000
TILEWEIGHT = 10
MOVEWEIGHT = 100
class Board(object):
    def __init__(self, boardArray=None):
        self.boardArray = boardArray if boardArray is not None else self.getNewBoard()
        
    def getNewBoard(self):
        boardArray = []
        for i in range(8):
            boardArray.append([' '] * 8)
            
        boardArray = self.resetBoard(boardArray)
        return boardArray
    
    def resetBoard(self, oldboard):
        for x in range(8):
            for y in range(8):
                oldboard[x][y] = ' '
                
        oldboard[3][3] = 'O'
        oldboard[3][4] = 'X'
        oldboard[4][3] = 'X'
        oldboard[4][4] = 'O'
        return oldboard
    
    def getScore(self):
        xScore = 0
        oScore = 0
        for row in self.boardArray:
            for item in row:
                if item == 'X':
                    xScore += 1
                elif item == 'O':
                    oScore += 1
        return xScore - oScore
    
    def getBoardWithHints(self, tile):
        copy = self.copyBoard()
        copy = Board(copy)
        for x, y in copy.getValidMoves(tile):
            copy.boardArray[x][y] = '.'
        return copy
    
    def drawBoard(self):
        HLINE = '  +---+---+---+---+---+---+---+---+'
        VLINE = '  |   |   |   |   |   |   |   |   |'
 

        print(HLINE)
        for y in range(8):
            print "%d" % (y+1),
            for x in range(8):
                print('| %s' % self.boardArray[x][y]),
            print('|')
            print(HLINE)
        print('    1   2   3   4   5   6   7   8')
            
    def copyBoard(self):
        return copy.deepcopy(self.boardArray)
    
    def checkValidMoveWithFlips(self, tile, xStart, yStart):
        """Checks from a starting position every possible space near it with an enemy tile
           and returns a list of tiles to be flipped along all lines of enemy tiles, if any."""
        board = self.copyBoard()
        if self.boardArray[xStart][yStart] != " " or not self.onBoard(xStart, yStart):
            return False
        board[xStart][yStart] = tile
    
        if tile == 'X':
            otherTile = 'O'
        else:
            otherTile = 'X'
            
        tilesToFlip = []
        for xdir, ydir in [[0, 1], [1, 0], [1, 1], [1, -1], [0, -1], [-1, 0], [-1, -1], [-1, 1]]:
            x, y = xStart, yStart
            x += xdir
            y += ydir
            if self.onBoard(x, y) and board[x][y] == otherTile:
                x += xdir
                y += ydir
                if not self.onBoard(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdir
                    y += ydir
                    if not self.onBoard(x, y):
                        break
                if not self.onBoard(x, y):
                    continue
                if board[x][y] == tile:
                    while True:
                        x -= xdir
                        y -= ydir
                        if x == xStart and y == yStart:
                            break
                        tilesToFlip.append([x, y])
        if len(tilesToFlip) is 0:
            return False
        return tilesToFlip
    
    def onBoard(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7
    
    def getValidMoves(self, tile):
        validMoves = []
        for x in range(8):
            for y in range(8):
                if self.checkValidMoveWithFlips(tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves
    
    def getBoardWithValidMoves(self, tile):
        copy = self.copyBoard()
        
        for x, y in self.getValidMoves(tile):
            copy[x][y] = '.'
        return Board(copy)
    
    def makeMove(self, tile, xstart, ystart):
        copyBoard = Board(self.copyBoard())
        flipTiles = copyBoard.checkValidMoveWithFlips(tile, xstart, ystart)
        
        if flipTiles == False:
            return False
        
        copyBoard.boardArray[xstart][ystart] = tile
        for x, y in flipTiles:
            copyBoard.boardArray[x][y] = tile
        return copyBoard
        
    
    def evaluateState(self, tile):
        if tile == 'X':
            otherTile = 'O'
        else:
            otherTile = 'X'
            
        #check corners, total number of tiles, number of available moves
        value = 0
        
        #check corners
        myCorners = 0
        oppCorners = 0
        for x, y in [[0, 0], [0, 7], [7, 0], [7, 7]]:
            if self.boardArray[x][y] == tile:
                myCorners += 1
            elif self.boardArray[x][y] == otherTile:
                oppCorners += 1
                
        corners = (CORNERWEIGHT*(myCorners - oppCorners))
        
        #check total number of tiles
        myTotal = 0
        oppTotal = 0
        for row in self.boardArray:
            for space in row:
                if space == tile:
                    myTotal += 1
                elif space == otherTile:
                    oppTotal += 1
        tiles = (TILEWEIGHT*(myTotal - oppTotal))
        
        #check number of available next moves
        myMoves = 0
        oppMoves = 0
        
        myMoves = len(self.getValidMoves(tile))
        oppMoves = len(self.getValidMoves(otherTile))
        
        moves = (MOVEWEIGHT*(myMoves - oppMoves))
        value = corners + tiles + moves
        return value

class Random(object):
    def __init__(self, tile, quick):
        self.tile = tile
        self.quick = quick
        
    def getMove(self, board):
        if not self.quick:
            print "Press enter to see the computer's move"
            raw_input()
        possibleMoves = []
        for x, y in board.getValidMoves(self.tile):
            possibleMoves.append((x, y))
            
        if possibleMoves == []:
            return None
        move = random.choice(possibleMoves)
        return move
        
class Human(object):
    def __init__(self, tile):
        self.tile = tile
        
    def getMove(self, board):
        ONETHROUGHEIGHT = '1 2 3 4 5 6 7 8'.split()
        possibleMoves = []
        for x, y in board.getValidMoves(self.tile):
            possibleMoves.append((x, y))

        if possibleMoves == []:
            return None
        
        while True:

            print "Enter your move's x coordinate, or type quit to end the game."
            moveX = raw_input().lower()

            if moveX == 'quit':
                return 'quit'

            print "Enter your move's y coordinate."
            moveY = raw_input().lower()
            if moveX in ONETHROUGHEIGHT and moveY in ONETHROUGHEIGHT:
                x = int(moveX) - 1
                y = int(moveY) - 1
                
                if board.checkValidMoveWithFlips(self.tile, x, y) == False:
                    print "You can't move there, try again"
                    continue
                else:
                    break
                    
            else:
                print "That is not a valid move. Type just the x digit (or quit) followed by a return, and just the y digit followed by a return"
                print "Example: 8\n1\nwill result in the very top right corner."
                
        return (x, y)
            

class AI(object):
    def __init__(self, tile, quick, numMoves=4):
        self.tile = tile
        self.depth = numMoves
        self.quick = quick
    
    def getMove(self, board):
        if not self.quick:
            print "Press enter to see the computer's move"
            raw_input()
        return self.getBestMove(board, self.tile, self.depth)
    
    def getBestMove(self, board, tile, depth):
        bestMove = None
        maxEval = float('-infinity')
        
        player = tile
        opponent = getOtherPlayer(player)
        possibleMoves = board.getValidMoves(player)
        alpha = float('infinity')
        
        for x, y in possibleMoves:
            newBoard = board.makeMove(player, x, y)
            alpha = -self.alphaBeta(newBoard, float('-infinity'), alpha, depth - 1, getOtherPlayer(player))
            
            if alpha > maxEval:
                maxEval = alpha
                bestMove = (x, y)
        
        return bestMove
    
    def alphaBeta(self, board, alpha, beta, depth, player):
        if depth == 0:
            return board.evaluateState(player)
        
        possibleMoves = board.getValidMoves(player)
        for x, y in possibleMoves:
            newBoard = board.makeMove(player, x, y)
            currentAlpha = -self.alphaBeta(board, -beta, -alpha, depth - 1, getOtherPlayer(player))
            
            if currentAlpha >= beta:
                return beta
            
            if currentAlpha > alpha:
                alpha = currentAlpha
                
        return alpha
        
def getOtherPlayer(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'
    
def getHumanPlayers():
    print "\nEnter Number of Human Players (0, 1, or 2)"
    numPlayers = raw_input()
    playerOneHuman = False
    playerTwoHuman = False
    if numPlayers is not '0':
        if numPlayers is '1':
            print "\nWhich Player Is Human, X or [O]?"
            playerOneHuman = 'x' == raw_input().lower()
            if not playerOneHuman:
                print "Player two, 'O', will be human\n"
                playerTwoHuman = True
            else:
                print "Player one, 'X', will be human\n"
                playerTwoHuman = False
        else:
            print "Both players will be human"
            playerOneHuman = playerTwoHuman = True
    else:
        print "Both players will be computer controlled\n"
        playerOneHuman = playerTwoHuman = False
    
    return playerOneHuman, playerTwoHuman
        
    
def getRandomOrAI(player):
    output = "\nIs player " + player + " Randomly choosing, or using AI (random or [ai])?"
    print output
    playerRandom = raw_input()
    response = playerRandom.lower().startswith('r')
    if response:
        print "Player " + player + " will be random\n"
        return False
    print "Player " + player + " will be AI\n"
    return True
    
def displayIntro():
    output = "Welcome to othello!\nThis program is a text based implementation of the game Othello or Reversi.\nFirst player uses the X tile, second uses the O tile.\nThe AI player uses an alpha-beta pruning minimax algorithm with a maximum depth of 3 moves.\n"
    print output


def playAgain():
    print "Do you want to play again? ([yes] or no)"
    return not raw_input().lower().startswith('n')


def getQuick(tile):
    print "Would you like to analyze each move for " + tile + " or have it play as fast as possible ([quick] or wait?"
    return not raw_input().lower().startswith('w')
    
######################################################################################################################
while True:
    gameBoard = Board()
    playerOneHuman = False
    playerTwoHuman = False
    aiPlayerOne = False
    aiPlayerTwo = False

    displayIntro()

    playerOneHuman, playerTwoHuman = getHumanPlayers()
    if playerOneHuman == False:
        aiPlayerOne = getRandomOrAI("X")
        pOneQuick = getQuick("X")
        if aiPlayerOne:
            playerOne = AI("X", pOneQuick)
            
        else:
            playerOne = Random("X", pOneQuick)
    else:
        playerOne = Human("X")
        
    if playerTwoHuman == False:
        aiPlayerTwo = getRandomOrAI("O")
        pTwoQuick = getQuick("O")
        if aiPlayerTwo:
            playerTwo = AI("O", pTwoQuick)
        else:
            playerTwo = Random("O", pTwoQuick)
    else:
        playerTwo = Human("O")
    
    turn = "playerOne"
    
    while True:
        if turn == 'playerOne':
            displayBoard = gameBoard.getBoardWithValidMoves(playerOne.tile)
            displayBoard.drawBoard()
            
            move = playerOne.getMove(gameBoard)
            if move is not None:
                if move == 'quit':
                    print "Thanks for playing!"
                    sys.exit()
                else:
                    print "Playing an " + playerOne.tile + " at (%d, %d)" % (move[0] + 1, move[1] + 1)
                    gameBoard = gameBoard.makeMove(playerOne.tile, move[0], move[1])
                
                if gameBoard.getValidMoves(playerTwo.tile) == []:
                    if gameBoard.getValidMoves(playerOne.tile) == []:
                        break
                    turn = 'playerOne'
                else:
                    turn = 'playerTwo'
                    
        else:
            displayBoard = gameBoard.getBoardWithValidMoves(playerTwo.tile)
            displayBoard.drawBoard()
            
            move = playerTwo.getMove(gameBoard)
            if move is not None:
                if move == 'quit':
                    print "Thanks for playing!"
                    sys.exit()
                else:
                    print "Playing an " + playerTwo.tile + " at (%d, %d)" % (move[0] + 1, move[1] + 1)
                    gameBoard = gameBoard.makeMove(playerTwo.tile, move[0], move[1])
                    
                if gameBoard.getValidMoves(playerOne.tile) == []:
                    if gameBoard.getValidMoves(playerTwo.tile) == []:
                        break
                    turn = 'playerTwo'
                else:
                    turn = 'playerOne'
                    
    gameBoard.drawBoard()
    score = gameBoard.getScore()
    if score > 0:
        #player 1 wins
        print "Player 1 wins by %d tiles" % math.fabs(score)
    elif score < 0:
        #player 2 wins
        print "Player 2 wins by %d tiles" % math.fabs(score)
    else:
        #tie game
        print "Tie game!"
        
    if not playAgain():
        break;
        
        
    
    
    
    
    
    
    
    
    
    
    
    
