# -=- encoding: utf-8 -=-
import datetime 

from sigma.www.testcases.sigmatestcase import SigmaTestCase
from sigma.www.models import Categorie, ProjetPoste, Appel, Candidature
from sigma.references.models import \
    Poste, Pays, Etablissement, Discipline, Bureau
from sigma.www import workflow

__all__ = ['TestAppelWorkflow', 'TestCandidatureWorkflow']

class TestCandidatureWorkflow(SigmaTestCase):
    """Test du workflow des candidature seulement et de ces variations"""
    def setUp(self):
        """Configuration de chacun des tests"""
        SigmaTestCase.setUp(self)
        poste = Poste.objects.all()[0]
        self.cat = Categorie(nom='test', 
                             poste = poste,
                             exception_possible = True,
                             renouvellement_possible = True,
                             renouvellement_nb_max = 2,
                             age_max = 25,
                             statut_etudiant_obligatoire = True,
                             mobilite_duree_mois_min = 20,
                             mobilite_duree_mois_max = 25,
                             origine_etabl_membre_obligatoire = True,
                             accueil_etabl_membre_obligatoire = True,
                             diplome_duree_validite_obligatoire = True,
                             diplome_duree_validite_min = 10,
                             alternance_obligatoire = True,
                             alternance_duree_min_mois = 100)
        self.cat.save(force_insert=True)
        
        projetposte = ProjetPoste.objects.all()[0]
        self.app = Appel(nom="Appel d'offre 2",
                    projetposte=projetposte,
                    renouvellement_possible = True,
                    renouvellement_nb_max=10,
                    inscription_date_debut=datetime.date(2009, 03, 22),
                    inscription_date_fin=datetime.date(2009, 03, 23),
                    mobilite_date_debut=datetime.date(2009, 03, 24),
                    mobilite_date_fin=datetime.date(2009, 03, 26),
                    age_max=45,
                    statut_etudiant_obligatoire=True,
                    mobilite_duree_mois_min=9,
                    mobilite_duree_mois_max=20,
                    origine_etabl_membre_obligatoire=True,
                    accueil_etabl_membre_obligatoire=True,
                    diplome_duree_validite_obligatoire=True,
                    diplome_duree_validite_min=20,
                    alternance_obligatoire=True,
                    alternance_duree_min_mois=12)
        self.app.save()

        self.app3 = Appel(nom="Appel d'offre 3",
                    projetposte=projetposte,
                    renouvellement_possible = True,
                    renouvellement_nb_max=10,
                    inscription_date_debut=datetime.date(2009, 03, 22),
                    inscription_date_fin=datetime.date(2009, 03, 23),
                    mobilite_date_debut=datetime.date(2009, 03, 24),
                    mobilite_date_fin=datetime.date(2009, 03, 26),
                    age_max=45,
                    statut_etudiant_obligatoire=True,
                    mobilite_duree_mois_min=10,
                    mobilite_duree_mois_max=20,
                    origine_etabl_membre_obligatoire=True,
                    accueil_etabl_membre_obligatoire=True,
                    diplome_duree_validite_obligatoire=True,
                    diplome_duree_validite_min=20,
                    alternance_obligatoire=True,
                    alternance_duree_min_mois=12)
        self.app3.save()

        self.can = Candidature(nom = "Leduc",
                           prenom = "Mathieu",
                           nationalite = Pays.objects.all()[0],
                           genre = "M",
                           nom_jeune_fille = "",
                           civilite = "M.",
                           date_naissance = datetime.date(1981, 12, 23),
                           pays_naissance = Pays.objects.all()[0],
                           ville_naissance = "Montreal",
                           adresse = "5591 Esplanade",
                           ville = "Montreal",
                           province = "Quebec",
                           pays = Pays.objects.all()[0],
                           code_postal = "H2T 2Z9",
                           tel = "514-568-1234",
                           fax = "514-556-9878",
                           tel_professionnel = "",
                           fax_professionnel = "",
                           courriel = "",
                           fonction = "",
                           diplome_intitule = "Bac",
                           diplome_date = datetime.date(1976, 03, 26),
                           etablissement = Etablissement.objects.all()[0],
                           discipline = Discipline.objects.all()[0],
                           type = "Etudiant",
                           reception_bureau = Bureau.objects.all()[0],
                           date_reception = datetime.date(2009, 03, 21),
                           appel = self.app,
                           mobilite_debut = datetime.date(2009, 06, 26),
                           mobilite_fin = datetime.date(2010, 03, 26),
                           mobilite_debute_accueil = datetime.date(2009, 07, 26),
                           origine_pays = Pays.objects.all()[0],
                           origine_etabl = Etablissement.objects.all()[0],
                           origine_etabl_autre = "",
                           origine_duree_mois = 12,
                           origine_resp_institutionnel_civilite = "M.",
                           origine_resp_institutionnel_nom = "Tremblay",
                           origine_resp_institutionnel_prenom = "Roger",
                           origine_resp_institutionnel_fonction = "Responsable",
                           origine_resp_scientifique_civilite = "M.",
                           origine_resp_scientifique_nom = "Ledoux",
                           origine_resp_scientifique_prenom = "Michel",
                           origine_resp_scientifique_fonction = "Responsable",
                           accueil_pays = Pays.objects.all()[0],
                           accueil_etabl = Etablissement.objects.all()[0],
                           accueil_etabl_autre = "",
                           accueil_duree_mois = 12,
                           accueil_resp_institutionnel_civilite = "M.",
                           accueil_resp_institutionnel_nom = "Cyr",
                           accueil_resp_institutionnel_prenom = "Michel",
                           accueil_resp_institutionnel_fonction = "Responsable",
                           accueil_resp_scientifique_civilite = "M.",
                           accueil_resp_scientifique_nom = "Patate",
                           accueil_resp_scientifique_prenom = "Michel",
                           accueil_resp_scientifique_fonction = "Responsable")
        self.can.save()

    def test_analyse_candidatures_recevable(self):
        """L'analyse des candidatures recevables"""
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreRecevable')

    def test_analyse_candidtures_irrecevable_date_reception(self):
        """L'analyse des candidatures irrecevables à cause de la date de réception"""
        for candidature in Candidature.objects.filter(appel=self.app):
            candidature.date_reception = datetime.date(2009, 04, 23)
            candidature.save()
        
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreIrrecevable')
            
    def test_analyse_candidtures_irrecevable_statut_etudiant(self):
        """L'analyse des candidatures irrecevables à cause d'un statut non-étudiant"""
        for candidature in Candidature.objects.filter(appel=self.app):
            candidature.type = "bidon"
            candidature.save()
        
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreIrrecevable')

    def test_analyse_candidtures_irrecevable_age_max(self):
        """L'analyse des candidatures irrecevables à cause de l'âge maximum"""
        for candidature in Candidature.objects.filter(appel=self.app):
            candidature.date_naissance = datetime.date(1945, 12, 23)
            candidature.save()
        
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreIrrecevable')

    def test_analyse_candidtures_irrecevable_mobilite_debut(self):
        """L'analyse des candidatures irrecevables à cause de la période de mobilité"""
        for candidature in Candidature.objects.filter(appel=self.app):
            candidature.mobilite_debut = datetime.date(1945, 12, 23)
            candidature.save()
        
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreIrrecevable')

    def test_analyse_candidtures_irrecevable_origin_etabl(self):
        """L'analyse des candidatures irrecevables à cause d'un établissement d'origine non-membre"""
        for candidature in Candidature.objects.filter(appel=self.app):
            candidature.origine_etabl = None
            candidature.origine_etabl_autre = "Etablissement bidon"
            candidature.save()
        
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)


        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreIrrecevable')

    def test_analyse_candidtures_irrecevable_accueil_etabl(self):
        """L'analyse des candidatures irrecevables à cause d'un établissement d'accueil non-membre"""
        for candidature in Candidature.objects.filter(appel=self.app):
            candidature.accueil_etabl = None
            candidature.accueil_etabl_autre = "Etablissement bidon"
            candidature.save()
        
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreIrrecevable')

    def test_analyse_candidtures_irrecevable_diplome_duree_validite(self):
        """L'analyse des candidatures irrecevables à cause de la durée de validité du diplôme"""
        for candidature in Candidature.objects.filter(appel=self.app):
            candidature.diplome_date = datetime.date(2009, 12, 12)
            candidature.save()
        
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreIrrecevable')

    def test_analyse_candidtures_irrecevable_alternance_obligatoire(self):
        """L'analyse des candidatures irrecevables à cause de l'alternance"""
        for candidature in Candidature.objects.filter(appel=self.app):
            candidature.accueil_duree_mois = 0 
            candidature.origine_duree_mois = 0
            candidature.save()
        
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification de chaque candidature de l'appel d'offre
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertEqual(candidature.statut, 'PreIrrecevable')
        

class TestAppelWorkflow(SigmaTestCase):
    """Test du workflow des appels et par le fait meme de certaines des 
    caracteristiques des candidatures
    """

    def setUp(self):
        """Configuration de chacun des tests"""
        SigmaTestCase.setUp(self)
        poste = Poste.objects.all()[0]
        self.cat = Categorie(nom='test', 
                        poste = poste,
                        exception_possible = True,
                        renouvellement_possible = True,
                        renouvellement_nb_max = 2,
                        age_max = 25,
                        statut_etudiant_obligatoire = True,
                        mobilite_duree_mois_min = 20,
                        mobilite_duree_mois_max = 25,
                        origine_etabl_membre_obligatoire = True,
                        accueil_etabl_membre_obligatoire = True,
                        diplome_duree_validite_obligatoire = True,
                        diplome_duree_validite_min = 10,
                        alternance_obligatoire = True,
                        alternance_duree_min_mois = 100)
        self.cat.save(force_insert=True)

        projetposte = ProjetPoste.objects.all()[0]
        self.app = Appel(nom="Appel d'offre 2",
                    projetposte=projetposte,
                    renouvellement_possible = True,
                    renouvellement_nb_max=10,
                    inscription_date_debut=datetime.date(2009, 03, 22),
                    inscription_date_fin=datetime.date(2009, 03, 23),
                    mobilite_date_debut=datetime.date(2009, 03, 24),
                    mobilite_date_fin=datetime.date(2009, 03, 26),
                    age_max=45,
                    statut_etudiant_obligatoire=True,
                    mobilite_duree_mois_min=10,
                    mobilite_duree_mois_max=20,
                    origine_etabl_membre_obligatoire=True,
                    accueil_etabl_membre_obligatoire=True,
                    diplome_duree_validite_obligatoire=True,
                    diplome_duree_validite_min=20,
                    alternance_obligatoire=True,
                    alternance_duree_min_mois=12)
        self.app.save()

        self.app3 = Appel(nom="Appel d'offre 3",
                    projetposte=projetposte,
                    renouvellement_possible = True,
                    renouvellement_nb_max=10,
                    inscription_date_debut=datetime.date(2009, 03, 22),
                    inscription_date_fin=datetime.date(2009, 03, 23),
                    mobilite_date_debut=datetime.date(2009, 03, 24),
                    mobilite_date_fin=datetime.date(2009, 03, 26),
                    age_max=45,
                    statut_etudiant_obligatoire=True,
                    mobilite_duree_mois_min=10,
                    mobilite_duree_mois_max=20,
                    origine_etabl_membre_obligatoire=True,
                    accueil_etabl_membre_obligatoire=True,
                    diplome_duree_validite_obligatoire=True,
                    diplome_duree_validite_min=20,
                    alternance_obligatoire=True,
                    alternance_duree_min_mois=12)
        self.app3.save()

        self.can = Candidature(nom = "Leduc",
                           prenom = "Mathieu",
                           nationalite = Pays.objects.all()[0],
                           genre = "M",
                           nom_jeune_fille = "",
                           civilite = "M.",
                           date_naissance = datetime.date(1981, 12, 23),
                           pays_naissance = Pays.objects.all()[0],
                           ville_naissance = "Montreal",
                           adresse = "5591 Esplanade",
                           ville = "Montreal",
                           province = "Quebec",
                           pays = Pays.objects.all()[0],
                           code_postal = "H2T 2Z9",
                           tel = "514-568-1234",
                           fax = "514-556-9878",
                           tel_professionnel = "",
                           fax_professionnel = "",
                           courriel = "",
                           fonction = "",
                           diplome_intitule = "Bac",
                           diplome_date = datetime.date(2001, 03, 26),
                           etablissement = Etablissement.objects.all()[0],
                           discipline = Discipline.objects.all()[0],
                           type = "Etudiant",
                           reception_bureau = Bureau.objects.all()[0],
                           date_reception = datetime.date(2009, 03, 21),
                           appel = self.app,
                           mobilite_debut = datetime.date(2009, 06, 26),
                           mobilite_fin = datetime.date(2010, 03, 26),
                           mobilite_debute_accueil = datetime.date(2009, 07, 26),
                           origine_pays = Pays.objects.all()[0],
                           origine_etabl = Etablissement.objects.all()[0],
                           origine_etabl_autre = "",
                           origine_duree_mois = 12,
                           origine_resp_institutionnel_civilite = "M.",
                           origine_resp_institutionnel_nom = "Tremblay",
                           origine_resp_institutionnel_prenom = "Roger",
                           origine_resp_institutionnel_fonction = "Responsable",
                           origine_resp_scientifique_civilite = "M.",
                           origine_resp_scientifique_nom = "Ledoux",
                           origine_resp_scientifique_prenom = "Michel",
                           origine_resp_scientifique_fonction = "Responsable",
                           accueil_pays = Pays.objects.all()[0],
                           accueil_etabl = Etablissement.objects.all()[0],
                           accueil_etabl_autre = "",
                           accueil_duree_mois = 12,
                           accueil_resp_institutionnel_civilite = "M.",
                           accueil_resp_institutionnel_nom = "Cyr",
                           accueil_resp_institutionnel_prenom = "Michel",
                           accueil_resp_institutionnel_fonction = "Responsable",
                           accueil_resp_scientifique_civilite = "M.",
                           accueil_resp_scientifique_nom = "Patate",
                           accueil_resp_scientifique_prenom = "Michel",
                           accueil_resp_scientifique_fonction = "Responsable")
        self.can.save()
        
    def test_starting_statut(self):
        """Verification que les appels d'offres sont toujours Nouveaux 
        initialement"""
        self.assertEqual(self.app.statut, 'Nouveau')


    def test_evolution_statut(self):
        """Verification de l'egalite du statut d'un objet du model 
        et de sa valeur obtenue"""
        self.assertEqual(workflow.Manager().curr_statut(self.app, self.user), 
                         self.app.statut)
        
        # Premiere execution ver l'ouverture
        workflow.Manager().execute(self.app, self.user)

        # Verification l'evolution du statut d'un objet du modele est bien 
        # propagee
        statut = workflow.Manager().curr_statut(self.app, self.user)
        self.assertEqual(statut, self.app.statut)


    def test_completion(self):
        """Verification de la completion d'un appel d'offre"""
        # Nouveau
        self.assertEqual(self.app3.statut, 'Nouveau')
        self.assertFalse(workflow.Manager().is_completed(self.app3, self.user))

        # Diffuse
        workflow.Manager().execute(self.app3, self.user)
        self.assertEqual(self.app3.statut, 'Diffuse')
        self.assertFalse(workflow.Manager().is_completed(self.app3, self.user))

        # Analyse
        workflow.Manager().execute(self.app3, self.user)
        self.assertEqual(self.app3.statut, 'Analyse')
        self.assertFalse(workflow.Manager().is_completed(self.app3, self.user))

        # Evalue
        workflow.Manager().execute(self.app3, self.user)
        self.assertEqual(self.app3.statut, 'Evalue')
        self.assertFalse(workflow.Manager().is_completed(self.app3, self.user))

        # Selectionne
        workflow.Manager().execute(self.app3, self.user)
        self.assertEqual(self.app3.statut, 'Selectionne')
        self.assertFalse(workflow.Manager().is_completed(self.app3, self.user))

        # Notifie
        workflow.Manager().execute(self.app3, self.user)
        self.assertEqual(self.app3.statut, 'Notifie')
        self.assertFalse(workflow.Manager().is_completed(self.app3, self.user))

        # Suivie
        workflow.Manager().execute(self.app3, self.user)
        self.assertEqual(self.app3.statut, 'Suivie')

        # Ferme
        workflow.Manager().execute(self.app3, self.user)
        self.assertEqual(self.app3.statut, 'Ferme')
        self.assertTrue(workflow.Manager().is_completed(self.app3, self.user))


    def test_supprimer(self):
        """Verification qu'on ne peut pas supprimer un appel d'offre qui n'est 
        plus Nouveau"""
        self.assertTrue(workflow.Manager().is_reacheable(self.app3, self.user, 
                                                         "Supprimer"))
        while not workflow.Manager().is_completed(self.app3, self.user):
            workflow.Manager().execute(self.app3, self.user)
            self.assertFalse(workflow.Manager().is_reacheable(self.app3, 
                                                              self.user, 
                                                              "Supprimer"))


    def test_appel_link_candidatures_analyse(self):
        """Verification que le passage a l'analyse change les candidatures"""
        # Premiere execution vers la diffusion
        workflow.Manager().execute(self.app, self.user)

        """Test de l'evolution du workflow d'un appel d'offre 
        et de ses candidatures"""
        # Verification qu'on est bien a l'ouverture
        self.assertEqual(self.app.statut, 'Diffuse')

        # Premiere execution vers l'analyse
        workflow.Manager().execute(self.app, self.user)

        # Verification qu'on est bien a la analyse
 	self.assertEqual(self.app.statut, 'Analyse')
        
        # Verification qu'on ne peut pas evoluer a l'etape suivante puisqu'une
        # candidature doit etre analyse
        self.assertFalse(workflow.Manager().is_executable(self.app, self.user))

        # on verifie que toutes les candidatures ont ete changees de statut
        for candidature in Candidature.objects.filter(appel=self.app):
            self.assertFalse(candidature.statut == "Nouveau")
            self.assertTrue(candidature.statut == 'PreIrrecevable' \
                                or candidature.statut == 'PreRecevable')
            # Accepter la candidature en question
            workflow.Manager().execute(candidature, self.user, "Accepter")
            
            # Verification du passage a recevable
            self.assertEqual(candidature.statut, "Recevable")


    def test_appel_link_candidatures_evaluation(self):
        """Verification que le passage a l'evaluation a une influence 
        sur les candidatures"""
        # Passage direct a l'evaluation
        workflow.Manager().execute(self.app, self.user)
        workflow.Manager().execute(self.app, self.user)
        for candidature in Candidature.objects.filter(appel=self.app):
            workflow.Manager().execute(candidature, self.user, "Accepter")
        workflow.Manager().execute(self.app, self.user)
        
        # Verification qu'on est bien a l'evaluation
 	self.assertEqual(self.app.statut, 'Evalue')

        # Verification qu'on ne peut pas evoluer a l'etape suivante puisqu'une
        # candidature doit etre traitee
        self.assertFalse(workflow.Manager().is_executable(self.app, self.user))
        
        # Classement des candidatures
        for candidature in Candidature.objects.filter(appel=self.app):
            workflow.Manager().execute(candidature, self.user, "Classer")

        # Maintenant on devrait pouvoir continuer
        self.assertTrue(workflow.Manager().is_executable(self.app, self.user))


    def test_ajout_candidature_appel(self):
        """Verification de l'ajout de candidature a l'appel"""
        # Verification qu'on ne peut pas ajouter de candidatures lorsque nouveau
        self.assertEqual(self.app3.statut, 'Nouveau')
        self.assertFalse(workflow.Manager().can_add(Candidature, self.user, 
                                                    self.app3))

        # Passage a la diffusion
        workflow.Manager().execute(self.app3, self.user)

        # Verification qu'on peut ajouter des candidature a la diffusion
        self.assertEqual(self.app3.statut, 'Diffuse')
        self.assertTrue(workflow.Manager().can_add(Candidature, self.user, 
                                                   self.app3))

        # Verification qu'on ne peut ajouter de candidatures a toutes les autres
        # etapes du workflow de l'appel
        while not workflow.Manager().is_completed(self.app3, self.user):
            workflow.Manager().execute(self.app3, self.user)
            self.assertFalse(workflow.Manager().can_add(Candidature, self.user, 
                                                        self.app3))
