#Imports.
import random
import pygame
import sys
from copy import deepcopy

#Global constants.
CELL_SIZE = 30
COLUMNS = 12
ROWS = 20
SIDEBAR_WIDTH = 9

#List of colors associated with each block type.
colors = {
    "X": (0,   0,   0),
    "I": (255, 0,  0),
    "J": (0, 255, 0),
    "L": (0, 0, 255),
    "O": (255, 255, 0),
    "S": (0,  255, 255),
    "T": (255, 0, 255),
    "Z": (50, 100, 150),
    "BG": (255, 255, 255)
}

#List of block types. "X" indicates empty cell, other letter strings indicate
#specific block type for the block in question.
blockList = [
    [["I", "I", "I", "I"]],

    [["J", "X", "X"],
     ["J", "J", "J"]],

    [["L", "L", "L"],
     ["L", "X", "X"]],

    [["O", "O"],
     ["O", "O"]],

    [["X", "S", "S"],
     ["S", "S", "X"]],

    [["T", "T", "T"],
     ["X", "T", "X"]],

    [["Z", "Z", "X"],
     ["X", "Z", "Z"]],
]


class Tetris(object):
    def __init__(self):
        pygame.init()
        self.board_width = CELL_SIZE*COLUMNS
        self.width = CELL_SIZE*(COLUMNS+SIDEBAR_WIDTH)
        self.height = CELL_SIZE*ROWS
        self.background = [["BG" for x in range(0, COLUMNS)] for y in range(0, ROWS)]

        self.window_surface = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], CELL_SIZE)
        self.next_block = self.makeBlock()
        self.initializeGame()

    #Assigns appropriate values to attributes and methods needed upon restarting the game
    #(and starting it for the first time). A user event is called once ever 1000 ms; we
    #later use it to make the block fall down in uniform intervals.
    def initializeGame(self):
        self.board = self.makeBoard()
        self.newBlock()
        self.score = 0
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    #Assigns value to the falling block and its default coordinates, as well
    #as re-asssigning value to the previewed block. If a collision immediately occurs
    #as the block initially appears, the board has been filled to the top with
    #blocks, and thus it is a game over.
    def newBlock(self):
        self.block = deepcopy(self.next_block)
        self.next_block = self.makeBlock()
        self.block_x = int(COLUMNS*(1/2) - len(self.block[0])*(1/2))
        self.block_y = 0

        if self.hasBoardCollision(self.block, (self.block_x, self.block_y)):
            self.block = ["X"]
            pygame.display.update()
            self.game_over = True

    #One randomly chosen block is returned from the list of blocks.
    def makeBlock(self):
        return blockList[random.randint(0, len(blockList)-1)]

    #A board is created and returned, with predefined width and height
    #according to global variable assignments in ROWS and COLUMNS. All
    #cells are filled with "X", which indicates that they are empty cells.
    def makeBoard(self):
        board = []
        for i in range(0, ROWS):
            board.append([])
            for j in range(0, COLUMNS):
                board[i].append("X")
        return board

    #The non-empty cells of the current block get added to the board cells
    #in the corresponding location of the block's coordinates as this function
    #is being called.
    def addBlockToBoard(self):
        for y in range(len(self.block)):
            for x in range(len(self.block[y])):
                if self.block[y][x] != "X":
                    self.board[y+self.block_y-1][x+self.block_x] = self.block[y][x]

    #Visually displays text by rendering the text in white color on specified
    #coordinates on the game window.
    def showcaseText(self, text, coordinates):
        text_x, text_y = coordinates
        text_render = self.font.render(text, False, (255, 255, 255), (0, 0, 0))
        self.window_surface.blit(text_render, (text_x, text_y))

    #A grid gets visually realized by a square of width CELL_SIZE pixels for
    #every sublist element, with one square vertically for every sublist,
    #and one square horizontally for every element within a sublist. The value
    #of the element determines color, and in the case of value "X", is ignored.
    def drawGrid(self, grid, coordinates):
        grid_x, grid_y = coordinates
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] != "X":
                    rect = pygame.Rect((grid_x+x)*CELL_SIZE, (grid_y+y)*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.window_surface, colors[grid[y][x]], rect, 0)

    #Increases the value of the game score depending on how many consecutive
    #rows that were filled simultaneously. (Function is called on when a
    #block has been made part of the board, where a full row potentially
    #could occur.)
    def increaseScore(self, consecutiveFullRows):
        if consecutiveFullRows == 0:
            self.score += 0
        elif consecutiveFullRows == 1:
            self.score += 100
        elif consecutiveFullRows == 2:
            self.score += 300
        elif consecutiveFullRows == 3:
            self.score += 500
        elif consecutiveFullRows == 4:
            self.score += 800
        elif consecutiveFullRows > 4:
            self.score += 1500
        else:
            pass

    #Block moves horizontally (if game is not paused or a game over has not
    #occurred). If the block moves outside of the board, it is moved to the
    #closest horizontal point within the board (acts as a collision handler
    #with the "walls"). Lastly checks if a collision with the "floor" or
    #other blocks has occurred, and if not, the block's position is renewed.
    def moveBlockHorizontally(self, additional_x):
        if not self.game_over and not self.is_paused:
            new_x = self.block_x + additional_x
            if new_x < 0:
                new_x = 0
            if new_x > COLUMNS - len(self.block[0]):
                new_x = COLUMNS - len(self.block[0])
            if not self.hasBoardCollision(self.block, (new_x, self.block_y)):
                self.block_x = new_x

    #Block moves downwards one cell (if game is not paused or a game over has
    #not occurred). If a collision occurs, it is naturally assumed to be on
    #the "floor" of the board or on top of another block, so the block is
    #made part of the board. A new block is assigned after. A for-loop goes
    #through all of the rows in the board looking for full rows, in which
    #case the game score is increased accordingly.
    def moveDown(self):
        if not self.game_over and not self.is_paused:
            self.block_y += 1
            if self.hasBoardCollision(self.block, (self.block_x, self.block_y)):
                self.addBlockToBoard()
                self.newBlock()
                consecutiveFullRows = 0
                for i, row in enumerate(self.board[:]):
                    if "X" not in row:
                        self.deleteRowInBoard(i)
                        consecutiveFullRows += 1
                self.increaseScore(consecutiveFullRows)

    #Block rotates clockwise (if game is not paused or a game over has
    #not occurred). If a collision occurs as a result of the rotation, the
    #rotation assignment is cancelled.
    def rotateBlockClockwise(self):
        if not self.game_over and not self.is_paused:
            newBlock = [[self.block[y][x] for y in range(0, len(self.block))]
                        for x in range(len(self.block[0]) - 1, -1, -1)]
            if not self.hasBoardCollision(newBlock, (self.block_x, self.block_y)):
                self.block = newBlock

    #Deletes a row (sublist of elements) in the board according to the given
    #argument. Board is then recreated with an empty row of cells at the top.
    def deleteRowInBoard(self, row_index):
        del self.board[row_index]
        self.board = [["X" for i in range(0, COLUMNS)]] + self.board

    #Changes the value of attribute is_paused to True if it is False, and
    #vice versa.
    def pauseOrUnpause(self):
        self.is_paused = not self.is_paused

    #If a game over has occurred, it re-initializes the game.
    def restartGame(self):
        if self.game_over:
            self.initializeGame()
            self.game_over = False

    #Checks collision between a given block and the board. If the block and
    #the board have one cell (or more) that overlaps, coordinatewise, it is
    #registered as a collision. If an index error occurs, it is also registered
    #as a collision (block is outside of board boundaries).
    def hasBoardCollision(self, block, blockCoordinates):
        block_x, block_y = blockCoordinates
        for y in range(len(block)):
            for x in range(len(block[y])):
                try:
                    if block[y][x] != "X" and self.board[y + block_y][x + block_x] != "X":
                        return True
                except IndexError:
                    return True
        return False

    #Function defines keyboard inputs, frame rate, and has a while loop in
    #which the game continuously updates. Here the game is visually updated
    #and a for-loop acts as an event listener for user input, primarily.
    #pygame.USERVENT, which is set to be added to the event queue every
    #second in initializeGame(), moves the block downwards one cell, which
    #thus occurs once every second automatically.
    def runGame(self):
        key_actions = {
            'ESCAPE':	sys.exit,
            'LEFT': lambda: self.moveBlockHorizontally(-1),
            'RIGHT': lambda: self.moveBlockHorizontally(+1),
            'DOWN': lambda: self.moveDown(),
            'UP':		self.rotateBlockClockwise,
            'p':		self.pauseOrUnpause,
            'RETURN':	self.restartGame
        }

        pygame.key.set_repeat(50)
        self.is_paused = False
        self.game_over = False

        clock = pygame.time.Clock()
        print(pygame.event.get())

        while True:
            self.window_surface.fill((0, 0, 0))
            if self.game_over:
                self.showcaseText("Game over!", (self.board_width+CELL_SIZE*2, CELL_SIZE*7))
                self.showcaseText("Final score above.", (self.board_width+(CELL_SIZE), CELL_SIZE*8))
                self.showcaseText("Press Enter to restart.", (self.board_width+(CELL_SIZE)*(1/2), CELL_SIZE*10))
            elif self.is_paused:
                self.showcaseText("Paused!", (self.board_width+CELL_SIZE*3, CELL_SIZE*7))
            self.showcaseText("Next:", (self.board_width+CELL_SIZE*3, CELL_SIZE*(1/2)))
            self.showcaseText("Score: %d" % (self.score),
                              (self.board_width+CELL_SIZE*3, CELL_SIZE*5))
            self.drawGrid(self.background, (0, 0))
            self.drawGrid(self.board, (0, 0))
            self.drawGrid(self.block, (self.block_x, self.block_y))
            self.drawGrid(self.next_block, (COLUMNS+3, 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.moveDown()
                elif event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()

            clock.tick(30)


if __name__ == '__main__':
    tetrisGame = Tetris()
    tetrisGame.runGame()
