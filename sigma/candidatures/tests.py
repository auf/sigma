from django.test import TestCase
from .models import Candidat


class CandidatTestCase(TestCase):
    fixtures = ['test_data_all_models.json']

    def test_age(self):
        candidat = Candidat.objects.get(id=648)
        self.assertEquals(type(candidat.age()), int)
        candidat.naissance_date = None
        self.assertEquals(type(candidat.age()), type(None))
