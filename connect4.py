import numpy as np
import pygame
import sys
import math
import random

# codes of colors
colors = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'li_black': (69, 69, 69),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'gray': (192, 192, 192),
    'li_gray': (229, 228, 226)
}


# check if there is any space left in the board game or not
def board_hasSpace(boardGa, column):
    return boardGa[row_game - 1][column] == 0


# find the lowest row
def lowestRow(boardGa, column):
    for r in range(row_game):
        if boardGa[r][column] == 0:
            return r


# print the board game
def print_board(boardGa):
    print(np.flip(boardGa, 0))


# check for win
def check_win(boardGa, turnPl):

    for j in range(column_game - 3):  # check row
        for i in range(row_game):
            if boardGa[i][j] == boardGa[i][j + 1] == boardGa[i][j + 2] == boardGa[i][j + 3] == turnPl:
                return True

    for j in range(column_game):      # check column
        for i in range(row_game - 3):
            if boardGa[i][j] == boardGa[i + 1][j] == boardGa[i + 2][j] == boardGa[i + 3][j] == turnPl:
                return True

    return False


# check if the game is draw or not
def gameIsDraw(boardGa):

    for i in range(row_game):
        if 0 in boardGa[i]:
            return False
    return True


# draw the board game
def draw_board(boardGa, turnPl):

    for j in range(column_game):
        for i in range(row_game):
            pygame.draw.rect(screen, colors['blue'], (j * sizeOfGame, i * sizeOfGame, sizeOfGame, sizeOfGame))
            pygame.draw.circle(screen, colors['gray'], (
                int(j * sizeOfGame + sizeOfGame / 2), int(i * sizeOfGame + sizeOfGame / 2)), r_circle)

    for j in range(column_game):
        for i in range(row_game):
            if boardGa[i][j] == 1:
                pygame.draw.circle(screen, colors['red'], (
                    int(j * sizeOfGame + sizeOfGame / 2), height - int(i * sizeOfGame + sizeOfGame / 2)), r_circle)
            elif boardGa[i][j] == 2:
                pygame.draw.circle(screen, colors['yellow'], (
                    int(j * sizeOfGame + sizeOfGame / 2), height - int(i * sizeOfGame + sizeOfGame / 2)), r_circle)

    if turnPl == 0:
        pygame.draw.circle(screen, colors['red'], (width - 10, height - 10), 10)
    else:
        pygame.draw.circle(screen, colors['yellow'], (width - 10, height - 10), 10)

    pygame.display.update()


# min-max algorithm with pruning
def minimaxWithPru(boardGa, depthGa, alpha, beta, maxTurn, minTurn):
    valid_locations = valid_locsGame(boardGa)

    if depthGa == 0:
        return None, heuristic_Cal(boardGa, 2)

    elif node_final(boardGa):
        if check_win(boardGa, 2):
            return None, float('inf')
        elif check_win(boardGa, 1):
            return None, float('-inf')
        else:
            return None, 0

    if maxTurn:
        best = float('-inf')
        column = random.choice(valid_locations)

        for j in valid_locations:
            i = lowestRow(boardGa, j)
            boardCp = boardGa.copy()
            boardCp[i][j] = 2
            result = minimaxWithPru(boardCp, depthGa - 1, alpha, beta, False, True)
            if result[1] > best:
                best = result[1]
                column = j
            alpha = max(alpha, best)
            if alpha >= beta:
                break

        return column, best

    elif minTurn:
        best = float('inf')
        column = random.choice(valid_locations)

        for j in valid_locations:
            i = lowestRow(boardGa, j)
            boardCp = boardGa.copy()
            boardCp[i][j] = 1
            result = minimaxWithPru(boardCp, depthGa - 1, alpha, beta, True, False)
            if result[1] < best:
                best = result[1]
                column = j
            beta = min(beta, best)
            if alpha >= beta:
                break

        return column, best

    else:
        return None, None


# min-max algorithm without pruning
def minimax(boardGa, depthGa, maxTurn, minTurn):
    valid_locations = valid_locsGame(boardGa)

    if depthGa == 0:
        return None, heuristic_Cal(boardGa, 2)

    elif node_final(boardGa):
        if check_win(boardGa, 2):
            return None, float('inf')
        elif check_win(boardGa, 1):
            return None, float('-inf')
        else:
            return None, 0

    if maxTurn:
        best = float('-inf')
        column = random.choice(valid_locations)

        for j in valid_locations:
            i = lowestRow(boardGa, j)
            boardCp = boardGa.copy()
            boardCp[i][j] = 2
            result = minimax(boardCp, depthGa - 1, False, True)
            if result[1] > best:
                best = result[1]
                column = j

        return column, best

    elif minTurn:
        best = float('inf')
        column = random.choice(valid_locations)

        for j in valid_locations:
            i = lowestRow(boardGa, j)
            boardCp = boardGa.copy()
            boardCp[i][j] = 1
            result = minimax(boardCp, depthGa - 1, True, False)
            if result[1] < best:
                best = result[1]
                column = j

        return column, best

    else:
        return None, None


# find valid locations of the board game
def valid_locsGame(boardGa):
    valid_locations = [j for j in range(column_game) if board_hasSpace(boardGa, j)]
    return valid_locations


# check if we reach to the final node of the tree or not
def node_final(boardGa):
    if check_win(boardGa, 1):
        return True

    elif check_win(boardGa, 2):
        return True

    elif len(valid_locsGame(boardGa)) == 0:
        return True

    else:
        return False


# calculate heuristic
def heuristic_Cal(boardGa, turnPl):
    score = 0

    for r in range(row_game):                     # scores for rows
        arrOfRow = list()
        for i in list(boardGa[r, :]):
            arrOfRow.append(int(i))
        for c in range(column_game - 3):
            fourPic = arrOfRow[c:c + 4]
            score += heu_score(fourPic, turnPl)


    for c in range(column_game):                  # scores for columns
        arrOfCol = list()
        for i in list(boardGa[:, c]):
            arrOfCol.append(int(i))
        for r in range(row_game - 3):
            fourPic = arrOfCol[r:r + 4]
            score += heu_score(fourPic, turnPl)

    return score


# find scores for heuristic
def heu_score(fourPi, maxPl):
    score = 0
    minPl = 2 if maxPl == 1 else 1
    countMax = fourPi.count(maxPl)
    countZero = fourPi.count(0)
    countMin = fourPi.count(minPl)

    if countMax == 4:                         # the agent is going to win absolutely
        score += 200
    elif countMax == 3 and countZero == 1:    # the agent is going to win probably
        score += 10
    elif countMax == 2 and countZero == 2:    # the agent is close to win
        score += 4

    if countMin == 3 and countZero == 1:      # the opposite is going to win
        score -= 8

    return score


row_game = 6
column_game = 7
board_game = np.zeros((row_game, column_game))
print_board(board_game)
game_over = False
turn = 0

pygame.init()

sizeOfGame = 110
width = column_game * sizeOfGame
height = row_game * sizeOfGame
r_circle = int(sizeOfGame / 2 - 5)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect Four")
pygame.display.update()

font = pygame.font.SysFont("calibri", 30)
fontWin = pygame.font.SysFont("monospace", 75)
singlePlayer = False
multiPlayer = False
run = True
depth = 0
playGame_menu = False
main_menu = True
started_game = False
level_menu = False

while run:
    screen.fill(colors['gray'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # draw main menu
    if main_menu:
        label = font.render("Welcome to ConnectFour!", 1, colors['red'])
        screen.blit(label, (230, 100))
        menu_play = pygame.draw.rect(screen, colors['blue'], (300, 180, 170, 90), 0, 5)
        pygame.draw.rect(screen, colors['black'], (300, 180, 170, 90), 5, 5)
        label = font.render("1.Play Game", 1, colors['black'])
        screen.blit(label, (310, 210))

        if menu_play.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(500)
            playGame_menu = True
            main_menu = False

        menu_exit = pygame.draw.rect(screen, colors['blue'], (300, 400, 170, 90), 0, 5)
        pygame.draw.rect(screen, colors['black'], (300, 400, 170, 90), 5, 5)
        label = font.render("0. Exit", 1, colors['black'])
        screen.blit(label, (340, 430))

        if menu_exit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(500)
            run = False

    # draw play game menu
    elif playGame_menu and not started_game:
        menu_single = pygame.draw.rect(screen, colors['blue'], (300, 180, 170, 90), 0, 5)
        pygame.draw.rect(screen, colors['black'], (300, 180, 170, 90), 5, 5)
        label = font.render("SinglePlayer", 1, colors['black'])
        screen.blit(label, (310, 210))

        if menu_single.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(500)
            playGame_menu = False
            main_menu = False
            level_menu = True

        menu_multi = pygame.draw.rect(screen, colors['blue'], (300, 400, 170, 90), 0, 5)
        pygame.draw.rect(screen, colors['black'], (300, 400, 170, 90), 5, 5)
        label = font.render("MultiPlayer", 1, colors['black'])
        screen.blit(label, (320, 430))

        if menu_multi.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(500)
            playGame_menu = False
            main_menu = False
            multiPlayer = True
            started_game = True

    # draw the agent levels menu
    elif level_menu and not started_game:
        menu_easy = pygame.draw.rect(screen, colors['blue'], (300, 90, 170, 90), 0, 5)
        pygame.draw.rect(screen, colors['black'], (300, 90, 170, 90), 5, 5)
        label = font.render("Easy", 1, colors['black'])
        screen.blit(label, (360, 120))

        if menu_easy.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(500)
            depth = 2
            level_menu = False
            singlePlayer = True
            started_game = True

        menu_medium = pygame.draw.rect(screen, colors['blue'], (300, 320, 170, 90), 0, 5)
        pygame.draw.rect(screen, colors['black'], (300, 320, 170, 90), 5, 5)
        label = font.render("Medium", 1, colors['black'])
        screen.blit(label, (340, 350))

        if menu_medium.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(500)
            depth = 4
            level_menu = False
            singlePlayer = True
            started_game = True

        menu_hard = pygame.draw.rect(screen, colors['blue'], (300, 530, 170, 90), 0, 5)
        pygame.draw.rect(screen, colors['black'], (300, 530, 170, 90), 5, 5)
        label = font.render("Hard", 1, colors['black'])
        screen.blit(label, (350, 560))

        if menu_hard.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(500)
            depth = 6
            level_menu = False
            singlePlayer = True
            started_game = True

    if started_game:
        draw_board(board_game, turn)

    pygame.display.update()

    # game has been started
    while not game_over and (singlePlayer or multiPlayer):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if multiPlayer:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, colors['gray'], (0, 0, width, sizeOfGame))

                    if turn == 0:
                        x_click = event.pos[0]
                        col = int(math.floor(x_click / sizeOfGame))

                        if board_hasSpace(board_game, col):
                            row = lowestRow(board_game, col)
                            board_game[row][col] = 1

                            if check_win(board_game, 1):
                                print("Red wins!")
                                game_over = True

                    else:
                        x_click = event.pos[0]
                        col = int(math.floor(x_click / sizeOfGame))

                        if board_hasSpace(board_game, col):
                            row = lowestRow(board_game, col)
                            board_game[row][col] = 2

                            if check_win(board_game, 2):
                                print("Yellow wins!")
                                game_over = True

                    if gameIsDraw(board_game) and not game_over:
                        print("Draw!")
                        game_over = True

                    turn += 1
                    turn %= 2
                    draw_board(board_game, turn)


            elif singlePlayer:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, colors['gray'], (0, 0, width, sizeOfGame))

                    if turn == 0:
                        x_click = event.pos[0]
                        col = int(math.floor(x_click / sizeOfGame))

                        if board_hasSpace(board_game, col):
                            row = lowestRow(board_game, col)
                            board_game[row][col] = 1

                            if check_win(board_game, 1):

                                print("You win!")
                                game_over = True

                            turn += 1
                            turn %= 2
                            draw_board(board_game, turn)

                        if gameIsDraw(board_game) and not game_over:
                            print("Draw!")
                            game_over = True

        if turn == 1 and not game_over and singlePlayer:

            if depth == 2 or depth == 4:
                pygame.time.wait(500)

            col, scoreOfMinMax = minimaxWithPru(board_game, depth, -math.inf, math.inf, True, False)

            if board_hasSpace(board_game, col):
                row = lowestRow(board_game, col)
                board_game[row][col] = 2

                if check_win(board_game, 2):
                    print("You lose!")
                    game_over = True

                if gameIsDraw(board_game) and not game_over:
                    print("Draw!")
                    game_over = True

                turn += 1
                turn %= 2
                draw_board(board_game, turn)

        if game_over:
            print_board(board_game)
            pygame.time.wait(3000)
            main_menu = True
            started_game = False
            singlePlayer = False
            multiPlayer = False
            game_over = False
            turn = 0
            board_game = np.zeros((row_game, column_game))

print("Game Exited!")
