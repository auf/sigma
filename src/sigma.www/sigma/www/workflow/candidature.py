# -=- encoding: utf-8 -=-
from sigma.www.models import Appel, Candidature, RegionalGroup, PieceJointeCandidature, CritereSupplementaireCandidature
from django.utils.translation import ugettext as _

from sigma.www.workflow import Handler
from sigma.www.workflow import Manager
from sigma.www.workflow import WorkflowError
from sigma.www.workflow import exporter

from datetime import date
from sigma.www.utils import *

import sigma.www.workflow

class CandidatureHandler(Handler):
    """
    Representation d'un handler de workflow des candidatures

    On definit ici toutes les etapes du workflow des candidatures sous forme de:

    Etat Initial | Action | Etat Final

    Ainsi, chaque etat a sa propre methode de transition qui contient toutes 
    les validations qui sont necessaire au passage a l'etat suivant.

    Veuillez noter que le plupart des verifications qui sont faites ici sont 
    utilisees dans les tags personnalises des candidatures qui se trouvent 
    dans le module suivant:

      sigma.www.templatetags.candidature_extra
    """

    # identificateur utilise par le gestionaire de workflow afin de faire
    # l'association avec la classe geree
    classe = Candidature

    def __init__(self, user):
        """
        @param user L'utilisateur courant du site
        """
        Handler.__init__(self, user, "statut", 'Nouveau')

        ## Definition du workflow
        self.add_final('Nouveau', 'Supprimer', 'Supprime', self.supprimer)
        self.add_revert('Supprime', 'RevertSupprimer', 'Nouveau', self.supprimer)

        self.add_final('Nouveau', 'PreRejeter', 'PreIrrecevable', self.rejeter_pre)
        self.add('Nouveau', 'PreAccepter', 'PreRecevable', self.accepter_pre)


        self.add_final('PreIrrecevable', 'Rejeter', 'Irrecevable', self.rejeter)
        self.add('PreRecevable', 'Rejeter', 'Irrecevable', self.rejeter)

        self.add('PreIrrecevable', 'Accepter', 'Recevable', self.accepter)
        self.add('PreRecevable', 'Accepter', 'Recevable', self.accepter)

        self.add_revert('Recevable', 'RevertAccepterIrrecevable', 'PreIrrecevable', self.rejeter_pre)
        self.add_revert('Recevable', 'RevertAccepterRecevable', 'PreRecevable', self.accepter_pre)
        self.add_revert('Irrecevable', 'RevertRejeterIrrecevable', 'PreIrrecevable', self.rejeter_pre)
        self.add_revert('Irrecevable', 'RevertRejeterRecevable', 'PreRecevable', self.accepter_pre)

        self.add('Recevable', 'Classer', 'Classe', self.classer)
        self.add_final('Recevable', 'Declasser', 'Non-Classe', self.declasser)

        self.add_revert('Classe', 'RevertClasserRecevable', 'Recevable', self.accepter)
        self.add_revert('Non-Classe', 'RevertDeClasserRecevable', 'Recevable', self.accepter)

        self.add('Classe', 'Selectionner', 'Selectionne', self.selectionner)
        self.add_final('Classe', 'Attendre', 'Attente', self.attendre)

        self.add_revert('Selectionne', 'RevertSelectionnerClasse', 'Classe', self.classer)
        self.add_revert('Attente', 'RevertAttendreClasse', 'Classe', self.classer)

        self.add('Attente', 'Reveiller', 'Selectionne', self.reveiller)
        self.add_final('Selectionne', 'Desister', 'Desiste', self.desister)
        self.add('Selectionne', 'Boursier', 'Boursie', self.boursier)

        self.add_revert('Desiste', 'RevertDesisterSelectionne', 'Selectionne', self.selectionner)
        self.add_revert('Boursie', 'RevertBoursierSelectionne', 'Selectionne', self.selectionner)

        self.add_final('Boursie', 'Completer', 'Complet', self.completer)

        self.add_revert('Complet', 'RevertCompleterBoursie', 'Boursie', self.boursier)

        self.add_post("Supprimer", self.after_supprimer)
        self.add_post("RevertSupprimer", self.after_supprimer)

        ## On peut ainsi avoir des labels plus "user-friendly"
        label1=_("PreIrrecevable")
        label2=_("PreRecevable")
        label3=_("Irrecevable")
        label4=_("Recevable")
        label5=_("Classe")
        label6=_("Non-Classe")
        label7=_("Selectionne")
        label8=_("Attente")
        label9=_("Desiste")
        label10=_("Boursie")
        label11=_("Complet")

        ## Initialisation des exporteurs
        self.add_exporter(exporter.CandidatureODFExporter)
        self.add_exporter(exporter.GenericODSExporter)
        self.add_exporter(exporter.MultiCandidatureODFExporter)


    def supprimer(self, from_state, to_state, action, ob):
        """Verification du passage au statut supprime

        @param from_state Nouveau
        @param to_state Supprime
        @param action Supprimer
        @param ob Instance de candidature
        """
        self.assert_sys(ob.appel.statut == "Diffuse",
                        ob, from_state, to_state, 
                        _("La periode de diffusion n'est pas en cours"))

        self.assert_sys(from_state == "Nouveau" or from_state == "Supprime",
                        ob, from_state, to_state, 
                        _("La candidature ne peut pas etre supprimee"))

        self.assert_sys(to_state != ob.statut,
                         ob, from_state, to_state,
                        _("La candidature est deja supprimee"))

        appel_handler = Manager().get_handler(ob.appel, self.user)

        self.assert_sys(appel_handler.check_bureau(ob.appel), 
                        ob, from_state, to_state,
                        _("Vous ne faites pas parti du bureau de lappel de cette candidature"))


    def rejeter_pre(self, from_state, to_state, action, ob):
        """Vérification du passage au statut PreRejete

        @param from_state Nouveau
        @param to_state PreRejete
        @param action PreRejeter
        @param ob Instance de candidature
        """
        self.assert_sys(ob.appel.statut == "Diffuse" or ob.appel.statut == "Analyse",
                        ob, from_state, to_state, 
                        _("La periode de diffusion n'est pas en cours"))

        self.assert_sys(from_state == "Nouveau" or from_state == "Recevable" or from_state == "Irrecevable",
                        ob, from_state, to_state, 
                        _("La candidature a deja pre-analyse"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state, 
                        _("L'utilisateur n'a pas la permission d'analyser cette candidature"))


    def accepter_pre(self, from_state, to_state, action, ob):
        """Vérification du passage au statut PreAccepte

        @param from_state Nouveau
        @param to_state PreAccepte
        @param action PreAccepter
        @param ob Instance de candidature
        """
        self.assert_sys(ob.appel.statut == "Diffuse" or ob.appel.statut == "Analyse",
                        ob, from_state, to_state, 
                       _("La periode de diffusion n'est pas en cours"))

        self.assert_sys(from_state == "Nouveau" or from_state == "Recevable" or from_state == "Irrecevable",
                        ob, from_state, to_state, 
                        _("La candidature a deja ete pre-analyse"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state, 
                        _("L'utilisateur n'a pas la permission d'analyser cette candidature"))

        # La candidature est complete
        self.assert_criteria(self.is_valid(ob),
                             ob, from_state, to_state,
                             _("La candidature n'est pas complete"))

        # Reception dossier
        if ob.appel.inscription_date_fin and ob.date_reception:
            self.assert_criteria(ob.appel.inscription_date_fin >= ob.date_reception,
                                 ob, from_state, to_state, _("date reception non conforme"))

        # statut etudiant 
        self.assert_criteria(not ob.appel.statut_etudiant_obligatoire or ob.type == "Etudiant",
                             ob, from_state, to_state, _("statut etudiant non conforme"))

        # niveau etude
        self.assert_criteria((ob.appel.niveau_etude and ob.niveau_etude == ob.appel.niveau_etude) \
                                 or (not ob.appel.niveau_etude),
                             ob, from_state, to_state, _("niveau etude non conforme"))

        # age maximum
        self.assert_criteria(not ob.appel.age_max or calculateAge(ob.date_naissance) <= ob.appel.age_max,
                             ob, from_state, to_state, _("age non conforme"))
        
        # duree mobilite
        mobilite_duree_mois = calculateAge(ob.mobilite_debut, ob.mobilite_fin, months=True)

        self.assert_criteria(mobilite_duree_mois >= ob.appel.mobilite_duree_mois_min 
                             and mobilite_duree_mois <= ob.appel.mobilite_duree_mois_max,
                             ob, from_state, to_state, _("duree mobilite nom conforme"))

        # etablissement origine membre obligatoire        
        self.assert_criteria(not ob.appel.origine_etabl_membre_obligatoire or ob.origine_etabl,
                             ob, from_state, to_state, _("etablissement origine membre nom conforme"))

        # etablissement accueil membre obligatoire        
        self.assert_criteria(not ob.appel.accueil_etabl_membre_obligatoire or ob.accueil_etabl,
                             ob, from_state, to_state, _("etablissement accueil membre nom conforme"))

        # diplome
        diplome_duree_validite = (date.today().year - ob.diplome_date.year)
        self.assert_criteria(not ob.appel.diplome_duree_validite_obligatoire or \
                                 ob.appel.diplome_duree_validite_min <= diplome_duree_validite,
                             ob, from_state, to_state, _("diplome non conforme"))

        # alternance 
        self.assert_criteria(not ob.appel.alternance_obligatoire or \
                        (ob.accueil_duree_mois >= ob.appel.alternance_duree_min_mois and \
                             ob.origine_duree_mois >= ob.appel.alternance_duree_min_mois),
                             ob, from_state, to_state, _("Alternance non conforme"))

        # pieces jointes
        for piecejointe in PieceJointeCandidature.objects.filter(candidature=ob):
            self.assert_criteria(piecejointe.presente, ob, from_state, to_state, _("%s non present") % piecejointe)
            if piecejointe.presente:
                self.assert_criteria(piecejointe.conforme, ob, from_state, to_state, _("%s non conforme") % piecejointe)


    def rejeter(self, from_state, to_state, action, ob):
        """Verification du passage au statut Irrecevable

        @param from_state PreAccepte/PreRejete
        @param to_state   Irrecevable
        @param action     Rejeter
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut == "Analyse", ob, from_state, to_state, 
                        _("La periode d'analyse n'est pas commence"))

        self.assert_sys(from_state == "PreRecevable" or from_state == "PreIrrecevable",
                        ob, from_state, to_state, _("La candidature a deja ete analyse"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state, 
                        _("L'utilisateur n'a pas la permission de rejeter cette candidature"))


    def accepter(self, from_state, to_state, action, ob):
        """Verification du passage au statut Recevable

        @param from_state PreAccepte/PreRejete
        @param to_state   Recevable
        @param action     Accepter
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut == "Analyse" or ob.appel.statut == "Evalue",
                        ob, from_state, to_state, 
                        _("La periode d'analyse n'est pas commence"))

        self.assert_sys(from_state in ("PreRecevable", "PreIrrecevable", "Classe", "Non-Classe"),
                        ob, from_state, to_state, _("La candidature a deja ete analyse"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state,
                        _("L'utilisateur n'a pas la permission d'accepter cette candidature"))

        # Vérification que critères sont tous respectés
        for critere in CritereSupplementaireCandidature.objects.filter(candidature=ob):
            self.assert_warn(critere.valide,
                             ob, from_state, to_state,
                             _("La critere %s n'est pas respecte" % critere),
                             critere)

    def classer(self, from_state, to_state, action, ob):
        """Verification du passage au statut Classe

        @param from_state Recevable
        @param to_state   Classe
        @param action     Classer
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut in ("Evalue", "Selectionne"),
                        ob, from_state, to_state, 
                        _("La periode d'evaluation n'est pas commence"))

        self.assert_sys(from_state in ("Recevable", "Selectionne", "Attente"),
                        ob, from_state, to_state, 
                        _("La candidature n'est pas recevable"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_classe_candidature"),
                        ob, from_state, to_state,
                        _("L'utilisateur n'a pas la permission de classer cette candidature"))


    def declasser(self, from_state, to_state, action, ob):
        """Verification du passage au statut Declasse

        @param from_state Recevable
        @param to_state   Declasse
        @param action     Declasser
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut == 'Evalue', ob, from_state, to_state, 
                        _("La periode d'evaluation n'est pas commence"))

        self.assert_sys(from_state == "Recevable", ob, from_state, to_state, 
                        _("La candidature n'est pas recevable"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_classe_candidature"),
                        ob, from_state, to_state,
                        _("L'utilisateur n'a pas la permission de declasser cette candidature"))


    def selectionner(self, from_state, to_state, action, ob):
        """Verification du passage au statut Selectionne

        @param from_state Classe
        @param to_state   Selectionne
        @param action     Selectionner
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut in ('Selectionne', 'Notifie'), 
                        ob, from_state, to_state,
                        _("La periode de selection n'est pas commence"))

        self.assert_sys(from_state in ("Classe", "Attente", "Desiste", "Boursie"),
                        ob, from_state, to_state, _("La candidature n'est pas classee"))

        self.assert_sys(self.user.is_staff or  self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state,
                        _("L'utilisateur n'a pas la permission de selectionner cette candidature"))
    

    def attendre(self, from_state, to_state, action, ob):
        """Verification du passage au statut Attente

        @param from_state Classe
        @param to_state   Attente
        @param action     Attendre
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut == 'Selectionne', ob, from_state, to_state, 
                        _("La periode de selection n'est pas commence"))

        self.assert_sys(from_state == "Classe", ob, from_state, to_state, 
                        _("La candidature n'est pas classee"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state,
                        _("L'utilisateur n'a pas la permission de mettre en attente cette candidature"))


    def reveiller(self, from_state, to_state, action, ob):
        """Verification du passage au statut Selectionne

        @param from_state Attente
        @param to_state   Selectionne
        @param action     Reveiller
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut == 'Selectionne', ob, from_state, to_state, 
                        _("La periode de selection n'est pas commence"))

        self.assert_sys(from_state == "Attente", ob, from_state, to_state, 
                        _("La candidature n'est pas en attente"))

        self.assert_sys(self.user.is_staff or  self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state, 
                        _("L'utilisateur n'a pas la permission de reveiller cette candidature"))


    def desister(self, from_state, to_state, action, ob):
        """Verification du passage au statut Desiste

        @param from_state Selectionne
        @param to_state   Desiste
        @param action     Desister
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut == 'Notifie', ob, from_state, to_state,
                        _("La periode de selection n'est pas commence"))

        self.assert_sys(from_state == "Selectionne", ob, from_state, to_state, 
                        _("La candidature n'est pas selectionne"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state, 
                        _("L'utilisateur n'a pas la permission de desister cette candidature"))


    def boursier(self, from_state, to_state, action, ob):
        """Verification du passage au statut Boursie

        @param from_state Selectionne
        @param to_state   Boursie
        @param action     Boursier
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut in ('Notifie', "Suivie"),
                        ob, from_state, to_state, 
                        _("La periode de selection n'est pas commence"))

        self.assert_sys(from_state in ("Selectionne", "Complet"),
                        ob, from_state, to_state,
                        _("La candidature n'est pas selectionne"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state, 
                        _("L'utilisateur n'a pas la permission de rendre boursier cette candidature"))


    def completer(self, from_state, to_state, action, ob):
        """Verification du passage au statut Complete

        @param from_state Boursie
        @param to_state   Complet
        @param action     Completer
        @param ob         Instance de candidature
        """
        self.assert_sys(ob.appel.statut == 'Suivie', ob, from_state, to_state, 
                        _("La periode de suivie n'est pas commence"))

        self.assert_sys(from_state == "Boursie", ob, from_state, to_state, 
                        _("La candidature n'est pas boursiere"))

        self.assert_sys(self.user.is_staff or self.user.has_perm("www.can_select_candidature"),
                        ob, from_state, to_state, 
                        _("L'utilisateur n'a pas la permission completer cette candidature"))

    #### Methode post

    def after_supprimer(self, candidature):
        """Apres la suppression d'une candidature, on s'assure de la rendre inactive

        @param candidature
        """
        if candidature.statut == "Supprime":
            candidature.actif = False
        else:
            candidature.actif = True
        candidature.save()


    #### Methodes automatiques

    def auto_analyse(self, candidature):
        """Analyse automatique des candidatures

        @param candidature Instance de candidature"""
        try:
            Manager().execute(candidature, self.user, "PreAccepter")
        except WorkflowError:
            Manager().execute(candidature, self.user, "PreRejeter")


    #### Methodes utilitaire
    def is_valid(self, candidature):
        """ Est-ce que la candidature est complete, que ces champs
        obligatoires sont remplis

        @param candidature
        """
        for field in candidature._meta.fields:
            if not field.blank:
                try:
                    if not getattr(candidature, field.name):
                        if field.name in Candidature.field_dependencies.keys():
                            depends = Candidature.field_dependencies[field.name]
                            return True and getattr(candidature, depends)
                        elif field.name in Candidature.field_dependencies.values():
                            for key in Candidature.field_dependencies.keys():
                                if Candidature.field_dependencies[key] == field.name:
                                    return True and getattr(candidature, key)
                        return False
                except AttributeError:
                    pass
        return True


    def can_add(self, appel):
        """Est-ce que c'est possible d'ajouter une nouvelle candidature
        pour un appel d'offre, pour l'utilisateur courant ?

        @param appel L'appel d'offre en question
        """
        if self.user.is_staff:
            return appel.statut == "Diffuse"
        elif self.user.has_perm('www.add_candidature'):
            if Manager().get_handler(appel, self.user).check_bureau(appel):
                return appel.statut == "Diffuse"
        return False


    def can_edit(self, candidature):
        """Est-ce que c'est possible d'ajouter une nouvelle candidature
        pour un appel d'offre, pour l'utilisateur courant ?

        @param appel L'appel d'offre en question
        """
        appel = candidature.appel

        if self.user.is_staff:
            return True

        if Manager().get_handler(appel, self.user).check_bureau(appel):
            return self.user.has_perm('www.change_candidature')
        return False

    def can_note(self, candidature):
        """Est-ce que c'est possible de noter cette candidature
        pour l'utilisateur courant

        @param candidature La candidature a noter
        """
        if self.user.is_staff:
            return True
        if self.user.is_expert():
            return True
        return self.can_edit(candidature)


Manager().register(CandidatureHandler)
