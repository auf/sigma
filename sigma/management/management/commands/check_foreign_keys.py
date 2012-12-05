# -*- encoding: utf-8 -*-
#
# Tout ceci est utilisé pour tester seulement. Il n'y a pas vraiment
# d'autres raisons d'utiliser ceci. N'utilisez rien de ceci sur une
# base de donnée comportant des données auxquelles vous tennez.
#

import sys
import random
import pprint
from django.core.management.base import BaseCommand
from django.db import models, DatabaseError
from auf.django.references.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import (
    RelatedField,
    ForeignKey,
    OneToOneField,
    )


all_models = models.get_models()


def warn():
    print('Warning! This will automatically delete a bunch of stuff '
          'from your database. Please ensure that you are using a '
          'test database, and that you know what you are doing! Enter '
          '"Yes" if you are sure that this is what you want to do!')
    confirm = raw_input()
    if confirm != 'Yes':
        sys.exit()
    

def print_count():
    for model in all_models:
        try:
            print "%s count: %s" % (str(model), model.objects.count())
        except:
            pass
    

def try_fix_data(model, items, field):
    # This will attempts to "fix" bad data by:
    # * Trying to set the bad foreign key to "Null",
    # * Else try to set it to a random related item
    # * Else delete it.
    for inst in items:
        try:
            inst = inst.__class__.objects.get(**{
                    inst._meta.pk.name: getattr(
                        inst, inst._meta.pk.name),
                    })
        except ObjectDoesNotExist:
            print "Deleting because cannot load."
            inst.delete()
            continue
        try:
            # Try to set to null
            setattr(inst, field.name, None)
            print "Set to null"
            inst.save()
        except ValueError:
            # Try to give random value.
            objcount = (
                field.rel.to.objects.count())
            if objcount and not isinstance(field, OneToOneField):
                rel_inst = (
                    field.rel.to.objects.all()[random.randint(
                            0,
                            objcount-1)])
                setattr(
                    inst, field.name, rel_inst)
                print "Set random related"
                try:
                    inst.save()
                except Exception, e:
                    print(
                        "Failed to save instance with random value: "
                        "%s inst id: %s" %
                        str(model.__class__),
                        getattr(inst, inst.__class__._meta.pk.name)
                        )
            else:
                # If all else fails..
                print "Deleting"
                inst.delete()
    


def find_missing(try_fix=False, print_out=False):
    if try_fix:
        warn()
    missing = {}
    for model in all_models:
        for field in model._meta.fields:
            if isinstance(field, (ForeignKey, OneToOneField)):
                try:
                    query = (
                        "SELECT a.%(pk)s, a.%(model_rel_column)s FROM "
                        "%(model_table_name)s  as a LEFT "
                        "OUTER JOIN %(rel_table_name)s as b ON "
                        "a.%(model_rel_column)s = b.%(rel_id_column)s "
                        "WHERE b.%(rel_id_column)s IS NULL and "
                        "a.%(model_rel_column)s IS NOT NULL;" 
                        % {
                            'pk': model._meta.pk.column,
                            'model_table_name': model._meta.db_table,
                            'rel_table_name': field.rel.to._meta.db_table,
                            'model_rel_column': field.column,
                            'rel_id_column': field.rel.field_name,
                            })
                    res2 = [x for x in model.objects.raw(query)]
                    if len(res2):
                        missing['%s: %s.%s' % (
                                model.__name__,
                                model._meta.db_table,
                                field.name)] = res2
                    if try_fix:
                        try_fix_data(model, res2, field)
                            
                except DatabaseError, e:
                    print "Failed to query: %s" % str(model.__class__)
                    print query
                    continue

            elif isinstance(field, RelatedField):
                # Not sure how to deal with other types of relations
                # yet.
                print field

    if print_out:
        pprint.pprint(missing)
    return missing


def use_alternative():
    find_missing(try_fix=True)


# def delete_missing():
#     warn()
#     missing = find_missing()

#     for key in missing.keys():
#         print "Deleting %s" % key
#         for inst in missing[key]:
#             pk_name = inst.__class__._meta.pk.name
#             try:
#                 inst.delete()
#             except:
#                 try:
#                     full_inst = inst.__class__.objects.get(**{
#                             pk_name: getattr(inst, pk_name)
#                             })
#                     full_inst.delete()
#                 except:
#                     print "Failed to delete: %s" % str(inst)


class Command(BaseCommand):
    args = 'model_count'
    help = """
./manage.py candidatures model_count: Prints the database count of all
    registered models.
./manage.py candidatures find_missing: Prints a report of all models
    with a missing foreign key.
"""

    def handle(self, *args, **options):
        """
        Dispatcher de commandes
        """
        method = args[0]

        if method == 'model_count':
            print_count()

        elif method == 'missing':
            find_missing(print_out=True)

        elif method == 'try_fix':
            find_missing(try_fix=True)
            
