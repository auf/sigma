# -*- encoding: utf-8 -*-

import datetime
from django.core.management.base import BaseCommand, CommandError
from project.wcs.tools import Appel
from project.wcs.models import Spool

class Command(BaseCommand):
    """
    Aide WCS
    ========
    * liste : liste tous les appels
    
    * clear : supprime le cache WCS
    
    * dossiers <appel_id> : liste tous les dossiers d'un appel
    
    * dossier <appel_id> <dossier_id> : affiche le dossier
    
    * test <appel_id> : test d'intégrité des données entre tous les dossiers
    
    * default_mapping : génère un squelette pour mapper les attributs des modèles
                        SIGMA une clef WCS
    
    * custom_mapping <appel_id> : génère un squelette pour faire un mapping custom
                                  à partir des clefs de WCS
    
    * importer <appel_id> dryrun|run : importe les dossiers
                                       (dryrun ne fait aucunes écritures)

    * cron : exécute ce qui est dans le spooler

    """

    def cron(self):
        for spool in Spool.objects.filter(requesting=True, date_requesting_debut=None):
            spool.date_requesting_debut = datetime.datetime.now()
            spool.save()
            spool.dryrun()
            
        for spool in Spool.objects.filter(processing=True, date_processing_debut=None):
            spool.date_processing_debut = datetime.datetime.now()
            spool.save()
            spool.run()
        
    def handle(self, *args, **options):
        """
        Dispatcher de commandes
        """
        method = args[0]

        if method == 'cron':
            self.cron()
            return

        if method == 'aide':
            print self.__doc__
            return

        appel = Appel()
        getattr(appel, method)(*args[1:])
