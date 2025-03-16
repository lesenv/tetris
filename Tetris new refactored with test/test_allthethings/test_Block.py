import unittest
from Block import Block
import logic
from sre_constants import ANY

class Test_Blocks(unittest.TestCase):
    def setUp(self):
        # Blocks
        self.threex1 = Block([[3,3,3]])
        self.fourx3 = Block([[4,4,4,4],[4,4,4,4],[4,4,4,4]])
        self.onex3 = Block([[3],[3],[3]])

    def test_Block_getwidth(self):
        self.assertEqual(self.threex1.get_width(), 3)
        self.assertEqual(self.onex3.get_width(), 1)
        self.assertEqual(self.fourx3.get_width(), 4)
        
    def test_Block_getheight(self):
        self.assertEqual(self.threex1.get_height(), 1)
        self.assertEqual(self.onex3.get_height(), 3)
        self.assertEqual(self.fourx3.get_height(), 3)

    def test_Block_iterate(self):
        # normal matrix
        result = Block([[0,0,0,0],[1,2,3,4],[None, ANY, -1, "wer"]])
        for i, j, res in self.fourx3:
            result.block[i][j] = res
        self.assertEqual(result.block, self.fourx3.block, "iterating doesn't work")
        # matrix with width 1
        result = Block([[None], [ANY],[ "wer"]])
        for i, j, res in self.onex3:
            result.block[i][j] = res
        self.assertEqual(result.block, self.onex3.block, "iterating doesn't work")
        # matrix with height 1
        result = Block([[1, ANY,  "wer"]])
        for i, j, res in self.threex1:
            result.block[i][j] = res
        self.assertEqual(result.block, self.threex1.block, "iterating doesn't work")
        
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)
