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


#codes actions
DOSSIER_ACTION_CREER = u'CREER'

# codes états
DOSSIER_ETAT_NOUVEAU        = 'NOUVEAU'
DOSSIER_ETAT_INCOMPLET      = 'INCOMPLET'
DOSSIER_ETAT_ATTENTE        = 'ATTENTE'
DOSSIER_ETAT_EN_COURS       = 'EN_COURS'
DOSSIER_ETAT_A_VERIFIER     = 'A_VERIFIER'
DOSSIER_ETAT_IRRECEVABLE    = 'IRRECEVABLE'
DOSSIER_ETAT_REJETE         = 'REJETE'
DOSSIER_ETAT_RAPPROCHE      = 'RAPPROCHE'
DOSSIER_ETAT_RECEVABLE      = 'RECEVABLE'
DOSSIER_ETAT_NON_CLASSE     = 'NON_CLASSE'
DOSSIER_ETAT_CLASSE         = 'CLASSE'
DOSSIER_ETAT_RETENU         = 'RETENU'
DOSSIER_ETAT_BOURSIER       = 'BOURSIER'
DOSSIER_ETAT_DECLASSE       = 'DECLASSE'

#libellés états
DOSSIER_ETATS = {
    DOSSIER_ETAT_NOUVEAU        : 'Nouveau',
    DOSSIER_ETAT_INCOMPLET      : 'Incomplet',
    DOSSIER_ETAT_ATTENTE        : 'En attente',
    DOSSIER_ETAT_EN_COURS       : 'En cours',
    DOSSIER_ETAT_A_VERIFIER     : 'A vérifier',
    DOSSIER_ETAT_IRRECEVABLE    : 'Irrecevable',
    DOSSIER_ETAT_REJETE         : 'Rejeté',
    DOSSIER_ETAT_RAPPROCHE      : 'Rapproché',
    DOSSIER_ETAT_RECEVABLE      : 'Recevable',
    DOSSIER_ETAT_NON_CLASSE     : 'Non classé',
    DOSSIER_ETAT_CLASSE         : 'Classé',
    DOSSIER_ETAT_RETENU         : 'Retenu',
    DOSSIER_ETAT_BOURSIER       : 'Boursier',
    DOSSIER_ETAT_DECLASSE       : 'Déclassé',
    }

# Création des actions à partir des états
# le workflow est très permissif, pour le générer de cette
# façon, autrement on pourrait faire un dictionnaire pour créer chaque action
DOSSIER_ACTIONS = {}
for etat in DOSSIER_ETATS.keys():
    DOSSIER_ACTIONS[etat] = {
        'nom' : DOSSIER_ETATS[etat],
        'etat_initial' : DOSSIER_ETATS.keys(),
        'etat_final' : etat,
        }

# À la création, attribution automatique de l'état
DOSSIER_ACTIONS[DOSSIER_ETAT_NOUVEAU]['etat_initial'] = None

class DossierWorkflow(WorkflowMixin):
    etat_initial = DOSSIER_ETAT_NOUVEAU
    etats = DOSSIER_ETATS
    actions = DOSSIER_ACTIONS

    class Meta:
        abstract = True
