from random import choice


# Blocks for tetris game
Z_BLOCK = [[1,1,0],[0,1,1]]
S_BLOCK = [[0,1,1],[1,1,0]]
BLOCKS = [Z_BLOCK, S_BLOCK]

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
                    yield (i, j, self.block[i][j])
            
#        def __repr__(self):
#            string = "\n".join(self.block)
#            return string




