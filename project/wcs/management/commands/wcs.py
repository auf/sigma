# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from project.wcs import tools as cmd

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Dispatcher de commandes
        """
        classname, method = args[0:2]
        classname = classname.title()
        instance = getattr(cmd, classname)()
        getattr(instance, method)(*args[2:])
