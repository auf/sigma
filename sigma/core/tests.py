# encoding: utf-8

from auf.django.references import models as ref
from django.test import TestCase
from django.contrib.auth.models import User
from sigma.candidatures import models as candidatures


class AnonymousTestCase(TestCase):

    def test_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('this_is_the_login_form', response.content)


class SuperuserTestCase(TestCase):
    def setUp(self):
        region = ref.Region.objects.create(code='MO', nom='Moyen-Orient')
        appel = candidatures.Appel.objects.create(
            id=1,
            nom='Appel test',
            region=region,
            annee=2012,
        )
        dossier = candidatures.Dossier.objects.create(
            id=1,
            appel=appel
        )
        candidat = candidatures.Candidat(
            dossier=dossier,
            nom='Jiang',
            prenom='Qing',
            )
        User.objects.create_user('superman', password='superman')
        self.client.login(username='superman', password='superman')

    def test_admin_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_appel_changelist(self):
        response = self.client.get('/candidatures/appel/')
        self.assertEqual(response.status_code, 200)

    def test_appel_change(self):
        response = self.client.get('/candidatures/appel/1/')
        self.assertEqual(response.status_code, 200)

    def test_dossier_changelist(self):
        response = self.client.get('/candidatures/dossier/')
        self.assertEqual(response.status_code, 200)

    def test_dossier_change(self):
        response = self.client.get('/candidatures/dossier/1/')
        self.assertEqual(response.status_code, 200)
