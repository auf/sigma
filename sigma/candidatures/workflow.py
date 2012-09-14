# -*- encoding: utf-8 -*-

from auf.django.workflow.models import WorkflowMixin

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

    def acces_declasse(self, action, request):
        return True

    def acces_en_cours(self, action, request):
        return True

    def acces_rejete(self, action, request):
        return True

    def acces_rapproche(self, action, request):
        return True

    def acces_retenu(self, action, request):
        return True

    def acces_incomplet(self, action, request):
        return True

    def acces_attente(self, action, request):
        return True

    def acces_non_classe(self, action, request):
        return True

    def acces_classe(self, action, request):
        return True

    def acces_a_verifier(self, action, request):
        return True

    def acces_boursier(self, action, request):
        return True

    def acces_recevable(self, action, request):
        return True

    def acces_irrecevable(self, action, request):
        return True
