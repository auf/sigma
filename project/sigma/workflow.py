# -*- encoding: utf-8 -*-

from auf.django.workflow.models import WorkflowMixin

#codes actions
APPEL_ACTION_CREER = u'CREER'

# codes états
APPEL_ETAT_NOUVEAU = 'NOUVEAU'

#libellés états
APPEL_ETATS = {
    APPEL_ETAT_NOUVEAU : u'Nouveau',
    }

# définition du worflow séquentiel
APPEL_ACTIONS = {
    APPEL_ACTION_CREER : {
        'nom' : u'Créer',
        'etat_initial' : None,
        'etat_final' : APPEL_ETAT_NOUVEAU,
    },
    
}

class AppelWorkflow(WorkflowMixin):
    etat_initial = APPEL_ETAT_NOUVEAU
    etats = APPEL_ETATS
    actions = APPEL_ACTIONS

    class Meta:
        abstract = True
