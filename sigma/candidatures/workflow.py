# -*- encoding: utf-8 -*-

from auf.django.workflow.models import WorkflowMixin

# https://redmine.auf.org/issues/4031

#Nouveau
#(par défaut tout dossier auquel le correspondant n'a pas encore changé le statut)

#Irrecevable
#(par rapport aux conditions de candidature et pièces,
#ne sera pas évalué / à voir pour l'import de WCS car la recevabilité se fera probablement dans WCS)

#Recevable
#(dossier à évaluer)

#Non-retenu (Rejeté)
#(évalué mais pas retenu)

#En attente
#(liste de réserves avec un classement hiérarchisé, dans laquelle seront récupérés les remplaçants en cas de désistement)

#Retenu
#(dans l'étape de gestion de la bourse seuls ces dossiers seront pris en compte et visibles dans la partie boursiers)

#Désisté
#(un « Boursier » qui renonce à la bourse après l'attribution)

#codes actions
DOSSIER_ACTION_CREER = u'CREER'

# codes états
DOSSIER_ETAT_NOUVEAU = 'NOUVEAU'
DOSSIER_ETAT_IRRECEVABLE = 'IRRECEVABLE'
DOSSIER_ETAT_RECEVABLE = 'RECEVABLE'
DOSSIER_ETAT_REJETE = 'REJETE'
DOSSIER_ETAT_ATTENTE = 'ATTENTE'
DOSSIER_ETAT_RETENU = 'RETENU'
DOSSIER_ETAT_DESISTE = 'DESISTE'


#libellés états
DOSSIER_ETATS = {
    DOSSIER_ETAT_NOUVEAU: 'Nouveau',
    DOSSIER_ETAT_IRRECEVABLE: 'Irrecevable',
    DOSSIER_ETAT_RECEVABLE: 'Recevable',
    DOSSIER_ETAT_ATTENTE: 'En attente',
    DOSSIER_ETAT_REJETE: 'Non retenu',
    DOSSIER_ETAT_RETENU: 'Retenu',
    DOSSIER_ETAT_DESISTE: 'Désisté',
}

DOSSIER_ACTIONS = {
    DOSSIER_ETAT_NOUVEAU: {
        'nom': DOSSIER_ETATS[DOSSIER_ETAT_NOUVEAU],
        'etat_initial': None,
        'etat_final': DOSSIER_ETAT_NOUVEAU,
        },
    DOSSIER_ETAT_IRRECEVABLE: {
        'nom': DOSSIER_ETATS[DOSSIER_ETAT_IRRECEVABLE],
        'etat_initial': (DOSSIER_ETAT_NOUVEAU, DOSSIER_ETAT_RECEVABLE),
        'etat_final': DOSSIER_ETAT_IRRECEVABLE,
        },
    DOSSIER_ETAT_RECEVABLE: {
        'nom': DOSSIER_ETATS[DOSSIER_ETAT_RECEVABLE],
        'etat_initial': (DOSSIER_ETAT_NOUVEAU, DOSSIER_ETAT_IRRECEVABLE,),
        'etat_final': DOSSIER_ETAT_RECEVABLE,
        },
    DOSSIER_ETAT_ATTENTE: {
        'nom': DOSSIER_ETATS[DOSSIER_ETAT_ATTENTE],
        'etat_initial': (DOSSIER_ETAT_RECEVABLE, DOSSIER_ETAT_RETENU,
            DOSSIER_ETAT_REJETE,),
        'etat_final': DOSSIER_ETAT_ATTENTE,
        },
    DOSSIER_ETAT_REJETE: {
        'nom': DOSSIER_ETATS[DOSSIER_ETAT_REJETE],
        'etat_initial': (DOSSIER_ETAT_RECEVABLE, DOSSIER_ETAT_ATTENTE, DOSSIER_ETAT_RETENU,),
        'etat_final': DOSSIER_ETAT_REJETE,
        },
    DOSSIER_ETAT_RETENU: {
        'nom': DOSSIER_ETATS[DOSSIER_ETAT_RETENU],
        'etat_initial': (DOSSIER_ETAT_RECEVABLE, DOSSIER_ETAT_ATTENTE,
            DOSSIER_ETAT_REJETE, ),
        'etat_final': DOSSIER_ETAT_RETENU,
        },
    DOSSIER_ETAT_DESISTE: {
        'nom': DOSSIER_ETATS[DOSSIER_ETAT_DESISTE],
        'etat_initial': (DOSSIER_ETAT_RETENU, ),
        'etat_final': DOSSIER_ETAT_DESISTE,
        },
    }


class DossierWorkflow(WorkflowMixin):
    etat_initial = DOSSIER_ETAT_NOUVEAU
    etats = DOSSIER_ETATS
    actions = DOSSIER_ACTIONS

    class Meta:
        abstract = True

    def acces_nouveau(self, action, request):
        return True

    def acces_irrecevable(self, action, request):
        return True

    def acces_recevable(self, action, request):
        return True

    def acces_rejete(self, action, request):
        return True

    def acces_attente(self, action, request):
        return True

    def acces_retenu(self, action, request):
        return True

    def acces_desiste(self, action, request):
        return True
