# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from sigma_v1 import models as models_v1

class Command(BaseCommand):
    args = '<action>'
    help = '?'

    def handle(self, *args, **options):
        self.stdout.write('\nModèles V1 accessible à travers la passerelle\n')
        print models_v1.Personne.__class__
        self.stdout.write('\nSIGMA import des données de SIGMA1.0 ver SIGMA2.0\n')



