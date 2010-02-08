# -=- encoding: utf-8 -=-
from sigma.www.models import Appel, Candidature, RegionalGroup

from sigma.www.workflow import Handler
from sigma.www.workflow import Manager
from sigma.www.workflow import WorkflowError
from sigma.www.workflow import exporter

import datetime 

class AppelHandler(Handler):
    """
    Representation d'un handler de wokflow des appels

    On definit ici toutes les etapes du workflow des appels d'offres sous 
    forme de:

    # Etat Initial
    # Action
    # Etat Final

    Ainsi, chaque etat a sa propre methode de transition qui contient toutes 
    les validations qui sont necessaire au passage a l'etat suivant.

    Veuillez noter que le plupart des verifications qui sont faites ici 
    sont utilisees dans les tags personnalises des appels qui se trouvent 
    dans le module suivant:

      sigma.www.templatetags.appel_extra

    Notons que certaines transitions déclenchent aussi un certains nombre
    d'actions. Pour se faire, on a seulement qu'à définir en plus une 
    "post_actions" ainsi::

       self.add_post("Analyser", self.after_diffuse)

    Dans le cas présent, la méthode after_diffuse sera appelé après le passage
    à l'état "Analyse".
    """

    # identificateur utilise par le gestionaire de workflow afin de faire
    # l'association avec la classe geree
    classe = Appel
    
    def __init__(self, user):
        """
        Définition du workflow des appels d'offre

        @param user L'utilisateur courant du site
        """
        Handler.__init__(self, user, "statut", 'Nouveau')

        self.add_final('Nouveau', 'Supprimer', 'Supprime', self.supprimer)
        self.add('Nouveau', 'Ouvrir', 'Diffuse', self.ouvrir)
        self.add('Diffuse', 'Analyser', 'Analyse', self.analyser)
        self.add('Analyse', 'Evaluer', 'Evalue', self.evaluer)
        self.add('Evalue', 'Selectionner', 'Selectionne', self.selectionner)
        self.add('Selectionne', 'Notifier', 'Notifie', self.notifier)
        self.add('Notifie', 'Suivre', 'Suivie', self.suivre)
        self.add_final('Suivie', 'Fermer', 'Ferme', self.fermer)

        self.add_post("Analyser", self.after_diffuser)
        self.add_post("Supprimer", self.after_supprimer)

        self.add_exporter(exporter.GenericODSExporter)

    def check_bureau(self, appel):
        """
        Méthode s'assurant que l'utilisateur courant, celui qui a initalisé 
        le workflow, appartient à un groupe qui lui donne droit de 
        manipuler cet appel

        @param user L'utilisateur à vérifier
        @param appel L'appel d'offre a examiné
        """
        if self.user.is_staff:
            return True
        bureau = appel.projetposte.code_bureau
        for group in self.user.groups.iterator():
            if RegionalGroup.objects.get(id=group.id).bureau == bureau:
                return True
        return False

    def ouvrir(self, from_state, to_state, action, ob):
        """
        Vérification du passage au statut Diffusé

        @param from_state État initial: Nouveau
        @param to_state   État final:  Diffuse
        @param action     Action: Ouvrir
        @param ob         Objet
        """
        self.assert_sys(self.check_bureau(ob), ob, from_state, to_state, 
                        "Vous ne faites pas parti du bureau de cet appel d'offre")

        self.assert_sys(from_state == "Nouveau", ob, from_state, to_state, 
                        "L'appel d'offre n'est pas nouveau")

        self.assert_sys(ob.inscription_date_debut <= datetime.datetime.now().date(),
                        ob, from_state, to_state, 
                        "La période d'ouverture n'est pas encore commencée")


    def supprimer(self, from_state, to_state, action, ob):
        """
        Vérification du passage au statut Supprimé

        @param from_state État initial: Nouveau
        @param to_state   État final: Supprime
        @param action     Action: Supprimer
        @param ob         Objet
        """
        self.assert_sys(self.check_bureau(ob), ob, from_state, to_state, 
                        "Vous ne faites pas parti du bureau de cet appel d'offre")

        self.assert_sys(from_state == "Nouveau", ob, from_state, to_state, 
                        "Impossible de supprimer un appel d'offre une fois ouvert")


    def analyser(self, from_state, to_state, action, ob):
        """
        Vérification du passage au statut Analyse

        @param from_state État initial: Diffuse
        @param to_state   État final: Analyse
        @param action     Action: Analyser
        @param ob         Objet
        """
        self.assert_sys(self.check_bureau(ob), ob, from_state, to_state, 
                        "Vous ne faites pas parti du bureau de cet appel d'offre")

        self.assert_sys(from_state == "Diffuse", ob, from_state, to_state, 
                        "L'appel d'offre n'est pas en phase de diffusion")

        for candidature in Candidature.objects.filter(appel=ob):
            if candidature.statut != "Supprime":
                handler = Manager().get_handler(candidature, self.user)                
                self.assert_sys(handler.is_valid(candidature),
                                ob, from_state, to_state, 
                                "Une candidature est encore incomplete")

    def evaluer(self, from_state, to_state, action, ob):
        """
        Vérification du passage au statut Evalue

        @param from_state Etat initial: Analyse
        @param to_state   Etat final: Evalue
        @param action     Action: Evaluer
        @param ob         Objet
        """

        self.assert_sys(self.check_bureau(ob), ob, from_state, to_state, 
                        "Vous ne faites pas parti du bureau de cet appel d'offre")

        self.assert_sys(from_state == "Analyse", ob, from_state, to_state, 
                        "L'appel d'offre n'est pas en phase d'analyse")

        for candidature in Candidature.objects.filter(appel=ob, actif=True):
            self.assert_sys(candidature.statut != "PreIrrecevable" and candidature.statut != "PreRecevable",
                            ob, from_state, to_state, 
                            "Une candidature doit encore être analysée")


    def selectionner(self, from_state, to_state, action, ob):
        """
        Vérification du passage au statut Selectionne

        @param from_state État initial: Evalue
        @param to_state   État final: Selectionne
        @param action     Action: Selectionner
        @param ob         Objet
        """
        self.assert_sys(self.check_bureau(ob), ob, from_state, to_state, 
                     "Vous ne faites pas parti du bureau de cet appel d'offre")

        self.assert_sys(from_state == "Evalue", ob, from_state, to_state, 
                        "L'appel d'offre n'est pas en phase d'analyse")

        for candidature in Candidature.objects.filter(appel=ob, actif=True):
            self.assert_sys(candidature.statut != "Recevable",
                            ob, from_state, to_state, 
                            "Une candidature doit encore etre analysée")


    def notifier(self, from_state, to_state, action, ob):
        """
        Vérification du passage au statut Notifie

        @param from_state Etat initial: Selectionne
        @param to_state   Etat final: Notifie
        @param action     Action: Notifie
        @param ob         Objet
        """
        self.assert_sys(self.check_bureau(ob), ob, from_state, to_state, 
                        "Vous ne faites pas parti du bureau de cet appel d'offre")

        self.assert_sys(from_state == "Selectionne", ob, from_state, to_state,
                        "L'appel d'offre n'est pas en phase de sélection")

        for candidature in Candidature.objects.filter(appel=ob, actif=True):
            self.assert_sys(candidature.statut != "Classe",
                            ob, from_state, to_state,
                            "Une candidature doit encore être selectionnée")
            
    def suivre(self, from_state, to_state, action, ob):
        """
        Vérification du passage au statut Suivie

        @param from_state Etat initial: Notifie
        @param to_state   Etat final: Suivie
        @param action     Action: Suivre
        @param ob         Objet
        """
        self.assert_sys(self.check_bureau(ob), ob, from_state, to_state,
                        "Vous ne faites pas parti du bureau de cet appel d'offre")

        self.assert_sys(from_state == "Notifie", ob, from_state, to_state, 
                        "L'appel d'offre n'est pas en phase de notification")

        for candidature in Candidature.objects.filter(appel=ob, actif=True):
            self.assert_sys(candidature.statut != "Selectionne",
                            ob, from_state, to_state, 
                            "Une candidature doit encore être notifiée")

    def fermer(self, from_state, to_state, action, ob):
        """
        Vérification du passage au statut Ferme

        @param from_state Etat initial: Suivie
        @param to_state   Etat final: Ferme
        @param action     Action: Fermer
        @param ob         Objet
        """
        self.assert_sys(self.check_bureau(ob), ob, from_state, to_state,
                        "Vous ne faites pas parti du bureau de cet appel d'offre")

        self.assert_sys(from_state == "Suivie", ob, from_state, to_state, 
                        "L'appel d'offre n'est pas en phase de suivie")

        for candidature in Candidature.objects.filter(appel=ob, actif=True):
            self.assert_sys(candidature.statut != "Boursie", 
                            ob, from_state, to_state, 
                            "Une candidature doit encore être suivie")
        

    def is_readable(self, ob):
        """
        Est-ce que l'appel d'offre ob est lisisble pour l'utilisateur specifie

        @param ob Objet L'appel d'offre peut être affiché
        """
        if ob.statut == "Supprime":
            return False
        if self.user.is_staff:
            return True
        return self.check_bureau(ob)


    def can_add(self):
        """Est-ce que l'utilisateur courant peut ajouter des appels d'offre"""
        if self.user.is_staff:
            return True
        return self.user.has_perm('www.add_appel')


    def can_edit(self, appel):
        """Est-ce que l'utilisateur courant peut editer des appels d'offre"""
        if self.user.is_staff:
            return True
        if self.user.has_perm('www.change_appel'):
            return self.check_bureau(ob)

        return False


    def after_diffuser(self, appel):
        """Après le passage à l'étape diffusé on rejète ou accepte toutes 
        les candidatures de l'appel d'offre
        
        @param appel Appel d'offre courant
        """
        for candidature in Candidature.objects.filter(appel=appel, actif=True):
            Manager().get_handler(candidature, self.user).auto_analyse(candidature)


    def after_supprimer(self, appel):
        """Apres la suppression d'un appel d'offre, on s'assure de le mettre inactif

        @param appel
        """
        appel.actif = False
        appel.save()

## Enregistrement du handler aupres du manager de workflows
Manager().register(AppelHandler)
