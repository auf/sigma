# -*- encoding: utf-8 -*-

import datetime
import mock
from django.test import TestCase
from datetime import date


class FakeDate(date):
    # Utilisé par mock dans les test.
    def __new__(cls, *args, **kwargs):
        return date.__new__(date, *args, **kwargs)


class CandidatTestCase(TestCase):
    fixtures = ['ref_test_data.json', 'test_candidatures.json']

    @mock.patch('datetime.date', FakeDate)
    def test_age(self):
        from datetime import date
        FakeDate.today = classmethod(
            lambda cls: date(2007, 12, 1)
            )
        from .models import Candidat

        candidat = Candidat.objects.get(id=1)
        self.assertEquals(
            candidat.naissance_date,
            datetime.date(1983, 5, 6)
            )
        self.assertEquals(
            candidat.age(),
            24,
            )

    # def test_period_iter(self):
    #     from .models import DossierMobilite

    #     p = DossierMobilite.Periode(
    #         datetime.date(2012, 11, 20),
    #         datetime.date(2013, 12, 19),
    #         )
    #     # self.assertEquals(p.mois, 13)
    #     # self.assertEquals(p.jours, 395)

    #     months = [x for x in p]
    #     self.assertEquals(
    #         months[0],
    #         datetime.date(year=2012, month=12, day=1))
    #     self.assertEquals(
    #         months[-1:][0],
    #         datetime.date(year=2013, month=12, day=1))
    #     self.assertEquals(len(months), 13)

    def test_periode(self):
        # Specs:
        # on arrondit au 20e jour.
        #
        # if date_debut <= 20e jour du mois :
        # compter le mois du début # ex.: debut = 2012-11-14 : mois
        # debut = novembre
        #
        # if date_fin >= 20e jour du mois :
        # compter le mois de fin # fin = 2012-12-14 : mois fin =
        # novembre

        # 1 mois, novembre compte, decembre non.

        from .models import DossierMobilite

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 12, 19),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 30)
        self.assertEquals(
            [x for x in p.month_iterator],
            [datetime.date(2012, 11, 1)],
            )
        self.assertEquals(
            [x for x in p.days_iterator],
            [datetime.date(2012, 11, 20),
             datetime.date(2012, 11, 21),
             datetime.date(2012, 11, 22),
             datetime.date(2012, 11, 23),
             datetime.date(2012, 11, 24),
             datetime.date(2012, 11, 25),
             datetime.date(2012, 11, 26),
             datetime.date(2012, 11, 27),
             datetime.date(2012, 11, 28),
             datetime.date(2012, 11, 29),
             datetime.date(2012, 11, 30),
             datetime.date(2012, 12, 1),
             datetime.date(2012, 12, 2),
             datetime.date(2012, 12, 3),
             datetime.date(2012, 12, 4),
             datetime.date(2012, 12, 5),
             datetime.date(2012, 12, 6),
             datetime.date(2012, 12, 7),
             datetime.date(2012, 12, 8),
             datetime.date(2012, 12, 9),
             datetime.date(2012, 12, 10),
             datetime.date(2012, 12, 11),
             datetime.date(2012, 12, 12),
             datetime.date(2012, 12, 13),
             datetime.date(2012, 12, 14),
             datetime.date(2012, 12, 15),
             datetime.date(2012, 12, 16),
             datetime.date(2012, 12, 17),
             datetime.date(2012, 12, 18),
             datetime.date(2012, 12, 19),
             ],
            )

        # 2 mois, novembre compte, decembre aussi.
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 12, 20),
            )
        self.assertEquals(p.mois, 2)
        self.assertEquals(p.jours, 31)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 11, 1),
             datetime.date(2012, 12, 1)],
            )

        # self.assertEquals(
        #     [x for x in p],
        #     [datetime.date(2012, 12, 1)],
        #     )

        # 1 mois, novembre ne compte pas, decembre oui.
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 21),
            datetime.date(2012, 12, 20),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 30)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 12, 1)],
            )

        # Edge cases.
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 11),
            datetime.date(2012, 11, 20),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 10)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 11, 1)],
            )

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 11, 20),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 1)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 11, 1)],
            )

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 18),
            datetime.date(2012, 11, 19),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 2)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 11, 1)],
            )

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 19),
            datetime.date(2012, 11, 20),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 2)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 11, 1)],
            )

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 11, 21),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 2)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 11, 1)],
            )

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 11, 21),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 2)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 11, 1)],
            )

        # Long periods
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2013, 11, 21),
            )
        self.assertEquals(p.mois, 13)
        self.assertEquals(p.jours, 367)
        self.assertEquals(
            [x for x in p],
            [datetime.date(2012, 11, 1),
             datetime.date(2012, 12, 1),
             datetime.date(2013, 1, 1),
             datetime.date(2013, 2, 1),
             datetime.date(2013, 3, 1),
             datetime.date(2013, 4, 1),
             datetime.date(2013, 5, 1),
             datetime.date(2013, 6, 1),
             datetime.date(2013, 7, 1),
             datetime.date(2013, 8, 1),
             datetime.date(2013, 9, 1),
             datetime.date(2013, 10, 1),
             datetime.date(2013, 11, 1),
             ],
            )

        # Long periods
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2113, 11, 21),
            )
        self.assertEquals(p.mois, 13 + 100 * 12)

        # Combination pour obtenir duree totale:
        p1 = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 11, 21),
            )

        p2 = DossierMobilite.Periode(
            datetime.date(2012, 12, 20),
            datetime.date(2012, 12, 21),
            )

        p_totale = p1 + p2
        self.assertEquals(p_totale.mois, 2)
        self.assertEquals(p_totale.jours, 4)

        # Pas d'origine:
        p1 = DossierMobilite.Periode(
            None,
            None,
            )

        p2 = DossierMobilite.Periode(
            datetime.date(2012, 12, 20),
            datetime.date(2012, 12, 21),
            )

        p_totale = p1 + p2
        self.assertEquals(p_totale.mois, 1)
        self.assertEquals(p_totale.jours, 2)

        # Pas d'accueil
        p1 = DossierMobilite.Periode(
            datetime.date(2012, 12, 20),
            datetime.date(2012, 12, 21),
            )

        p2 = DossierMobilite.Periode(
            None,
            None,
            )

        p_totale = p1 + p2
        self.assertEquals(p_totale.mois, 1)
        self.assertEquals(p_totale.jours, 2)

        # Aucun:
        p1 = DossierMobilite.Periode(
            None,
            None,
            )

        p2 = DossierMobilite.Periode(
            None,
            None,
            )

        p_totale = p1 + p2
        self.assertEquals(p_totale.mois, 0)
        self.assertEquals(p_totale.jours, 0)

        # Bad data:
        p1 = DossierMobilite.Periode(
            None,
            datetime.date(2012, 12, 21),
            )

        p2 = DossierMobilite.Periode(
            datetime.date(2012, 12, 21),
            None,
            )

        p_totale = p1 + p2
        self.assertEquals(p_totale.mois, 0)
        self.assertEquals(p_totale.jours, 0)

    def test_duree_mobilite(self):
        from .models import Dossier

        d1 = Dossier.objects.get(id=1)
        d2 = Dossier.objects.get(id=2)

        self.assertEquals(
            d1.mobilite.duree_origine.jours,
            214,
            )
        self.assertEquals(
            d1.mobilite.duree_origine.mois,
            7,
            )
        self.assertEquals(
            d1.mobilite.duree_accueil.jours,
            212,
            )
        self.assertEquals(
            d1.mobilite.duree_accueil.mois,
            7,
            )
        self.assertEquals(
            d1.mobilite.duree_totale.jours,
            426,
            )
        self.assertEquals(
            d1.mobilite.duree_totale.mois,
            14,
            )

        self.assertEquals(
            d2.mobilite.duree_origine.jours,
            0,
            )
        self.assertEquals(
            d2.mobilite.duree_origine.mois,
            0,
            )
        self.assertEquals(
            d2.mobilite.duree_accueil.jours,
            212,
            )
        self.assertEquals(
            d2.mobilite.duree_accueil.mois,
            7,
            )
        self.assertEquals(
            d2.mobilite.duree_totale.jours,
            212,
            )
        self.assertEquals(
            d2.mobilite.duree_totale.mois,
            7,
            )
