from auf.django.permissions import Role
from django.http import HttpResponseForbidden, HttpRequest


class BaseRole(Role):
    perms = []
    group_name = ''

    def __init__(self, regions):
        self.region = regions

    def has_perm(self, perm):
        return perm in self.perms


class SuperUser(BaseRole):
    def has_perm(self, perm):
        return True

    def get_filter_for_perm(self, perm, model):
        return True


class Gestionnaire(BaseRole):
    group_name = 'gestionnaires'
    perms = [
        'gestion_appels',
        'gestion_allocataire',
        'gestion_candidatures',
        'gestion_experts',
        ]


class Comptable(BaseRole):
    group_name = 'compatbles'
    perms = [
        'lecture_allocataire',
        ]
        

def group_role_provider(user):
    if user.is_superuser:
        return [SuperUser()]

    perms = []

    subclasses = BaseRole.__subclasses__()
    for cls in subclasses:
        for group in user.groups.all():
            if group.name == cls.group_name and cls.group_name != '':
                perms.append(cls(user.profile.regions.all()))

    return perms
    

def view_requires_perm(perm):
    def wrap(fun):
        def inner(*a, **kw):
            # This takes care of ModelAdmin "method" views.
            request = a[0] if isinstance(a[0], HttpRequest) else a[1]
            if request.user.has_perm(perm):
                return fun(*a, **kw)
            return HttpResponseForbidden('Permission denied')
        return inner
    return wrap


# from auf.django.permissions import Rules, Predicate
# from auf.django.permissions.predicates import has_global_perm
# from auf.django.references import models as ref
# from django.db.models import Q

# from sigma.candidatures.models import (
#     Appel,
#     Dossier,
#     Expert,
#     Candidat,
#     Diplome,
#     DossierOrigine,
#     DossierAccueil,
#     DossierMobilite,
#     Conformite,
#     )
# from sigma.boursiers.models import Allocation, Allocataire, FicheFinanciere


# def is_in_region(attr='pk'):
#     def p(user):
#         regions = [r.id for r in user.get_profile().regions.all()]
#         return Q(**{attr + '__in': regions})
#     return Predicate(p)


# rules = Rules()

# rules.allow('manage', ref.Region, is_in_region())
# rules.allow('change', Appel,
#             has_global_perm('global.gerer_appels') & is_in_region('region'))
# rules.allow('change', Expert,
#             has_global_perm('global.gerer_experts') & is_in_region('region'))
# rules.allow('assign', Expert, is_in_region('region'))


# # Dossier data:
# for dossier_model in ((Dossier, 'appel__region'),
#                       (Candidat, 'dossier__appel__region'),
#                       (Diplome, 'dossier__appel__region'),
#                       (DossierOrigine, 'dossier__appel__region'),
#                       (DossierAccueil, 'dossier__appel__region'),
#                       (DossierMobilite, 'dossier__appel__region'),
#                       (Conformite, 'dossier__appel__region')):
#     rules.allow('change', dossier_model[0],
#                 has_global_perm('global.gerer_dossiers') &
#                 is_in_region(dossier_model[1]))

# rules.allow('change', Allocataire,
#             has_global_perm('global.gerer_allocataires'))
# rules.allow('change', Allocation,
#             has_global_perm('global.gerer_allocations') &
#             is_in_region('dossier__appel__region'))
# rules.allow('change', FicheFinanciere,
#             has_global_perm('global.gerer_allocations') &
#             is_in_region('dossier__appel__region'))

# for perm in ['add', 'delete', 'change']:
#     for model in ['appel', 'dossier', 'expert']:
#         rules.allow_global(
#             'candidatures.%s_%s' % (perm, model),
#             has_global_perm('global.gerer_%ss' % model))
#     # Add perms for DossierAdmin inlines
#     for model in ['candidat', 'diplome', 'conformite',
#                   'dossierorigine', 'dossieraccueil', 'dossiermobilite']:
#         rules.allow_global(
#             'candidatures.%s_%s' % (perm, model),
#             has_global_perm('global.gerer_dossiers'))
#     for model in ['niveauetude', 'public', 'typeconformite', 'typepiece']:
#         rules.allow_global(
#             'candidatures.%s_%s' % (perm, model),
#             has_global_perm('global.configurer_sigma'))

#     rules.allow_global(
#         'boursiers.%s_allocation' % perm,
#         has_global_perm('global.gerer_allocations'))
#     # Add perms for BoursierAdmin inlines
#     for model in ['vueensemble',
#                   'depenseprevisionnelle',
#                   'allocataire',
#                   'allocation',
#                   'allocationorigine',
#                   'allocationaccueil',
#                   'allocationmobilite',
#                   'fichefinanciere',
#                   ]:
#         rules.allow_global(
#             'boursiers.%s_%s' % (perm, model),
#             has_global_perm('global.gerer_allocations'))
