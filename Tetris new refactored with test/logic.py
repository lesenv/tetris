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
        new = ["X" if i else "." for i in line]
        print(new)

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
            block_preview = Block()
        else:
            block_preview = block
        self.preview_block = block_preview
        self.active_block = block
        self._new_Block(block = self.active_block)
        
    def _get_width(self) -> int:
        '''return width of playmatrix'''
        return len(self.playmatrix[0])
        
    def _get_height(self) -> int:
        '''return height of playmatrix'''
        return len(self.playmatrix)

    def _active_block_to_background(self):
        '''
        when Block stops moving and
        becomes part of the Background

        ?? storing color ??
        ?? or in GUI ??
        '''
        self._send_active_block_2_background()
        self._new_Block()
        
    def _send_active_block_2_background(self):
        x, y = self.active_block_pos
        for i, j, el in self.active_block:
            self.background_blocks[x+i][y+j] = el

    def _new_Block(
            self,
            block = None,
            pos = None
            ) -> None:
        '''
        create new Block:
        - deactivate the active Block
        - activate the preview block
        - create a new one for the preview
        '''
        # active getting from the preview block
        if not self.preview_block:
            raise BlockingIOError("no preview_block, too bad. in _new_Block()")
        self.active_block = self.preview_block
        if not block:
            # if not given, _add_Block needs a Block()
            block = Block()
        self._add_Block(block, pos)

    def _add_Block(
            self,
            block = None,
            pos = None
            ) -> None:
        '''        
        Check if there is no Block blocking
        the new one,
        else lose the Game!!
        '''
        # if pos is not given,
        # take the top-middle
        if not pos:
            pos =  [0, int((len(self.playmatrix[0])-self.active_block.get_width()+1)/2)]
        self.active_block_pos = pos
        if self._is_block_free(self.active_block, pos):
          self._insert_active_block()
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


### needed?? ###
    def _get_block_pos(self, block):
        '''DOESN'T WORK yet
        perhaps not needed
        '''
        x, y = self.active_block_pos
        for i in range(block.get_width()):
            for j in range(block.get_width()):
                _x = x + i
                _y = y + j
                yield [_x, _y]

          
    def _insert_active_block(self):
        '''
        copy active block to playmatrix
        '''
        ablock = self.active_block
        x, y = self.active_block_pos
        bw = ablock.get_width()
        bh = ablock.get_height()
        for i in range(bw):
            for j in range(bh):
                _x = x + i
                _y = y + j
                self.playmatrix[_x][_y] = ablock.block[j][i]


    def _erase_active_block(self):
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
                
    def _counting(self, matrix, what_to_count = None):
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
            
    def _fall_down(self):
        '''
        active Block falls a step,
        if it's not at the bottom
        '''
        if self.active_block_pos[0] + self.active_block.get_height() >= self._get_height() - 1:
            raise BlockTooLowError
        #else: go down
        self.active_block_pos[0] += 1
                                        
    def _go_left(self):
        '''
        if not at the left border, go left
        '''
        if self.active_block_pos[1] == 0:
            raise BlockTooLeftError
        #else: go left
        self.active_block_pos[1] -= 1
            
    def _go_right(self):
        '''
        if not at the right border, go right
        '''
        # Block with height because
        # Block is turned
        if self.active_block_pos[1] + self.active_block.get_height() + 1 > self._get_width():
            raise BlockTooRightError(f"right border is right there, so stop")#:\nself.active_block_pos[1] = {self.active_block_pos[1]}\nself.active_block.get_width() = {self.active_block.get_width()}\nself.get_width() = {self.get_width()}")
        self.active_block_pos[1] += 1

    def _turn_active_block(self):
        self.active_block.turn()

    def _safe_active_block(self):
        self.safe_block = Block(block = self.active_block.block)
        self.safe_pos = self.active_block_pos

    def _get_saved_block(self):
        self.active_block = self.safe_block
        self.active_block_pos = self.safe_pos
            
    def move(self, direction):
        '''
            First try, then Check if there is a
            collision (counting went down)
        '''
        # first counting,
        before = self._counting(self.playmatrix)
        # then deleting old block,
        self._erase_active_block()
        # then move block (old -> new)
        try:
                self._safe_active_block()
                if direction == MOVE_DOWN:
                    self._fall_down()
                elif direction == MOVE_LEFT:
                    self._go_left()
                elif direction == MOVE_RIGHT:
                    self._go_right()
                elif direction == MOVE_TURN:
                    self._turn_active_block()
        except BlockTooRightError as e:
            #self.active_block_pos[1] = self.get_width()-self.active_block.get_width()
            pass
        except BlockTooLeftError as e:
            print("went too left", e)
            self.active_block_pos[1] = 0
        except BlockTooLowError:
             self._active_block_to_background()
        finally:
            try:
                # input new block if no error found
                self._insert_active_block()
            except IndexError:
                # if another Error saving  don't move, get the old active_block back
                before = 100000

            if self._counting(self.playmatrix) < before:
                # if before != after: block blocked, reverse movement
                # first reset to background
                self.draw_background_blocks()
                # then reverse the movement
                self._get_saved_block()
                self._insert_active_block()

    def draw_background_blocks(self):
        for i, row in enumerate(self.background_blocks):
            for j , el in enumerate(row):
                self.playmatrix[i][j] = el

            
    def print_me(self):
        '''
        print playmatrix nicely
        to be called from outside
        '''
        print_matrix(self._combined_matrix())
        
    def _combined_matrix(self):
        combined = self.playmatrix
        for i, line in enumerate(self.playmatrix):
            for j in line:
                if self.background_blocks[i][j]:
                    combined[i][j] = 1
        return combined
                    
if __name__ == "__main__":
    print("LOS")
    block1 = Block()
    tetris = Playscreen(12, 6, block1)
    tetris.print_me()
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
        print(i)
        tetris.print_me()
        tetris.move(MOVE_RIGHT)
    tetris.print_me()
    print("go left to the other side")
    for _ in range(10):
        tetris.move(MOVE_LEFT)
    tetris.print_me()
    print("turn")
    tetris.move(MOVE_TURN)
    tetris.print_me()
    print("Fall thrice")
    for i in range(5):
        tetris.move(MOVE_DOWN)
        print(i)
        tetris.print_me()
