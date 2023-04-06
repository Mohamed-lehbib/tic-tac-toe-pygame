from constant import *
import random
import copy
import sys
import numpy as np 
import pygame, sys
from button import Button

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

BG = pygame.image.load("assets/green.png")

class Board:

    def __init__(self) -> None:
        self.squares =  np.zeros( (ROWS, COLS))
        self.empty_sqrs = self.squares #[squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
        return 0 si il n'ya pas de gagnant
        return 1 si player 1 a gagner
        return 2 si player 2 a gagner
        '''
        #gagnant vertical
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] !=0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE //2, 20)
                    fPos = (col * SQSIZE + SQSIZE //2, HEIGHT -20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        #gagnant horizontal
        for row in range(ROWS):
                if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] !=0:
                    if show:
                        color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                        iPos = (20, row * SQSIZE + SQSIZE //2)
                        fPos = (WIDTH -20, row * SQSIZE + SQSIZE //2)
                        pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                    return self.squares[row][0]

        #desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] !=0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH -20, HEIGHT -20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]

        #asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] !=0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT -20)
                fPos = (WIDTH -20, 20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        #pas de gagnant
        return 0


    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs +=1

    def empty_sqr(self,row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs ==0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player =player

    def rnd_choice(self, board):
        empty_sqra = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqra))


        return empty_sqra[idx] #return (row, col)

    def minmax(self, board, maximazing):
        #terminal case
        case = board.final_state()

        #player 1 win
        if case == 1:
            return 1, None #eval, move
        
        #player 2 win
        if case == 2:
            return -1, None

        #draw
        elif board.isfull():
            return 0, None

        if maximazing:
            max_eval = -2
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minmax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximazing:
            min_eval = 2
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minmax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move
                

    def eval(self, main_board):
        if self.level == 0:
            #choix aliatoire
            eval = 'random'
            move = self.rnd_choice(main_board)
        else:
            #minimax algorithme choix
            eval, move = self.minmax(main_board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move #move = (row, col)

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 #1 - x #2 - O
        self.gamemode = 'ai' #player vs player or player vs ai
        self.running = True
        self.show_lines()

    def show_lines(self):
        #bg
        screen.fill(BG_COLOR)
        #vertical lines
        pygame.draw.line( screen, LINE_COLOR, (SQSIZE,0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line( screen, LINE_COLOR, (WIDTH - SQSIZE,0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        #horizontal lines
        pygame.draw.line( screen, LINE_COLOR, (0,SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line( screen, LINE_COLOR, (0,HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            #designe x
            #desc ligne
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            #asc ligne
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            #designe o
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADUIS, CIRC_WIDTH)
 
    def make_move(self, row, col):
        self.board.mark_sqr(row , col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode= 'ai' if self.gamemode == 'pvp' else 'pvp'
        
    def isover(self):
        return self.board.final_state(show= True) !=0 or self.board.isfull()

    def reset(self):
        self.__init__()


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def pvp():
    #objet Game
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        #PLAY_MOUSE_POS = pygame.mouse.get_pos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_BACKSPACE: #to restart the game press backspace
                    game.reset()
                    board = game.board
                    ai = game.ai
                if event.key == pygame.K_ESCAPE: #to get back the main menu press escape 
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                #print(row, col)
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    #print(board.squares)
                    if game.isover():
                        game.running = False

        pygame.display.update()
    
def pvai():
    #objet Game
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        #OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: #to restart the game press backspace
                    game.reset()
                    board = game.board
                    ai = game.ai
                if event.key == pygame.K_ESCAPE: #to get back the main menu press escape 
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                    #print(row, col)
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                        #print(board.squares)
                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #update the screen 
            pygame.display.update()

            #ai methodes
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
        
            

        pygame.display.update()

def pvai2():
    #objet Game
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        #OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: #to restart the game press backspace
                    game.reset()
                    board = game.board
                    ai = game.ai
                if event.key == pygame.K_ESCAPE: #to get back the main menu press escape 
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                    #print(row, col)
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                        #print(board.squares)
                    if game.isover():
                        game.running = False

            ai.level = 0

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #update the screen 
            pygame.display.update()

            #ai methodes
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
        
            

        pygame.display.update()


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Play", True, "#EFE7C8")
        MENU_RECT = MENU_TEXT.get_rect(center=(360, 100))

        PVP_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(360, 250), 
                            text_input="PvP", font=get_font(50), base_color="#000000", hovering_color="White")
        PvAI_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(360, 400), 
                            text_input="PvAI", font=get_font(50), base_color="#000000", hovering_color="White")
        PvAI2_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(360, 550), 
                            text_input="PvGame", font=get_font(50), base_color="#000000", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PVP_BUTTON, PvAI_BUTTON, PvAI2_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PVP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pvp()
                if PvAI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pvai()
                if PvAI2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pvai2()

        pygame.display.update()

main_menu()