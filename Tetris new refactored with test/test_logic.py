'''
tests the units in logic.py
importing logic imports Block automatically
'''
import unittest
import logic

S_BLOCK = [[1,1,0],
           [0,1,1]]
Z_BLOCK = [[0,1,1],
           [1,1,0]]

class Test_Moving_Tiles(unittest.TestCase):
    def setUp(self):
        # playscreens
        # create a playscreen, 4x4 playmatrix, first Block is the S_BLOCK
        self.playscreen4x4s = logic.Playscreen(4,4, block = logic.Block(S_BLOCK))
        # the other playscreen analogous  to the first one
        self.playscreen10x10z = logic.Playscreen(10, 10, block = logic.Block(Z_BLOCK))
        # one with non-squared playmatrix
        self.playscreen3x10z = logic.Playscreen(3, 10, block = logic.Block(Z_BLOCK))

    def test_setup(self):
        test_4x4s = [[0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,0,0]]
        self.assertEqual(self.playscreen4x4s.playmatrix,test_4x4s, "4x4s doesn't work")

        test_5x4z = [[0,0,1,0,0],
                     [0,1,1,0,0],
                     [0,1,0,0,0],
                     [0,0,0,0,0]]
        self.assertEqual(logic.Playscreen(5,4,block=logic.Block(Z_BLOCK)).playmatrix, test_5x4z,"5x4z didn't work")

        test_3x10z = [[0,1,0],
                      [1,1,0],
                      [1,0,0],
                      [0,0,0],
                      [0,0,0],
                      [0,0,0],
                      [0,0,0],
                      [0,0,0],
                      [0,0,0],
                      [0,0,0]]
        self.assertEqual(self.playscreen3x10z.playmatrix, test_3x10z, "3x10z doesn't work")
                                                                                          
    def test_turning_block(self):
        #
        # since we're testing logic.py, use MOVE_TURN!!
        # 

        test_4x4s_one_turn = [[0,0,1,1],
                              [0,1,1,0],
                              [0,0,0,0],
                              [0,0,0,0]]
        self.playscreen4x4s.move(logic.MOVE_TURN)
        self.assertEqual(self.playscreen4x4s.playmatrix, test_4x4s_one_turn, "one turn of 4x4s")
        # second turn, asserting turned back
        test_4x4s_two_turns = [[0,1,0,0],
                               [0,1,1,0],
                               [0,0,1,0],
                               [0,0,0,0]]
        self.playscreen4x4s.move(logic.MOVE_TURN)
        self.assertEqual(self.playscreen4x4s.playmatrix, test_4x4s_two_turns, "two turns of 4x4s")
        

        test_3x10z_one_turn = [[1,1,0],
                               [0,1,1],
                               [0,0,0],
                               [0,0,0],
                               [0,0,0],
                               [0,0,0],
                               [0,0,0],
                               [0,0,0],
                               [0,0,0],
                               [0,0,0]]
        self.playscreen3x10z.move(logic.MOVE_TURN)
        self.assertEqual(self.playscreen3x10z.playmatrix, test_3x10z_one_turn, "one turn of 3x10z")
        
        test_3x10z_two_turns = [[0,1,0],
                                [1,1,0],
                                [1,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0]]
        self.playscreen3x10z.move(logic.MOVE_TURN)
        self.assertEqual(self.playscreen3x10z.playmatrix, test_3x10z_two_turns, "second turn of 3x10z")

        self.playscreen3x10z.move(logic.MOVE_RIGHT)
        self.playscreen3x10z.move(logic.MOVE_TURN)
        test_3x10z_right_turn = [[0,0,1],
                                 [0,1,1],
                                 [0,1,0],
                                 [0,0,0],
                                 [0,0,0],
                                 [0,0,0],
                                 [0,0,0],
                                 [0,0,0],
                                 [0,0,0],
                                 [0,0,0]]
        self.assertEqual(self.playscreen3x10z.playmatrix, test_3x10z_right_turn, "turn of 3x10z moved to the right")


    def test_zero_matrix(self):
        self.assertEqual(logic.zero_matrix(2,2), [[0,0],[0,0]], "2-2 0-matrix didn't work")
        self.assertEqual(logic.zero_matrix(3,4), [[0,0,0],[0,0,0],[0,0,0],[0,0,0]], "3-4 0_matrix didn't work")
        
    def test_fall_block(self):
        #fallen_playscreen = fp
        fp = [[0,0,0,0],
              [0,1,0,0],
              [0,1,1,0],
              [0,0,1,0]]
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        self.assertEqual(self.playscreen4x4s.playmatrix, fp , "4x4s fell not okay")

        fp = [[0,0,0],
              [0,1,0],
              [1,1,0],
              [1,0,0],
              [0,0,0],
              [0,0,0],
              [0,0,0],
              [0,0,0],
              [0,0,0],
              [0,0,0]]
        self.playscreen3x10z.move(logic.MOVE_DOWN)
        self.assertEqual(self.playscreen3x10z.playmatrix, fp, "3x10z didn't fall alright") #sometimes, but most times it kicks you in the teeth

    def test_falling_block_collided_with_existing_block(self):
        # think of what is happening
        for _ in range(3):
            self.playscreen10x10z.move(logic.MOVE_DOWN)
        self.playscreen10x10z._new_Block()
        self.playscreen10x10z.move(logic.MOVE_DOWN)
        self.playscreen10x10z.move(logic.MOVE_DOWN)
        
    def test_fall_stopping_at_the_bottom(self):
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        bottom_screen = self.playscreen4x4s.playmatrix
        self.playscreen4x4s.move(logic.MOVE_DOWN)
        self.assertEqual(self.playscreen4x4s.playmatrix, bottom_screen, "4x4s: Block moved, although Block is at the bottom")

        for _ in range(10):
            self.playscreen3x10z.move(logic.MOVE_DOWN)
        bottom_screen = self.playscreen3x10z.playmatrix
        self.playscreen3x10z.move(logic.MOVE_DOWN)
        self.assertEqual(self.playscreen3x10z.playmatrix, bottom_screen, "3x10z: Block moved, although Block is at the bottom")

    def test_block_move_right(self):
        test = logic.zero_matrix(10,10)
        test[0][6] = 1
        test[1][5], test[1][6] = 1, 1
        test[2][5] = 1
        self.playscreen10x10z.move(logic.MOVE_RIGHT)
        self.assertEqual(self.playscreen10x10z.playmatrix, test, "didn't move right accordingly first time")
        test = logic.zero_matrix(10,10)
        test[0][7] = 1
        test[1][6], test[1][7] = 1,1
        test[2][6] = 1
        self.playscreen10x10z.move(logic.MOVE_RIGHT)
        self.assertEqual(self.playscreen10x10z.playmatrix, test, "didn't move right accordingly second time")

        
        test = logic.zero_matrix(3,10)
        test[0][2] = 1
        test[1][1], test[1][2] = 1,1
        test[2][1] = 1
        self.playscreen3x10z.move(logic.MOVE_RIGHT)
        self.assertEqual(self.playscreen3x10z.playmatrix, test, "didn't move right accordingly second time")

    def test_block_too_right_at_the_right_side(self):
        for _ in range(13):
            self.playscreen10x10z.move(logic.MOVE_RIGHT)
        right_screen = self.playscreen10x10z.playmatrix
        self.playscreen10x10z.move(logic.MOVE_RIGHT)
        self.assertEqual(self.playscreen10x10z.playmatrix, right_screen, "Block moved, although Block is at the right border")
        for _ in range(3):
            self.playscreen3x10z.move(logic.MOVE_RIGHT)
        right_screen = self.playscreen3x10z.playmatrix
        self.playscreen3x10z.move(logic.MOVE_RIGHT)
        self.assertEqual(self.playscreen3x10z.playmatrix, right_screen, "didn't move right accordingly second time")
        
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)
