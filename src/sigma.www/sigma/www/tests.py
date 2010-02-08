import unittest

from sigma.www.testcases.sigmatestcase import SigmaTestCase

import sigma.www.testcases

class TestBidon(unittest.TestCase):
    """ Classe de test qui lance tous les tests cases qui se trouvent
    dans le dossier de tests
    """
    def test_launch(self):
        """Lancement des tests"""
        for str_test in sigma.www.testcases.__all__:
            test = getattr(sigma.www.testcases, str_test)
            for e in dir(test):
                attr_e = getattr(test, e)
                try:
                    if issubclass(attr_e, SigmaTestCase):
                        if attr_e != SigmaTestCase:
                            suite = unittest.TestLoader().loadTestsFromTestCase(attr_e)
                            unittest.TextTestRunner(verbosity=2).run(suite)
                except TypeError:
                    pass
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBidon)
    unittest.TextTestRunner(verbosity=2).run(suite)
        
