import unittest
import logic #logic imports Block automatically

class Test_Moving_Tiles(unittest.TestCase):
    def setUp(self):
        # TetrisBlocks
        self.Z_BLOCK = logic.Block(
                                 [[1,1,0],
                                  [0,1,1]]
                                  )
        self.S_BLOCK = logic.Block(
                                 [[0,1,1],
                                  [1,1,0]]
                                  )
        self.tower_block = logic.Block(
                                 [[1,1,1,1]]
                                 )
        # playscreens
        self.playscreen4x4s = logic.Playscreen(4,4, block = self.S_BLOCK)
        self.playscreen4x4s.new_Block(self.S_BLOCK)
        self.playscreen10x10z = logic.Playscreen(10, 10, block = self.Z_BLOCK)
        self.playscreen10x10z.new_Block(self.Z_BLOCK)
                                                                                          
    def test_turning_block(self):
        self.Z_BLOCK.turn()
        self.assertEqual(self.Z_BLOCK.block, [[0,1], [1,1], [1,0]], "turning Z not working")
        self.Z_BLOCK.turn()
        self.assertEqual(self.Z_BLOCK.block, [[1,1,0], [0,1,1]], "2nd turning Z not working")
        self.tower_block.turn()
        self.assertEqual(self.tower_block.block, [[1],[1], [1],[1]], "turning tower not working")
        self.tower_block.turn()
        self.assertEqual(self.tower_block.block, [[1,1, 1,1]], "2nd turning tower not working")

    def test_zero_matrix(self):
        self.assertEqual(logic.zero_matrix(2,2), [[0,0],[0,0]], "2-2 0-matrix didn't work")
        self.assertEqual(logic.zero_matrix(3,4), [[0,0,0],[0,0,0],[0,0,0],[0,0,0]], "3-4 0_matrix didn't work")
        
    def test_default_block(self):
        #default_start_playscreen = dsp
        dsp = logic.zero_matrix(4, 4)
        dsp[0][2] = 1
        dsp[1][2], dsp[1][1] = 1, 1
        dsp[2][1] = 1
        self.assertEqual(self.playscreen4x4s.playmatrix, dsp, "playscreen didn't equal to 4x4-0-matrix")
        
    def test_fall_block(self):
        #fallen_playscreen = fp
        fp = logic.zero_matrix(4, 4)
        fp[1][2] = 1
        fp[2][2], fp[2][1] = 1, 1
        fp[3][1] = 1
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        self.assertEqual(self.playscreen4x4s.playmatrix, fp , "fell not okay")

    def test_falling_block_collided_with_existing_block(self):
        for _ in range(3):
            self.playscreen10x10z.move(logic.MOVE_DOWN)
        self.playscreen10x10z.new_Block()
        self.playscreen10x10z.move(logic.MOVE_DOWN)
        self.playscreen10x10z.move(logic.MOVE_DOWN)
        
    def test_fall_stopping_at_the_bottom(self):
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        bottom_screen = self.playscreen4x4s.playmatrix
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        self.assertEqual(self.playscreen4x4s.playmatrix, bottom_screen, "Block moved, although Block is at the bottom")

    def test_block_move_right(self):
        test = logic.zero_matrix(10,10)
        test[0][4] = 1
        test[1][4], test[1][5] = 1, 1
        test[2][5] = 1
        self.playscreen10x10z.move(logic.MOVE_RIGHT)
        self.assertEqual(self.playscreen10x10z.playmatrix, test, "didn't move right accordingly first time")
        test = logic.zero_matrix(10,10)
        test[0][6] = 1
        test[1][6], test[1][7] = 1,1
        test[2][7] = 1
        self.playscreen10x10z.move(logic.MOVE_RIGHT)
        self.assertEqual(self.playscreen10x10z.playmatrix, test, "didn't move right accordingly second time")

    def test_block_too_right_at_the_right_side(self):
        #for _ in range(3):
        #    self.playscreen10x10z.move(logic.MOVE_RIGHT)
        right_screen = self.playscreen10x10z.playmatrix
        self.playscreen10x10z.move(logic.MOVE_RIGHT)
        self.assertEqual(self.playscreen10x10z.playmatrix, right_screen, "Block moved, although Block is at the right border")
        
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)
    
