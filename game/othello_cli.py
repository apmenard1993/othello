import math
import sys

from game import Display
from game.AI import AI
from game.Board import Board
from game.Human import Human
from game.Random import Random

######################################################################################################################
# Program Loop
while True:
    gameBoard = Board()
    aiPlayerOne = False
    aiPlayerTwo = False

    Display.cli_display_intro()

    playerOneHuman, playerTwoHuman = Display.get_human_players()
    if not playerOneHuman:
        aiPlayerOne = Display.get_random_or_ai("X")
        pOneQuick = Display.get_quick("X")
        if aiPlayerOne:
            playerOne = AI("X", pOneQuick)

        else:
            playerOne = Random("X", pOneQuick)
    else:
        playerOne = Human("X")

    if not playerTwoHuman:
        aiPlayerTwo = Display.get_random_or_ai("O")
        pTwoQuick = Display.get_quick("O")
        if aiPlayerTwo:
            playerTwo = AI("O", pTwoQuick)
        else:
            playerTwo = Random("O", pTwoQuick)
    else:
        playerTwo = Human("O")

    turn = "playerOne"

    # Game Loop
    while True:
        if turn == 'playerOne':
            displayBoard = gameBoard.get_board_with_valid_moves(playerOne.tile)
            displayBoard.draw_board()

            move = playerOne.get_move(gameBoard)
            if move is not None:
                if move == 'quit':
                    print("Thanks for playing!")
                    sys.exit()
                else:
                    print("Playing an " + playerOne.tile + " at (%d, %d)" % (move[0] + 1, move[1] + 1))
                    gameBoard = gameBoard.make_move(playerOne.tile, move[0], move[1])

                if not gameBoard.get_valid_moves(playerTwo.tile):
                    if not gameBoard.get_valid_moves(playerOne.tile):
                        break
                    turn = 'playerOne'
                else:
                    turn = 'playerTwo'

        else:
            displayBoard = gameBoard.get_board_with_valid_moves(playerTwo.tile)
            displayBoard.draw_board()

            move = playerTwo.get_move(gameBoard)
            if move is not None:
                if move == 'quit':
                    print("Thanks for playing!")
                    sys.exit()
                else:
                    print("Playing an " + playerTwo.tile + " at (%d, %d)" % (1 + move[0], 1 + move[1]))
                    gameBoard = gameBoard.make_move(playerTwo.tile, move[0], move[1])

                if not gameBoard.get_valid_moves(playerOne.tile):
                    if not gameBoard.get_valid_moves(playerTwo.tile):
                        break
                    turn = 'playerTwo'
                else:
                    turn = 'playerOne'

    # End Game Screen
    gameBoard.draw_board()
    score = gameBoard.get_score()
    if score > 0:
        # player 1 wins
        print("Player 1 wins by %d tiles" % math.fabs(score))
    elif score < 0:
        # player 2 wins
        print("Player 2 wins by %d tiles" % math.fabs(score))
    else:
        # tie game
        print("Tie game!")

    if not Display.play_again():
        break
