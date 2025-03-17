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
        self.playscreen4x4s.new_Block()
        self.playscreen10x10z = logic.Playscreen(10, 10, block = self.Z_BLOCK)
                                                                                          
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
# DEBUGGING
##        logic.print_matrix(self.playscreen4x4s.playscreen)
##        print("ˆ<- logic  dsp->V")
##        logic.print_matrix(dsp)
        self.assertEqual(self.playscreen4x4s.playmatrix, dsp, "playscreen didn't equal to 4x4-0-matrix")
        
    def test_fall_block(self):
        #fallen_playscreen = fp
        fp = logic.zero_matrix(4, 4)
        fp[1][2] = 1
        fp[2][2], fp[2][1] = 1, 1
        fp[3][1] = 1
        self.playscreen4x4s.move(logic.MOVE_DOWN)
# DEBUGGING
##        logic.print_matrix(self.playscreen4x4s.playscreen)
##        print("ˆ<- logic  dsp->V")
##        logic.print_matrix(fp)
        self.assertEqual(self.playscreen4x4s.playmatrix, fp , "fell not okay")
        
    def test_fall_stopping_at_the_bottom(self):
# DEBUGGING
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        bottom_screen = self.playscreen4x4s.playmatrix
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        self.assertEqual(self.playscreen4x4s.playmatrix, bottom_screen, "Block moved, obwohl Block is at the bottom")
        
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)
    
