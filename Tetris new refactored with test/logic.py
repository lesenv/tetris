#pylint:disable=C0103 #don't care about snake_case
'''Logic of Tetris
unifying moves fall(), go_left() and go_right
to handle with exceptions??
then using constants like pygame.K_UP: logic.MOVE_DOWN, .MOVE_RIGHT, MOVE_LEFT
'''
from Block import Block
from Exceptions import *
'''
setting global constants for easily using in methods
'''
MOVE_DOWN = "fall"
MOVE_LEFT = "left"
MOVE_RIGHT = "right"
MOVE_TURN = "turn"

def print_matrix(matrix : list[list[int]]) -> None:
    '''
    printing nicely a matrix
    for DEBUGGING purposes
    '''
    for line in matrix:
        print(line)

def zero_matrix(width : int, height : int) -> list[list[int]]:
    '''
    return 0-matrix with given
    width and height
    '''
    return [[0 for i in range(width)] for j in range(height)]
    


class Playscreen():
    '''
    giving a playscreen inhabiting
    some blocks, not block-blocking,
    don't let them get out of bound'
    '''
    def __init__(
            self,
            width: int,
            height: int,
            block: Block | None = None
            ) -> None:
        # Playground and background
        self.playmatrix = zero_matrix(width, height)
        self.background_blocks = zero_matrix(width, height)
        # preview: new Block
        # active Block given?
        if not block:
            block = Block()
        self.preview_block = block
        self.active_block = None # activated in _add_Block by copying from preview
        self.active_block_pos = [0,0]
        self._add_Block(block = self.active_block)
        
    def get_width(self) -> int:
        '''return width of playmatrix'''
        return len(self.playmatrix[0])
        
    def get_height(self) -> int:
        '''return height of playmatrix'''
        return len(self.playmatrix)

    def active_block_to_background(self):
        '''
        when Block stops moving and
        becomes part of the Background

        ?? storing color ??
        ?? or in GUI ??
        '''

    def new_Block(
            self,
            block = None,
            pos = None
            ) -> None:
        '''
        create new Block:
        - deactivate the active Block
        - activate the preview block
    !!!!!!!                        !!!!!!!!
    !!! Not done in add_Block() anymore !!!
    !!!      pos, too!                  !!!
    !!!!!!!                        !!!!!!!!
        - create a new one for the preview
        '''
        #self.active_Block to background, then None
        self._add_Block(block, pos)

    def _add_Block(
            self,
            block = None,
            pos = None
            ) -> None:
        '''
        - active_block to background
        - active_block getting from
           preview_block
        - preview_block new Block(),
           if not given block
        
        Check if there is no Block blocking
        the new one,
        else lose the Game!!
        '''
        # copy active_block to background
        self.active_block_to_background()
        # active getting from the preview block
        # else new one
        if not self.preview_block:
            raise BlockingIOError("no preview_block, too bad. in _add_Block()")
        self.active_block = self.preview_block
        # if pos is not given,
        # take the top-middle    
        if not pos:
            pos =  [0, int((len(self.playmatrix[0])-self.active_block.get_width()+1)/2)]
        self.active_block_pos = pos
        if self._is_block_free(self.active_block, pos):
# DEBUGGING
#          print_matrix(block.block)
#          inserting active_block into playscreen
          self.insert_active_block()
        else:
            #Exception and lose game
            pass
        # preview getting from above
        # if not given, creating a new one
        self.preview_block = block if block else Block()
        
    def _is_block_free(self, block: Block, pos: list[int, int]) -> bool:
        '''
        return True if block isn't colliding
        with background, otherwise False
        '''
        x, y = pos
        I, J = block.get_width(), block.get_height()
        for i in range(I):
            for j in range(J):
                _x = x + i
                _y = y + j
                if self.playmatrix[_x][_y] and self.active_block.block[i][j]:
                    # self.playmatrix should be the same as self.background_blocks
                    return False
        return True

    def get_block_pos(self, block, abs = True):
        '''DOESN'T WORK yet
        perhaps not needed
        '''
        x, y = self.active_block_pos
        for i in range(block.get_width()):
            for j in range(block.get_width()):
                _x = x + i
                _y = y + j
                yield [_x, _y]

          
    def insert_active_block(self):
        '''
        copy active block to playmatrix
        '''
        ablock = self.active_block
        x, y = self.active_block_pos
#          for _x, _y in self.get_block_pos(block):
#                self.playmatrix[_x][_y] = block.block[y-_y][x-_x]
# DEBUGGING
#          print(f"erase block {block} at {x, y}")
#          self.playmatrix = zero_matrix(len(self.playmatrix[0]), len(self.playmatrix))
        bw = ablock.get_width()#
        bh = ablock.get_height()
        for i in range(bw):
            for j in range(bh):
#                print(i,j)
                _x = x + i
                _y = y + j
                self.playmatrix[_x][_y] = ablock.block[j][i]
#          print("alt:", self.playmatrix)
                
    def erase_active_block(self):
        '''
        delete active block from playmatrix
        '''
        ablock = self.active_block
        x, y = self.active_block_pos
        # just call functions once,
        # not every turn in for-loops
        bw = ablock.get_width()
        bh = ablock.get_height()
        for i in range(bw):
            for j in range(bh):
#              print(i,j)
                _x = x + i
                _y = y + j
                self.playmatrix[_x][_y] = 0
                
    def counting(self, matrix, what_to_count = None):
        '''
        count how many what_to_count-elements there are
        if None, counting how many non-Zeros
        '''
        count = 0
        if what_to_count:
            for row in matrix:
                count += row.count(what_to_count)
        else:
            for row in matrix:
                for el in row:
                    if el:
                        count += 1
        return count
            
    def fall_down(self):
        '''
        active Block falls a step,
        if it's not at the bottom
        '''
        if self.active_block_pos[0] + self.active_block.get_height() >= self.get_height() - 1:
            raise BlockTooLowError
        #else: go down
        self.active_block_pos[0] += 1
                                        
    def go_left(self):
        '''
        if not at the left border, go left
        '''
        if self.active_block_pos[1] == 0:
            raise BlockTooLeftError
        #else: go left
        self.active_block_pos[1] -= 1
            
    def go_right(self):
        '''
        if not at the right border, go right
        '''
        if self.active_block_pos[1] + self.active_block.get_width() + 1 >= self.get_width():
            raise BlockTooRightError(f"right border is right there, so stop") #:\nself.active_block_pos[1] = {self.active_block_pos[1]}\nself.active_block.get_width() = {self.active_block.get_width()}\nself.get_width() = {self.get_width()}")
        # if there is another Block at the right, don't go right
        y, x = self.active_block_pos
        for i, j, el in self.active_block.block:
            if not el:
                continue
            _x = x + j
            _y = y + i
            if self.background_blocks[_x][_y]:
                raise BlockTooRightError("there is another Block right to you, so don't go any more right")
        #else: go right
        self.active_block_pos[1] += 1

    def turn(self):
        dummy = Block(block = self.active_block.block)
        absx, absy = self.active_block_pos
        dummy.turn()
        for j, row in enumerate(dummy.block):
            for i, el in enumerate(row):
                if dummy.block[j][i] and self.background_blocks[absy+j][absx+i]:
                    raise BlockBlockedError("wanting to turn but some Block is in the way")
        self.active_block.turn()
            
    def move(self, direction):
        '''
        !!! First try, then Check if there is a
        !!! collision, Not in every sub function 
        to be called from outside
        ??? Change all the turn, fall and go_?-
        ??? functions to __-functions?
        '''
        # first counting,
        before = self.counting(self.playmatrix)
        # then deleting old block,
        self.erase_active_block()
        # then move block (old -> new)
        try:
                self.dummy = self.active_block
                if direction == MOVE_DOWN:
                    self.fall_down()
                elif direction == MOVE_LEFT:
                    self.go_left()
                elif direction == MOVE_RIGHT:
                    self.go_right()
                elif direction == MOVE_TURN:
                    self.turn()
                after = self.counting(self.playmatrix)
        except BlockTooRightError as e:
            #self.active_block_pos[1] = self.get_width()-self.active_block.get_width()
            print("went too right", e)
        except BlockTooLeftError:
            self.active_block_pos[1] = 0
        except BlockTooLowError:
            pass
#                self.active_block_2_background
#                self.new_Block()
        except BlockBlockedError:
# later there are Others when old blocks in the way
# make another Exception!!!
            # didn't turn, just dummy
            pass
        # input new block if no error found
        self.insert_active_block()
##############                    after = self.counting(self.playmatrix)
# DEBUGGING
#            print(f"{direction}: before: {before}, after: {after}")
#        if before != after: block blocked, reverse movement
            
    def print_me(self):
        '''
        print playmatrix nicely
        to be called from outside
        '''
        print_matrix(self.playmatrix)
        

if __name__ == "__main__":
    print("LOS")
    tetris = Playscreen(6,17)
    tetris.print_me()
    print("creating a block")
    block1 = Block()
    tetris.preview_block = block1
    print("adding a block:")
    print_matrix(block1.block)
    tetris._add_Block(block1)
    print("printing")
    tetris.print_me()
    print("turn")
    tetris.move(MOVE_TURN)
    tetris.print_me()
    print("Fall twice")
    tetris.move(MOVE_DOWN)
    tetris.move(MOVE_DOWN)
    tetris.print_me()
    print("go right to the most")
    for i in range(10):
        tetris.move(MOVE_RIGHT)
    tetris.print_me()
    print("go left to the other side")
    for i in range(10):
        tetris.move(MOVE_LEFT)
    tetris.print_me()
    print("turn")
    tetris.move(MOVE_TURN)
    tetris.print_me()
    
