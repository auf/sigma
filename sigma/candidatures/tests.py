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

        # 2 mois, novembre compte, decembre aussi.
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 12, 20),
            )
        self.assertEquals(p.mois, 2)
        self.assertEquals(p.jours, 31)

        # 1 mois, novembre ne compte pas, decembre oui.
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 21),
            datetime.date(2012, 12, 20),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 30)

        # Edge cases.
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 11),
            datetime.date(2012, 11, 20),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 10)

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 11, 20),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 1)

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 18),
            datetime.date(2012, 11, 19),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 2)

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 19),
            datetime.date(2012, 11, 20),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 2)

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 11, 21),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 2)

        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2012, 11, 21),
            )
        self.assertEquals(p.mois, 1)
        self.assertEquals(p.jours, 2)

        # Long periods
        p = DossierMobilite.Periode(
            datetime.date(2012, 11, 20),
            datetime.date(2013, 11, 21),
            )
        self.assertEquals(p.mois, 13)
        self.assertEquals(p.jours, 367)

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
