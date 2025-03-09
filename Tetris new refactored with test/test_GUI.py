import unittest
import logic

class Little_Block(unittest.TestCase):
    def test_little_block_default_dimension(self):
        '''test default size'''
        self.assertEqual(logic.little_block().size, (20,20), "wrong default size")
        
    def test_little_block_other_dimesion(self):
        self.assertEqual(logig.little_block(20).size, (30,30), "wrong explicit size")
    
#def suite():
#    suite = unittest.TestSuite()
#    suite.addTest(WidgetTestCase('test_default_widget_size'))
#    suite.addTest(WidgetTestCase('test_widget_resize'))
#    return suite

if __name__ == '__main__':
#    runner = unittest.TextTestRunner()
#    runner.run(suite())
    unittest.main()