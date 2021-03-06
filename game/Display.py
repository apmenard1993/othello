def get_intro():
    output = "Welcome to othello!</br>This program is a text based implementation of the game Othello or Reversi.</br>" \
             "First player uses the X tile, second uses the O tile.</br>" \
             "The AI player uses an alpha-beta pruning minimax algorithm with a maximum depth of 3 moves.</br>"
    return output


def cli_display_intro():
    output = "Welcome to othello!\nThis program is a text based implementation of the game Othello or Reversi.\n" \
             "First player uses the X tile, second uses the O tile.\n" \
             "The AI player uses an alpha-beta pruning minimax algorithm with a maximum depth of 3 moves.\n"
    print(output)


def get_human_players():
    print("\nEnter Number of Human Players (0, 1, or 2)")
    num_players = input()
    if num_players != '0':
        if num_players == '1':
            print("\nWhich Player Is Human, X or [O]?")
            player_one_human = 'x' == input().lower()
            if not player_one_human:
                print("Player two, 'O', will be human\n")
                player_two_human = True
            else:
                print("Player one, 'X', will be human\n")
                player_two_human = False
        else:
            print("Both players will be human")
            player_one_human = player_two_human = True
    else:
        print("Both players will be computer controlled\n")
        player_one_human = player_two_human = False

    return player_one_human, player_two_human


def get_random_or_ai(player):
    output = "\nIs player " + player + " Randomly choosing, or using AI (random or [ai])?"
    print(output)
    player_random = input()
    response = player_random.lower().startswith('r')
    if response:
        print("Player " + player + " will be random\n")
        return False
    print("Player " + player + " will be AI\n")
    return True


def get_other_player(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'


def get_quick(tile):
    print("Would you like to analyze each move for " + tile + " or have it play as fast as possible ([quick] or wait?")
    return not input().lower().startswith('w')


def play_again():
    print("Do you want to play again? ([yes] or no)")
    return not input().lower().startswith('n')
