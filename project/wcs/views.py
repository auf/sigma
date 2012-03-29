# -*- encoding: utf-8 -*-

from auf.django.references import models as ref
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from project.sigma import models as sigma
from project.wcs import WCSGenerator


@permission_required('global.generer_formulaire_wcs')
def formulaire_wcs(request):
    response = HttpResponse(mimetype='application/xml')
    response['Content-Disposition'] = 'attachment; filename=sigma.wcs'
    generator = WCSGenerator(response, u'Squelette SIGMA')
    with generator as g:
        g.add_page(u'Candidat')
        g.add_title(u'Identification')
        g.add_item_field(
            u'Civilité', [u'Monsieur', u'Madame', u'Mademoiselle'],
            varname=u'civilite', in_listing=True,
            show_as_radio=True
        )
        g.add_string_field(
            u'Prénom', varname=u'prenom', required=True,
            in_listing=True
        )
        g.add_string_field(
            u'Nom', varname=u'nom', required=True, in_listing=True
        )
        g.add_string_field(
            u'Nom de jeune fille', varname=u'nom_jeune_fille'
        )
        g.add_item_field(
            u'Nationalité',
            (p.nom for p in ref.Pays.objects.all()),
            in_listing=True
        )
        g.add_date_field(
            u'Date de naissance', varname=u'date_naissance',
            date_in_the_past=True, date_can_be_today=False
        )

        g.add_title(u'Coordonnées')
        g.add_string_field(u'Adresse', varname=u'adresse')
        g.add_string_field(u'Ville', varname=u'ville')
        g.add_string_field(u'Code postal', varname=u'code_postal')
        g.add_string_field(u'Région', varname=u'region')
        g.add_item_field(
            u'Pays de résidence',
            (p.nom for p in ref.Pays.objects.all()),
            varname=u'pays'
        )
        g.add_string_field(
            u'Téléphone fixe', varname=u'telephone_fixe'
        )
        g.add_string_field(
            u'Téléphone portable', varname=u'telephone_portable'
        )
        g.add_email_field(
            u'Adresse électronique', varname=u'courriel'
        )

        g.add_title(u'Situation universitaire')
        g.add_item_field(
            u'Statut du candidat',
            (c[1] for c in sigma.Dossier.CANDIDAT_STATUT_CHOICES),
            varname=u'statut_candidat'
        )
        g.add_string_field(u'Fonction', varname=u'fonction')

        g.add_title(u'Dernier diplôme obtenu')
        g.add_string_field(u'Intitulé', varname=u'diplome')
        g.add_date_field(u"Date d'obtention", varname=u'diplome_date')
        g.add_item_field(
            u"Niveau d'études",
            [u'Niveau 1', u'Niveau 2', u'Niveau 3'],
            varname=u'diplome_niveau'
        )
        g.add_item_field(
            u"Établissement d'obtention si membre de l'AUF",
            ('%s - %s' % (e.pays.nom, e.nom)
             for e in ref.Etablissement.objects \
             .select_related('pays').filter(membre=True)),
            varname=u'diplome_etablissement'
        )
        g.add_string_field(
            u"Nom de l'établissement (si absent de la liste ci-dessus)",
            varname=u'diplome_autre_etablissement'
        )
        g.add_item_field(
            u"Pays de l'établissement (si absent de la liste ci-dessus)",
            (p.nom for p in ref.Pays.objects.all()),
            varname=u'diplome_autre_etablissement_pays'
        )

        g.add_page(u"Origine")
        g.add_title(u"Origine (établissement d'inscription ou d'activité "
                   u"à la date de la candidature)")
        g.add_item_field(
            u"Établissement, si membre de l'AUF",
            ('%s - %s' % (e.pays.nom, e.nom)
             for e in ref.Etablissement.objects \
             .select_related('pays').filter(membre=True)),
            varname=u'origine_etablissement'
        )

        g.add_title(u"Coordonnées de l'établissement d'origine "
                    u"(si absent de la liste ci-dessus)")
        g.add_string_field(u'Nom', varname=u'origine_autre_etablissement')
        g.add_string_field(
            u'Adresse', varname=u'origine_autre_etablissement_adresse'
        )
        g.add_string_field(
            u'Ville', varname=u'origine_autre_etablissement_ville'
        )
        g.add_string_field(
            u'Code postal',
            varname=u'origine_autre_etablissement_code_postal'
        )
        g.add_string_field(
            u'Région', varname=u'origine_autre_etablissement_region'
        )
        g.add_item_field(
            u'Pays', (p.nom for p in ref.Pays.objects.all()),
            varname=u'origine_autre_etablissement_pays'
        )

        g.add_title(u"Responsable institutionnel à l'origine")
        g.add_item_field(
            u'Civilité', [u'Monsieur', u'Madame', u'Mademoiselle'],
            varname=u'origine_responsable_institutionnel_civilite',
            show_as_radio=True
        )
        g.add_string_field(
            u'Prénom',
            varname=u'origine_responsable_institutionnel_prenom'
        )
        g.add_string_field(
            u'Nom',
            varname=u'origine_responsable_institutionnel_nom'
        )
        g.add_email_field(
            u'Courriel',
            varname=u'origine_responsable_institutionnel_courriel'
        )
        g.add_string_field(
            u'Fonction',
            varname=u'origine_responsable_institutionnel_fonction'
        )
        g.add_string_field(
            u'Téléphone',
            varname=u'origine_responsable_institutionnel_telephone'
        )
        g.add_string_field(
            u'Télécopieur',
            varname=u'origine_responsable_institutionnel_fax'
        )

        g.add_title(u"Responsable scientifique à l'origine")
        g.add_item_field(
            u'Civilité', [u'Monsieur', u'Madame', u'Mademoiselle'],
            varname=u'origine_responsable_scientifique_civilite',
            show_as_radio=True
        )
        g.add_string_field(
            u'Prénom',
            varname=u'origine_responsable_scientifique_prenom'
        )
        g.add_string_field(
            u'Nom',
            varname=u'origine_responsable_scientifique_nom'
        )
        g.add_email_field(
            u'Courriel',
            varname=u'origine_responsable_scientifique_courriel'
        )
        g.add_string_field(
            u'Fonction',
            varname=u'origine_responsable_scientifique_fonction'
        )
        g.add_string_field(
            u'Téléphone',
            varname=u'origine_responsable_scientifique_telephone'
        )
        g.add_string_field(
            u'Télécopieur',
            varname=u'origine_responsable_scientifique_fax'
        )
        g.add_string_field(
            u'Faculté / Centre / Département',
            varname=u'origine_responsable_scientifique_faculte'
        )
        g.add_string_field(
            u'Adresse', varname=u'origine_responsable_scientifique_adresse'
        )
        g.add_string_field(
            u'Ville', varname=u'origine_responsable_scientifique_ville'
        )
        g.add_string_field(
            u'Code postal',
            varname=u'origine_responsable_scientifique_code_postal'
        )

        g.add_title(u"Directeur de thèse à l'origine")
        g.add_item_field(
            u'Civilité', [u'Monsieur', u'Madame', u'Mademoiselle'],
            varname=u'origine_directeur_civilite', show_as_radio=True
        )
        g.add_string_field(
            u"Prénom", varname=u'origine_directeur_prenom'
        )
        g.add_string_field(
            u"Nom", varname=u'origine_directeur_nom'
        )
        g.add_email_field(
            u"Adresse électronique", varname=u'origine_directeur_courriel'
        )
        g.add_string_field(
            u"Téléphone", varname=u'origine_directeur_telephone'
        )

        g.add_page(u'Accueil')
        g.add_title(u'Accueil (établissement de destination de la mobilité)')
        g.add_item_field(
            u"Établissement, si membre de l'AUF",
            ('%s - %s' % (e.pays.nom, e.nom)
             for e in ref.Etablissement.objects \
             .select_related('pays').filter(membre=True)),
            varname=u'accueil_etablissement'
        )

        g.add_title(u"Coordonnées de l'établissement d'accueil "
                    u"(si absent de la liste ci-dessus)")
        g.add_string_field(u'Nom', varname=u'accueil_autre_etablissement')
        g.add_string_field(
            u'Adresse', varname=u'accueil_autre_etablissement_adresse'
        )
        g.add_string_field(
            u'Ville', varname=u'accueil_autre_etablissement_ville'
        )
        g.add_string_field(
            u'Code postal',
            varname=u'accueil_autre_etablissement_code_postal'
        )
        g.add_string_field(
            u'Région', varname=u'accueil_autre_etablissement_region'
        )
        g.add_item_field(
            u'Pays', (p.nom for p in ref.Pays.objects.all()),
            varname=u'accueil_autre_etablissement_pays'
        )

        g.add_title(u"Responsable scientifique à l'accueil")
        g.add_item_field(
            u'Civilité', [u'Monsieur', u'Madame', u'Mademoiselle'],
            varname=u'accueil_responsable_scientifique_civilite',
            show_as_radio=True
        )
        g.add_string_field(
            u'Prénom',
            varname=u'accueil_responsable_scientifique_prenom'
        )
        g.add_string_field(
            u'Nom',
            varname=u'accueil_responsable_scientifique_nom'
        )
        g.add_email_field(
            u'Courriel',
            varname=u'accueil_responsable_scientifique_courriel'
        )
        g.add_string_field(
            u'Fonction',
            varname=u'accueil_responsable_scientifique_fonction'
        )
        g.add_string_field(
            u'Téléphone',
            varname=u'accueil_responsable_scientifique_telephone'
        )
        g.add_string_field(
            u'Télécopieur',
            varname=u'accueil_responsable_scientifique_fax'
        )
        g.add_string_field(
            u'Faculté / Centre / Département',
            varname=u'accueil_responsable_scientifique_faculte'
        )
        g.add_string_field(
            u'Adresse', varname=u'accueil_responsable_scientifique_adresse'
        )
        g.add_string_field(
            u'Ville', varname=u'accueil_responsable_scientifique_ville'
        )
        g.add_string_field(
            u'Code postal',
            varname=u'accueil_responsable_scientifique_code_postal'
        )

        g.add_title(u"Directeur de thèse à l'accueil")
        g.add_item_field(
            u'Civilité', [u'Monsieur', u'Madame', u'Mademoiselle'],
            varname=u'accueil_directeur_civilite', show_as_radio=True
        )
        g.add_string_field(
            u"Prénom", varname=u'accueil_directeur_prenom'
        )
        g.add_string_field(
            u"Nom", varname=u'accueil_directeur_nom'
        )
        g.add_email_field(
            u"Adresse électronique", varname=u'accueil_directeur_courriel'
        )
        g.add_string_field(
            u"Téléphone", varname=u'accueil_directeur_telephone'
        )

        g.add_page(u'Mobilité')
        g.add_title(u"Période de mobilité à l'origine")
        g.add_date_field(
            u"Date de début souhaitée", varname=u'date_debut_origine'
        )
        g.add_date_field(
            u"Date de fin souhaitée", varname=u'date_fin_origine'
        )

        g.add_title(u"Période de mobilité à l'accueil")
        g.add_date_field(
            u"Date de début souhaitée", varname=u'date_debut_accueil'
        )
        g.add_date_field(
            u"Date de fin souhaitée", varname=u'date_fin_accueil'
        )

        g.add_title(u"Dossier scientifique")
        g.add_string_field(u"Intitulé de projet", varname=u'intitule_projet')
        g.add_string_field(u"Mots-clefs", varname=u'mots_clefs')

        g.add_title(u'Disciplines')
        g.add_item_field(
            u'Discipline',
            (d.nom for d in ref.Discipline.objects.all()),
            varname=u'discipline'
        )
        g.add_string_field(u'Sous-discipline', varname=u'sous_discipline')

        g.add_title(u'Formation en cours')
        g.add_string_field(u'Diplôme', varname=u'formation_en_cours_diplome')
        g.add_item_field(
            u"Niveau d'études",
            [u'Niveau 1', u'Niveau 2', u'Niveau 3'],
            varname=u'formation_en_cours_niveau'
        )

        g.add_title(u'Diplôme demandé')
        g.add_string_field(u'Diplôme', varname=u'diplome_demande')
        g.add_item_field(
            u"Niveau d'études", [u'Niveau 1', u'Niveau 2', u'Niveau 3'],
            varname=u'diplome_demande_niveau'
        )

        g.add_title(u'Thèse')
        g.add_date_field(
            u"Date de première inscription en thèse",
            varname=u'these_date_inscription'
        )
        g.add_item_field(
            u"Pays de soutenance",
            (p.nom for p in ref.Pays.objects.all()),
            varname=u'these_pays_soutenance'
        )
        g.add_date_field(
            u"Date de soutenance prévue",
            varname=u'these_date_soutenance'
        )
        g.add_item_field(
            u"Type de thèse",
            (x[1] for x in sigma.DossierMobilite.TYPE_THESE_CHOICES),
            varname=u'these_type'
        )

        g.add_title(u'Programme de mission')
        g.add_item_field(
            u"Type d'intervention",
            [u'Type 1', u'Type 2', u'Type 3'],
            varname=u'type_intervention'
        )
        g.add_item_field(
            u"Public visé",
            [u'Public visé 1', u'Public visé 2', u'Public visé 3'],
            varname=u'public_vise'
        )
        g.add_string_field(
            u"Autres publics",
            varname=u'autres_publics'
        )

        g.add_page(u'AUF')
        g.add_title(u"Lien avec l'AUF")
        g.add_text_field(
            u'Description du dernier projet ou programme',
            varname=u'dernier_projet_description'
        )
        g.add_string_field(
            u'Année du dernier projet ou programme',
            varname=u'dernier_projet_annee'
        )
        g.add_item_field(
            u'Catégorie de la dernière bourse',
            [u'Catégorie 1', u'Catégorie 2', u'Catégorie 3'],
            varname=u'derniere_bourse_categorie'
        )
        g.add_string_field(
            u'Année de la dernière bourse',
            varname=u'derniere_bourse_annee'
        )
    return response
