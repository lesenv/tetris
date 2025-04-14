import unittest
from Block import Block

class Test_Blocks(unittest.TestCase):
    def setUp(self):
        # Blocks
        self.threex1 = Block([[3,3,3]])
        self.fourx3 = Block([[4,4,4,4],[4,4,4,4],[4,4,4,4]])
        self.onex3 = Block([[3],[3],[3]])
        self.ascend = Block([[0,1,2],[3,4,5]])
        # TetrisBlocks
        self.Z_BLOCK = Block(
                             [[1,1,0],
                              [0,1,1]]
                             )
        self.S_BLOCK = Block(
                             [[0,1,1],
                              [1,1,0]]
                             )
        self.tower_block = Block(
                                 [[1,1,1,1]]
                                 )

    def test_Block_getwidth(self):
        self.assertEqual(self.threex1.get_width(), 3)
        self.assertEqual(self.onex3.get_width(), 1)
        self.assertEqual(self.fourx3.get_width(), 4)
        
    def test_Block_getheight(self):
        self.assertEqual(self.threex1.get_height(), 1)
        self.assertEqual(self.onex3.get_height(), 3)
        self.assertEqual(self.fourx3.get_height(), 3)

    def test_Block_iterate(self):
        '''
        Test if the iterator is working indeed
        by copying known matrices to others
        '''
        # normal matrix
        result = Block([[0,0,0,0],[1,2,3,4],[None, [34, 234,4564], -1, "wer"]])
        for i, j, res in self.fourx3:
            result.block[i][j] = res
        self.assertEqual(result.block, self.fourx3.block, "iterating doesn't work")
        # matrix with width 1
        result = Block([[None], [[34, 234,4564]],[ "wer"]])
        for i, j, res in self.onex3:
            result.block[i][j] = res
        self.assertEqual(result.block, self.onex3.block, "iterating doesn't work")
        # matrix with height 1
        result = Block([[1, [34, 234,4564],  "wer"]])
        for i, j, res in self.threex1:
            result.block[i][j] = res
        self.assertEqual(result.block, self.threex1.block, "iterating doesn't work")
        # ascending without using Matrix in Loop
        twobythree = Block([[0,1,1],[3,4,1]])
        for l, [i, j, _] in enumerate(twobythree):
            lplus = l//twobythree.get_width()*twobythree.get_height()
            twobythree.block[i][j] = i+j+lplus
        self.assertEqual(twobythree.block, self.ascend.block, "ascending doesn't work")
                                                                                          
    def test_turning_block(self):
        self.Z_BLOCK.turn()
        self.assertEqual(self.Z_BLOCK.block, [[0,1], [1,1], [1,0]], "turning Z not working")
        self.Z_BLOCK.turn()
        self.assertEqual(self.Z_BLOCK.block, [[1,1,0], [0,1,1]], "2nd turning Z not working")
        self.tower_block.turn()
        self.assertEqual(self.tower_block.block, [[1],[1], [1],[1]], "turning tower not working")
        self.tower_block.turn()
        self.assertEqual(self.tower_block.block, [[1,1, 1,1]], "2nd turning tower not working")
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)
