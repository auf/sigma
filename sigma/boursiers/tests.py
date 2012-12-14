# -*- encoding: utf-8 -*-

from django.test import TestCase
from sigma.candidatures.models import Dossier


class TestVueEnsemble(TestCase):
    fixtures = ['ref_test_data.json', 'test_candidatures.json']

    def make_vues(self):
        dos = Dossier.objects.get(id=3)
        dos.etat = 'RECEVABLE'
        dos.save()
        dos.etat = 'RETENU'
        dos.save()
        return dos

    def test_vue_ensemble_creation(self):
        dos = self.make_vues()
        self.assertEquals(dos.boursier.vue_ensemble.all().count(), 4)

    def test_vue_ensemble_montant(self):
        pass
        # dos = self.make_vues()
        # Montant prevu:
        # Candidat Carole est du Sud
        #
        # exp_montant = 90 * 7 + 100 * 7
        # tot = dos.boursier.vue_ensemble.get(vue_type='EA')
        # self.assertEquals(tot.calc_montant(), exp_montant)
