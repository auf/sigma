# -=- encoding: utf-8 -=-

from sigma.www.testcases.sigmatestcase import SigmaTestCase

from sigma.www.utils import calculateAge

import datetime

class TestDates(SigmaTestCase):
      """Test des fonctions de date des utilitaires"""

      def test_age_in_years(self):
            """Test du calcul de l'age en annees"""
            self.assertEqual(calculateAge(datetime.date(1981, 12, 23), 
                                          datetime.date(2009, 8, 21)),
                                          27)
            self.assertEqual(calculateAge(datetime.date(1980, 2, 29), 
                                          datetime.date(2009, 8, 21)),
                                          29)
            self.assertEqual(calculateAge(datetime.date(1980, 2, 29), 
                                          datetime.date(2000, 8, 29)),
                                          20)
            self.assertEqual(calculateAge(datetime.date(1980, 12, 31), 
                                          datetime.date(2009, 12, 31)),
                                          29)

      def test_in_months(self):
            """Test du calcul de l'age en mois"""
            self.assertEqual(calculateAge(datetime.date(2009, 10, 23), 
                                          datetime.date(2009, 12, 23),
                                          months=True),
                                          2)
            self.assertEqual(calculateAge(datetime.date(2009, 10, 21), 
                                          datetime.date(2009, 12, 23),
                                          months=True),
                                          2)
            self.assertEqual(calculateAge(datetime.date(2008, 10, 21), 
                                          datetime.date(2009, 12, 23),
                                          months=True),
                                          14)
            self.assertEqual(calculateAge(datetime.date(2009, 06, 26), 
                                          datetime.date(2010, 03, 26),
                                          months=True),
                                          9)
