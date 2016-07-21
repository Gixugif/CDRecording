import unittest

class Call_Detail_Directory_Tests(unittest.TestCase):
    
    def getLoginFunctionReturnsString(self):
        actual = type(getLogin())
        expected = "<class 'list'>"
        
        self.assertEqual(actual,expected)
        
        