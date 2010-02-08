import datetime

from sigma.www.testcases.sigmatestcase import SigmaTestCase
from sigma.www.models import Appel, Categorie, Candidature, ProjetPoste
from sigma.references.models import \
    Region, Poste, Pays, Bureau, Etablissement, Discipline
from sigma.www import workflow
from sigma.www.workflow.appel import AppelHandler
from sigma.www.workflow.candidature import CandidatureHandler

__all__ = ['TestTaskManager', ]

class TestTaskManager(SigmaTestCase):
    """Verification du bon fonctionnement du taskmanager"""

    def setUp(self):
        SigmaTestCase.setUp(self)
        poste = Poste.objects.filter(id=93)[0]
        cat = Categorie(nom='test', 
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
        cat.save(force_insert=True)

    def test_singleton_status(self):
        self.assertEqual(getattr(workflow.Manager(), '_Manager__instance'),
                         getattr(workflow.Manager(), '_Manager__instance'))

    def test_task_manager(self):
        """Test du bon fonctionnement du taskmanager et du lien avec les handlers"""
        projetposte = ProjetPoste.objects.all()[0]
        app = Appel(nom="Appel d'offre 1",
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
        app.save()
        
        candidat = Candidature(nom = "Leduc",
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
                               date_reception = datetime.date(2009, 03, 26),
                               appel = app,
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
        candidat.save()

        appel_handler = workflow.Manager().get_handler(app, self.user)
        candidature_handler = workflow.Manager().get_handler(candidat, self.user)

        self.assertTrue(len(workflow.Manager().handlers) == 2)
        self.assertTrue(app.__class__ in workflow.Manager().handlers.keys())
        self.assertTrue(candidat.__class__ in workflow.Manager().handlers.keys())
        self.assertEqual(workflow.Manager().get_handler(app, self.user).__class__, AppelHandler)
        self.assertEqual(workflow.Manager().get_handler(candidat, self.user).__class__, CandidatureHandler)
