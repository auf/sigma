# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from project.wcs.tools import Appel

class Command(BaseCommand):
    """

    Aide
    ====

    * liste
    * clear
    * dossiers <appel_id>
    * dossier <appel_id> <dossier_id>
    * test <appel_id>

    """
    def handle(self, *args, **options):
        """
        Dispatcher de commandes
        """
        method = args[0]
        appel = Appel()
        getattr(appel, method)(*args[1:])
