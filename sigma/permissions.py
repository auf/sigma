from auf.django.permissions import Rules, Predicate
from auf.django.permissions.predicates import has_global_perm
from auf.django.references import models as ref
from django.db.models import Q

from sigma.candidatures.models import Appel, Dossier, Expert
from sigma.boursiers.models import Boursier


def is_in_region(attr='pk'):
    def p(user):
        regions = [r.id for r in user.get_profile().regions.all()]
        return Q(**{attr + '__in': regions})
    return Predicate(p)


rules = Rules()

rules.allow('manage', ref.Region, is_in_region())
rules.allow('change', Appel,
            has_global_perm('global.gerer_appels') & is_in_region('region'))
rules.allow('change', Expert,
            has_global_perm('global.gerer_experts') & is_in_region('region'))
rules.allow('assign', Expert, is_in_region('region'))
rules.allow('change', Dossier,
            has_global_perm('global.gerer_dossiers') &
            is_in_region('appel__region'))
rules.allow('change', Boursier,
            has_global_perm('global.gerer_boursiers') &
            is_in_region('dossier__appel__region'))

for perm in ['add', 'delete', 'change']:
    for model in ['appel', 'dossier', 'expert']:
        rules.allow_global(
            'candidatures.%s_%s' % (perm, model),
            has_global_perm('global.gerer_%ss' % model))
    # Add perms for DossierAdmin inlines
    for model in ['candidat', 'diplome', 'conformite',
                  'dossierorigine', 'dossieraccueil', 'dossiermobilite']:
        rules.allow_global(
            'candidatures.%s_%s' % (perm, model),
            has_global_perm('global.gerer_dossiers'))
    for model in ['niveauetude', 'public', 'typeconformite', 'typepiece']:
        rules.allow_global(
            'candidatures.%s_%s' % (perm, model),
            has_global_perm('global.configurer_sigma'))

    rules.allow_global(
        'boursiers.%s_boursier' % perm,
        has_global_perm('global.gerer_boursiers'))
    # Add perms for BoursierAdmin inlines
    for model in ['vueensemble',
                  'depenseprevisionnelle',
                  'allocataire',
                  'allocation',
                  'allocationorigine',
                  'allocationaccueil',
                  'allocationmobilite',
                  ]:
        rules.allow_global(
            'boursiers.%s_%s' % (perm, model),
            has_global_perm('global.gerer_boursiers'))
