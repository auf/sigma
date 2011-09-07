# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from project.wcs import tools as cmd

class Command(BaseCommand):
    """

    Aide
    ====

    Appel
    -----
    * appel liste
    * appel clear
    * appel dossiers <appel_id>
    * appel dossier <appel_id> <dossier_id>
    * appel test <appel_id>

    """
    def handle(self, *args, **options):
        """
        Dispatcher de commandes
        """
        try:
            classname, method = args[0:2]
            classname = classname.title()
            instance = getattr(cmd, classname)()
            getattr(instance, method)(*args[2:])
        except:
            print self.__doc__
