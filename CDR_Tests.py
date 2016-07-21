import unittest

class Call_Detail_Directory_Tests(unittest.TestCase):
    
    def getLoginFunctionReturnsString(self):
        actual = type(getLogin())
        expected = str
        
        self.assertEqual(true,all(isinstance(n,expected) for n in acutal))
        
