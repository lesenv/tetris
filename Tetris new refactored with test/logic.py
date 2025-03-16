'''
unifying moves fall(), go_left() and go_right to handle with exceptions?? then using constants like pygame.K_UP: logic.MOVE_DOWN, .MOVE_RIGHT, MOVE_LEFT
'''
from random import choice

class BlockMovingError(IndexError):
    '''
    template for different types when
    moving Blocks out of the Box of
    the playscreen
    '''

class BlockTooLowError(BlockMovingError):
    '''
    when the active Block moves
    to the last line
    '''
    
class BlockTooRightError(BlockMovingError):
    '''
    when the active Block moves
    too right out of the playscreen
    '''
    
class BlockTooLeftError(BlockMovingError):
    '''
    when the active Block moves
    too left out of the playscreen
    '''
    
class BlockBlockedError(BlockMovingError):
    '''
    when trying to move to or creating
    a Block interfering with an already
    existing Block
    '''
'''
setting global constants for easily using in methods
'''
MOVE_DOWN = "fall"
MOVE_LEFT = "left"
MOVE_RIGHT = "right"
MOVE_TURN = "turn"

Z_BLOCK = [[1,1,0],[0,1,1]]
S_BLOCK = [[0,1,1],[1,1,0]]
BLOCKS = [Z_BLOCK, S_BLOCK]

def print_matrix(m):
    '''printing nicely a matrix'''
    for line in m:
        print(line)

def zero_matrix(width, height):
    '''
    return 0-matrix with given
    width and height
    '''
    return [[0 for i in range(width)] for j in range(height)]
    

class Block():
        '''
        return a tetris-block, able to turn
        '''
        def __init__(
            self,
            block = None
            ):
            if not block:
                block = choice(BLOCKS)
            self.block = block
                
        def get_width(self):
            return len(self.block[0])
            
        def get_height(self):
            return len(self.block)

        def turn(self):
            rotated = list(zip(*self.block[::-1]))
            self.block = list(list(x) for x in rotated)
            return

        def __iter__(self):
            '''
            iterating through the whole self.block
            giving the coords and the 0 or 1s
            so it's possible to do:
            for i, j, element in block:
            :-)
            '''
            for i in range(self.get_height()):
                for j in range(self.get_width()):
                    yield i, j, self.block[i][j]
            
#        def __repr__(self):
#            string = "\n".join(self.block)
#            return string

class Playscreen():
    '''
    giving a playscreen inhabiting
    some blocks, block-blocking,
    don't let them get out of bound'
    '''
    def __init__(
            self,
            width,
            height,
            block = None):
        self.playmatrix = zero_matrix(width, height)
        self.background_blocks = []
        self.active_block_pos = [0,0]
        if not block:
            block = Block()
        self.preview_block = block
        self.active_block = None
#        self.add_Block(block = block)
        
    def get_width(self):
        return len(self.playmatrix[0])
        
    def get_height(self):
        return len(self.playmatrix)

    def new_Block(self):
        #self.active_Block to background, then None
        self.add_Block()

    def add_Block(
            self,
            block = None,
            pos = None):
        # if already existing, no new active_block
        if self.active_block:
            return
        # else get the preview block
        self.active_block = self.preview_block
        # preview getting from above
        # if not given, creating a new one
        try:
            self.preview_block = block
        except AttributeError:
            self.preview_block = Block()
        if not pos:
            # if pos is not given,
            # take the top-middle
            pos =  [0, int((len(self.playmatrix[0])-self.active_block.get_width()+1)/2)]
        self.active_block_pos = pos
        x, y = self.active_block_pos
        free = True
        # self.active_block = block
        for i in range(self.active_block.get_width()):
            for j in range(self.active_block.get_height()):
                _x = x + i
                _y = y + j
                if self.playmatrix[_x][_y] and self.active_block[i][j]:
                    free = False
        if free:
# DEBUGGING
#          print_matrix(block.block)
#          inserting active_block into playscreen
          self.insert_active_block()
        else:
            pass
            #Exception and lose game

    def get_block_pos(self, block, abs = True):
        '''DOESN'T WORK yet'''
        x, y = self.active_block_pos
        for i in range(block.get_width()):
            for j in range(block.get_width()):
                _x = x + i
                _y = y + j
                yield [_x, _y]

          
    def insert_active_block(self):
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
        bw = ablock.get_width()#
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
            if self.active_block_pos[1] + self.active_block.get_width() >= self.get_width():
                raise BlockTooRightError
            #else: go right
            self.active_block_pos[1] += 1

    def turn(self):
        dummy = self.active_block
        absx, absy = self.active_block_pos
        dummy.turn()
        for j, row in dummy.block:#
            for i, el in row:
                if dummy[i][j] and self.playmatrix[absx+i][absy+j]:
                    raise BlockBlockedError("wanting to turn but some Block is in the way")
        self.active_block.turn()
            
    def move(self, direction):
            before = self.counting(self.playmatrix)
            # delete old block
            self.erase_active_block()
            # move block (old -> new)
            try:
                    if direction == MOVE_DOWN:
                        self.fall_down()
                    elif direction == MOVE_LEFT:
                        self.go_left()
                    elif direction == MOVE_RIGHT:
                        self.go_right()
                    elif direction == MOVE_TURN:
                        self.turn()
            except BlockTooRightError:
                self.active_block_pos[1] = self.get_width()-self.active_block.get_width()-1
            except BlockTooLeftError:
                self.active_block_pos[1] = 0
            except BlockTooLowError:
                pass
#                self.new_Block()
            # input new block
            self.insert_active_block()
            after = self.counting(self.playmatrix)
# DEBUGGING
#            print(f"{direction}: before: {before}, after: {after}")
#        if before != after: block blocked, reverse movement
            
    def print_me(self):
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
    tetris.add_Block(block1)
    print("printing")
    tetris.print_me()
    print("Fall twice")
    tetris.move(MOVE_DOWN)
    tetris.move(MOVE_DOWN)
    tetris.print_me()
    print("go right once")
    tetris.move(MOVE_RIGHT)
    tetris.print_me()
    print("go left twice")
    tetris.move(MOVE_LEFT)
    tetris.move(MOVE_LEFT)
    tetris.print_me()
    print("turn")
    tetris.move(MOVE_TURN)
    tetris.print_me()
    
