# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand

from sigma.dynamo import dynamo_registry

class Command(BaseCommand):

    def handle(self, *args, **options):
        dynamo_registry.synchro_meta_2_instance()
