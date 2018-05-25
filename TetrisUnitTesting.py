#Imports.
from Tetris import Tetris, pygame, deepcopy, blockList, colors, CELL_SIZE, COLUMNS, ROWS, SIDEBAR_WIDTH

#Helpers for the unit-testing
tetris = Tetris()

def initializeGameObjects():
    tetris.board = tetris.makeBoard()
    tetris.newBlock()

def enableBlockMovement():
    tetris.game_over = False
    tetris.is_paused = False

#Unit-testing for Tetris.py.
#Naming convention follows as: test_[function name]_[number]().
#(Number is omitted if redundant.)
def test_makeBlock():
    block = tetris.makeBlock()
    assert block in blockList

def test_initializeGame_1():
    tetris.initializeGame()
    assert tetris.score == 0

def test_initializeGame_2():
    tetris.board = None
    tetris.initializeGame()
    assert tetris.board != None

def test_makeBoard_1():
    board = tetris.makeBoard()
    assert len(board) == ROWS

def test_makeBoard_2():
    board = tetris.makeBoard()
    assert len(board[0]) == COLUMNS

def test_newBlock_1():
    tetris.newBlock()
    assert tetris.block_x == int(COLUMNS*(1/2) - len(tetris.block[0])*(1/2))

def test_newBlock_2():
    tetris.newBlock()
    assert tetris.block_y == 0

def test_newBlock_3():
    tetris.newBlock()
    assert tetris.block in blockList

def test_newBlock_4():
    tetris.newBlock()
    assert tetris.next_block in blockList

def test_addBlockToBoard():
    tetris.board = tetris.makeBoard()
    board = deepcopy(tetris.board)
    tetris.newBlock()
    tetris.addBlockToBoard()
    assert board != tetris.board

def test_showcaseText():
    surface = tetris.window_surface.copy()
    tetris.showcaseText("Hey!", (0, 0))
    assert surface != tetris.window_surface

def test_drawGrid():
    cell = [["J"]]
    tetris.drawGrid(cell, (0, 0))
    alpha = 255
    assert tetris.window_surface.get_at((0, 0)) == colors["J"] + (alpha,)

def test_increaseScore_1():
    tetris.increaseScore(7)
    assert tetris.score == 1500

def test_increaseScore_2():
    tetris.score = 0
    tetris.increaseScore(-5)
    assert tetris.score == 0

def test_moveBlockHorizontally_1():
    initializeGameObjects()
    enableBlockMovement()
    block_x = deepcopy(tetris.block_x)
    tetris.moveBlockHorizontally(2)
    assert block_x == tetris.block_x - 2

def test_moveBlockHorizontally_2():
    initializeGameObjects()
    enableBlockMovement()
    block_x = deepcopy(tetris.block_x)
    tetris.moveBlockHorizontally(-3)
    assert block_x == tetris.block_x + 3

def test_moveDown():
    initializeGameObjects()
    enableBlockMovement()
    block_y = deepcopy(tetris.block_y)
    tetris.moveDown()
    assert block_y == tetris.block_y - 1

def test_rotateBlockClockwise():
    initializeGameObjects()
    enableBlockMovement()
    tetris.rotateBlockClockwise()
    assert tetris.block not in blockList or tetris.block == blockList[3]
    #blockList[3] is the square block, identical upon rotation.

def test_deleteRowInBoard():
    tetris.makeBoard()
    tetris.board[0] = ["J" for i in range(0, COLUMNS)]
    tetris.deleteRowInBoard(0)
    assert tetris.board[0][0] == "X"

def test_pauseOrUnpause():
    tetris.is_paused = False
    tetris.pauseOrUnpause()
    assert tetris.is_paused == True

def test_restartGame():
    tetris.game_over = True
    tetris.restartGame()
    assert tetris.game_over == False

def test_hasBoardCollision_1():
    initializeGameObjects()
    tetris.board[0] = ["J" for i in range(0, COLUMNS)]
    assert tetris.hasBoardCollision(tetris.block, (tetris.block_x, tetris.block_y)) == True

def test_hasBoardCollision_2():
    initializeGameObjects()
    tetris.block_y = ROWS
    assert tetris.hasBoardCollision(tetris.block, (tetris.block_x, tetris.block_y)) == True
