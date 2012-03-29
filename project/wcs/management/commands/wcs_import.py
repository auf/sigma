# encoding: utf-8

import base64
import json
import os
import re
import urllib2
from getpass import getpass
from urlparse import urljoin

from auf.django.references import models as ref
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from project.sigma.models import \
        Dossier, Candidat, DossierOrigine, DossierMobilite, DossierAccueil, \
        Appel, Piece, Diplome


class Command(BaseCommand):
    args = "<id de l'appel> <url WCS> [type de formulaire]"
    DOSSIER_URL_RE = re.compile(r'''href=['"]([^?'"]+\.json)['"]''')
    PAYS_RE = re.compile(r'(?P<nom>[^(]*)(\((?P<code>[A-Z]{2}))?')
    ETABLISSEMENT_RE = re.compile(
        r'(?P<pays>[^(]*) - (?P<nom>[^(]*)(\((?P<id>\d+))?'
    )
    DISCIPLINE_RE = re.compile(r'(?P<nom>[^(]*)(\(D(?P<id>\d+))?')

    @transaction.commit_on_success
    def handle(self, *args, **options):
        if len(args) < 2:
            self.stderr.write('Usage: bin/django wcs_import %s\n' % self.args)
            return
        try:
            self.appel = Appel.objects.get(id=int(args[0]))
        except TypeError, Appel.DoesNotExist:
            raise CommandError("L'appel %s n'existe pas" % args[0])
        self.wcs_url = args[1]
        self.wcs_user = raw_input('Utilisateur: ')
        self.wcs_password = getpass('Mot de passe: ')
        if len(args) > 2:
            handler = getattr(self, 'import_' + args[2])
        else:
            handler = self.import_default
        self.data_url = urljoin(self.wcs_url, 'data/')
        for info in self.get_dossiers_json():
            for k in info:
                if info[k] is None:
                    info[k] = u''
            handler(info)

    # Méthodes utilitaires

    def urlopen(self, url):
        request = urllib2.Request(url)
        request.add_header(
            "Authorization",
            "Basic " + base64.encodestring('%s:%s' % (
                self.wcs_user, self.wcs_password
            ))
        )
        return urllib2.urlopen(request)

    def get_dossiers_json(self):
        index = self.urlopen(self.data_url).read()
        for dossier_filename in self.DOSSIER_URL_RE.findall(index):
            dossier_url = urljoin(self.data_url, dossier_filename)
            yield json.loads(self.urlopen(dossier_url).read())

    def parse_civilite(self, civilite):
        if civilite in ('M.', 'M', 'Monsieur'):
            return 'MR'
        elif civilite in ('Mme', 'Madame'):
            return 'MM'
        elif civilite in ('Mademoiselle', 'Mlle'):
            return 'ME'
        else:
            return ''

    def parse_pays(self, pays):
        if not pays:
            return None
        match = self.PAYS_RE.match(pays)
        if match:
            for field in ['code', 'nom']:
                val = match.group(field)
                if val:
                    val = val.strip()
                    try:
                        return ref.Pays.objects.get(**{field: val})
                    except ref.Pays.DoesNotExist:
                        pass
        return None

    def parse_etablissement(self, etablissement):
        if not etablissement:
            return None
        match = self.ETABLISSEMENT_RE.match(etablissement)
        if match:
            id = match.group('id')
            if id:
                id = id.strip()
                try:
                    return ref.Etablissement.objects.get(id=id)
                except ref.Etablissement.DoesNotExist:
                    pass
            pays = match.group('pays')
            nom = match.group('nom')
            if pays and nom:
                pays = pays.strip()
                nom = nom.strip()
                try:
                    return ref.Etablissement.objects.get(
                        nom=nom, pays__nom=pays
                    )
                except ref.Etablissement.DoesNotExist:
                    pass
        return None

    def parse_discipline(self, discipline):
        if not discipline:
            return None
        match = self.DISCIPLINE_RE.match(discipline)
        if match:
            for field in ['id', 'nom']:
                val = match.group(field)
                if val:
                    val = val.strip()
                    try:
                        return ref.Discipline.objects.get(**{field: val})
                    except ref.Discipline.DoesNotExist:
                        pass
        return None

    def parse_choices(self, value, choices):
        if value is None:
            return ''
        for key, label in choices:
            if label == value:
                return key
        return ''

    def import_piece(self, dossier, identifiant, filename):
        basename, ext = os.path.splitext(filename)
        save_filename = str(dossier.id) + '-' + identifiant + ext
        contents = ContentFile(
            self.urlopen(urljoin(self.data_url, filename)).read()
        )
        piece = Piece(
            dossier=dossier,
            identifiant=identifiant
        )
        piece.fichier.save(save_filename, contents)

    # Importeurs

    def import_default(self, info):
        dossier = Dossier.objects.create(
            appel=self.appel,
            candidat_statut=self.parse_choices(
                info.get('statut_candidat'), Dossier.CANDIDAT_STATUT_CHOICES
            ),
            candidat_fonction=info.get('fonction', ''),
            dernier_projet_description=info.get(
                'dernier_projet_description', ''
            ),
            dernier_projet_annee=info.get('dernier_projet_annee', ''),
            derniere_bourse_categorie=info.get(
                'derniere_bourse_categorie', ''
            ),
            derniere_bourse_annee=info.get('derniere_bourse_annee', '')
        )
        Candidat.objects.create(
            dossier=dossier,
            civilite=self.parse_civilite(info.get('civilite')),
            prenom=info['prenom'],
            nom=info['nom'],
            nom_jeune_fille=info.get('nom_jeune_fille', ''),
            nationalite=self.parse_pays(info.get('nationalite')),
            naissance_date=info.get('date_naissance'),
            adresse=info.get('adresse', ''),
            ville=info.get('ville', ''),
            region=info.get('region', ''),
            code_postal=info.get('code_postal', ''),
            pays=self.parse_pays(info.get('pays')),
            telephone=info.get('telephone_fixe', ''),
            telephone_portable=info.get('telephone_portable', ''),
            courriel=info.get('courriel', '')
        )
        Diplome.objects.create(
            dossier=dossier,
            nom=info.get('diplome', ''),
            date=info.get('diplome_date'),
            niveau=info.get('diplome_niveau', ''),
            etablissement=self.parse_etablissement(
                info.get('diplome_etablissement')
            ),
            autre_etablissement_nom=info.get('diplome_autre_etablissement'),
            autre_etablissement_pays=self.parse_pays(
                info.get('diplome_autre_etablissement_pays')
            )
        )
        DossierOrigine.objects.create(
            dossier=dossier,
            etablissement=self.parse_etablissement(
                info.get('origine_etablissement')
            ),
            autre_etablissement_nom=info.get(
                'origine_autre_etablissement', ''
            ),
            autre_etablissement_adresse=info.get(
                'origine_autre_etablissement_adresse', ''
            ),
            autre_etablissement_ville=info.get(
                'origine_autre_etablissement_ville', ''
            ),
            autre_etablissement_code_postal=info.get(
                'origine_autre_etablissement_code_postal', ''
            ),
            autre_etablissement_region=info.get(
                'origine_autre_etablissement_region', ''
            ),
            autre_etablissement_pays=self.parse_pays(
                info.get('origine_autre_etablissement_pays')
            ),
            resp_inst_civilite=self.parse_civilite(
                info.get('origine_responsable_institutionnel_civilite')
            ),
            resp_inst_nom=info.get(
                'origine_responsable_institutionnel_nom', ''
            ),
            resp_inst_prenom=info.get(
                'origine_responsable_institutionnel_prenom', ''
            ),
            resp_inst_fonction=info.get(
                'origine_responsable_institutionnel_fonction', ''
            ),
            resp_inst_courriel=info.get(
                'origine_responsable_institutionnel_courriel', ''
            ),
            resp_inst_telephone=info.get(
                'origine_responsable_institutionnel_telephone', ''
            ),
            resp_inst_fax=info.get(
                'origine_responsable_institutionnel_fax', ''
            ),
            resp_sc_civilite=self.parse_civilite(
                info.get('origine_responsable_scientifique_civilite', '')
            ),
            resp_sc_prenom=info.get(
                'origine_responsable_scientifique_prenom', ''
            ),
            resp_sc_nom=info.get(
                'origine_responsable_scientifique_nom', ''
            ),
            resp_sc_fonction=info.get(
                'origine_responsable_scientifique_fonction', ''
            ),
            resp_sc_courriel=info.get(
                'origine_responsable_scientifique_courriel', ''
            ),
            resp_sc_telephone=info.get(
                'origine_responsable_scientifique_telephone', ''
            ),
            resp_sc_fax=info.get(
                'origine_responsable_scientifique_fax', ''
            ),
            faculte_nom=info.get(
                'origine_responsable_scientifique_faculte', ''
            ),
            faculte_adresse=info.get(
                'origine_responsable_scientifique_adresse', ''
            ),
            faculte_ville=info.get(
                'origine_responsable_scientifique_ville', ''
            ),
            faculte_code_postal=info.get(
                'origine_responsable_scientifique_code_postal', ''
            ),
            dir_civilite=self.parse_civilite(
                info.get('origine_directeur_civilite')
            ),
            dir_prenom=info.get('origine_directeur_prenom', ''),
            dir_nom=info.get('origine_directeur_nom', ''),
            dir_courriel=info.get('origine_directeur_courriel', ''),
            dir_telephone=info.get('origine_directeur_telephone', '')
        )
        DossierAccueil.objects.create(
            dossier=dossier,
            etablissement=self.parse_etablissement(
                info.get('accueil_etablissement')
            ),
            autre_etablissement_nom=info.get(
                'accueil_autre_etablissement', ''
            ),
            autre_etablissement_adresse=info.get(
                'accueil_autre_etablissement_adresse', ''
            ),
            autre_etablissement_ville=info.get(
                'accueil_autre_etablissement_ville', ''
            ),
            autre_etablissement_code_postal=info.get(
                'accueil_autre_etablissement_code_postal', ''
            ),
            autre_etablissement_region=info.get(
                'accueil_autre_etablissement_region', ''
            ),
            autre_etablissement_pays=self.parse_pays(
                info.get('accueil_autre_etablissement_pays')
            ),
            resp_sc_civilite=self.parse_civilite(
                info.get('accueil_responsable_scientifique_civilite', '')
            ),
            resp_sc_prenom=info.get(
                'accueil_responsable_scientifique_prenom', ''
            ),
            resp_sc_nom=info.get(
                'accueil_responsable_scientifique_nom', ''
            ),
            resp_sc_fonction=info.get(
                'accueil_responsable_scientifique_fonction', ''
            ),
            resp_sc_courriel=info.get(
                'accueil_responsable_scientifique_courriel', ''
            ),
            resp_sc_telephone=info.get(
                'accueil_responsable_scientifique_telephone', ''
            ),
            resp_sc_fax=info.get(
                'accueil_responsable_scientifique_fax', ''
            ),
            faculte_nom=info.get(
                'accueil_responsable_scientifique_faculte', ''
            ),
            faculte_adresse=info.get(
                'accueil_responsable_scientifique_adresse', ''
            ),
            faculte_ville=info.get(
                'accueil_responsable_scientifique_ville', ''
            ),
            faculte_code_postal=info.get(
                'accueil_responsable_scientifique_code_postal', ''
            ),
            dir_civilite=self.parse_civilite(
                info.get('accueil_directeur_civilite')
            ),
            dir_prenom=info.get('accueil_directeur_prenom', ''),
            dir_nom=info.get('accueil_directeur_nom', ''),
            dir_courriel=info.get('accueil_directeur_courriel', ''),
            dir_telephone=info.get('accueil_directeur_telephone', '')
        )
        DossierMobilite.objects.create(
            dossier=dossier,
            date_debut_origine=info.get('date_debut_origine'),
            date_fin_origine=info.get('date_fin_origine'),
            date_debut_accueil=info.get('date_debut_accueil'),
            date_fin_accueil=info.get('date_fin_accueil'),
            intitule_projet=info.get('intitule_projet', ''),
            mots_clefs=info.get('mots_clefs', ''),
            discipline=self.parse_discipline(info.get('discipline')),
            sous_discipline=info.get('sous_discipline', ''),
            formation_en_cours_diplome=info.get(
                'formation_en_cours_diplome', ''
            ),
            formation_en_cours_niveau=info.get(
                'formation_en_cours_niveau', ''
            ),
            diplome_demande_nom=info.get('diplome_demande', ''),
            diplome_demande_niveau=info.get('diplome_demande_niveau', ''),
            these_date_inscription=info.get('these_date_inscription', ''),
            these_soutenance_pays=self.parse_pays(
                info.get('these_pays_soutenance', '')
            ),
            these_soutenance_date=info.get('these_date_soutenance', ''),
            these_type=self.parse_choices(
                info.get('these_type'), DossierMobilite.TYPE_THESE_CHOICES
            ),
            type_intervention=info.get('type_intervention', ''),
            public_vise=info.get('public_vise', ''),
            autres_publics=info.get('autres_publics', '')
        )

    def import_stage_beco_2012(self, info):
        dossier = Dossier(
            appel=self.appel,
            derniere_bourse_categorie=info[
                'si_oui_precisez_le_type_de_bourse_obtenue'
            ],
            derniere_bourse_annee=info['precisez_l_annee']
        )
        dossier.save()
        candidat = Candidat(
            dossier=dossier,
            civilite=self.parse_civilite(info['civilite']),
            nom=info['nom'],
            prenom=info['prenom'],
            nationalite=self.parse_pays(info['pays_de_nationalite']),
            naissance_date=info['date_de_naissance'],
            adresse=info['adresse_de_correspondance_adresse_postale'],
            ville=info['municipalite_ville'],
            region=info['departement'],
            code_postal=info['code_postal'],
            pays=self.parse_pays(info['pays']),
            telephone=info['telephone_personnel_fixe_ou_gsm'],
            courriel=info['adresse_electronique'],
        )
        candidat.save()
        origine = DossierOrigine(
            dossier=dossier,
            etablissement=self.parse_etablissement(
                info['etablissement_d_origine_membre_de_l_auf']
            ),
            faculte_nom='%s, %s' % (info['faculte'], info['departement']),
        )
        origine.save()
        mobilite = DossierMobilite(
            dossier=dossier,
            formation_en_cours_niveau=info['annee_d_etude_en_cours'],
            formation_en_cours_diplome=info['diplome_en_cours_d_obtention'],
            discipline=self.parse_discipline(info['discipline']),
            date_debut_accueil=info['date_de_debut'],
            date_fin_accueil=info['date_de_fin'],
        )
        mobilite.save()
        accueil = DossierAccueil(
            dossier=dossier,
            autre_etablissement_nom=info['nom_2'],
            autre_etablissement_adresse=info['adresse_adresse_postale'],
            autre_etablissement_ville=info['municipalite_ville_2'],
            autre_etablissement_region=info['region_province_etat'],
            autre_etablissement_code_postal=info['code_postal_2'],
            autre_etablissement_pays=self.parse_pays(info['pays_2']),
            resp_sc_civilite=self.parse_civilite(
                info['civilite_du_responsable']
            ),
            resp_sc_nom=info['nom_du_responsable'],
            resp_sc_prenom=info['prenom_du_responsable'],
            resp_sc_fonction=info['fonction'],
            resp_sc_telephone=info['telephone_2'],
            resp_sc_courriel=info['adresse_electronique_du_responsable'],
            faculte_nom=info['unite_administrative'],
            faculte_adresse=info['adresse'],
            faculte_ville=info['municipalite_ville_3'],
            faculte_code_postal=info['code_postal_3']
        )
        accueil.save()
        self.import_piece(
            dossier, u'descriptif-du-projet',
            info['descriptif_detaille_du_projet_professionnel_integre_dans_'
                 'l_activite_les_projets_de_la_structure_d_accueil']
        )
        self.import_piece(
            dossier, u'dossier-de-scolarite-universitaire',
            info['copie_du_dossier_de_scolarite_universitaire']
        )
        self.import_piece(
            dossier, u"attestation-dinscription",
            info['attestation_d_inscription_a_l_universite_pour_'
                 'l_annee_en_cours']
        )
        self.import_piece(
            dossier, u"attestation-daccord",
            info['attestation_d_accord_motive_de_l_etablissement_d_origine_'
                 'delivree_signee_et_cachetee_par_le_responsable_scientifique_'
                 'direct_et_par_le_doyen']
        )
        self.import_piece(
            dossier, u"attestation-daccueil",
            info['attestation_d_accueil_du_responsable_du_projet_de_stage_'
                 'dans_l_etablissement_d_accueil']
        )
        self.import_piece(
            dossier, u"preuve-de-competence-linguistique",
            info['le_document_faisant_preuve_de_competence_linguistique_'
                 'en_francais_le_cas_echeant']
        )
