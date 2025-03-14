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

z_block = [[1,1,0],[0,1,1]]
s_block = [[0,1,1],[1,1,0]]
blocks = [z_block, s_block]

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
                block = choice(blocks)
            self.block = block
                
        def get_width(self):
            if type(self.block[0]) == type(1):
                # horizontal stick
                return len(self.block)
            return len(self.block[0])
            
        def get_height(self):
            if type(self.block[0]) == type(1):
                # horizontal stick
                return 1
            return len(self.block)

        def turn(self):
            if type(self.block[0]) == type(1):
                # horizontal stick
                self.block = [[e] for e in self.block]
            elif len(self.block[0]) == 1:
                self.block = [r for [r] in  self.block]
            else:
                rotated = list(zip(*self.block[::-1]))
                self.block = list(list(x) for x in rotated)
            return 
            
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
        self.playscreen = zero_matrix(width, height)
        self.blocks = []
        if not block:
            block = Block()
        self.preview_block = block
        self.active_block = None
        self.active_block_pos = [0,0]
        if not block:
            block = Block()
        self.add_Block(block = block)
        
    def get_width(self):
        return len(self.playscreen[0])
        
    def get_height(self):
        return len(self.playscreen)

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
        # if not existing, creating a new one
        try:
            self.preview_block = block
        except AttributeError:
            self.preview_block = Block()
        if not pos:
                pos =  [0, int((len(self.playscreen[0])-block.get_width()+1)/2)]
        self.active_block_pos = pos
        x, y = self.active_block_pos
        free = True
        # self.active_block = block
        for i in range(block.get_width()):
            for j in range(block.get_height()):
                _x = x + i
                _y = y + j
                if self.playscreen[_x][_y] and block[i][j]:
                    free = False
        if free:
# DEBUGGING
#          print_matrix(block.block)
#          inserting active_block into playscreen
          self.insert_active_block()
        else:
            pass
            #Exception and lose game
          
    def insert_active_block(self):
          block = self.active_block
          x, y = self.active_block_pos
          for i in range(block.get_width()):
            for j in range(block.get_height()):
                _x = x + i
                _y = y + j
                self.playscreen[_x][_y] = block.block[j][i]
                
    def erase_active_block(self):
          block = self.active_block
          x, y = self.active_block_pos
# DEBUGGING
#          print(f"erase block {block} at {x, y}")
          for i in range(block.get_width()):
            for j in range(block.get_height()):
#                print(i,j)
                _x = x + i
                _y = y + j
                self.playscreen[_x][_y] = 0
                
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
            
    def move(self, direction):
            before = self.counting(self.playscreen)
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
            except BlockTooRightError:
                self.active_block_pos[1] = self.get_width()-self.active_block.get_width()-1
            except BlockTooLeftError:
                self.active_block_pos[1] = 0
            except BlockTooLowError:
                self.new_Block()
            # input new block
            self.insert_active_block()
            after = self.counting(self.playscreen)
# DEBUGGING
#            print(f"{direction}: before: {before}, after: {after}")
#        if before != after: block blocked, reverse movement
            
    def print_me(self):
            print_matrix(self.playscreen)
        

if __name__ == "__main__":
    print("LOS")
    tetris = Playscreen(6,17)
    tetris.print_me()
    print("creating a block")
    block1 = Block()
    print("adding a block")
    tetris.add_Block(block1)
    print("printing")
    tetris.print_me()
    print("Fall twice")
    tetris.fall_down()
    tetris.fall_down()
    tetris.print_me()
    print("go right once")
    tetris.go_right()
    tetris.print_me()
    print("go left twice")
    tetris.go_left()
    tetris.go_left()
    tetris.print_me()
    
