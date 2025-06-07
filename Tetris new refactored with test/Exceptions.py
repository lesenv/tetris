'''
Exceptions used in logic.py
'''
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
    when trying to move or to create
    a Block interfering with an already
    existing Block
    '''
