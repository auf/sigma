# encoding: utf-8

import base64
import json
import os
import re
import urllib2
from urlparse import urljoin

from auf.django.references import models as ref
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from project.sigma.models import \
        Dossier, Candidat, DossierOrigine, DossierMobilite, DossierAccueil, \
        Appel, Piece


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
                settings.WCS_SIGMA_USER,
                settings.WCS_SIGMA_PASS
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

    def parse_pays(self, pays):
        match = self.PAYS_RE.match(pays)
        if match:
            for field in ['code', 'nom']:
                val = match.group(field).strip()
                if val:
                    try:
                        return ref.Pays.objects.get(**{field: val})
                    except ref.Pays.DoesNotExist:
                        pass
        return None

    def parse_etablissement(self, etablissement):
        match = self.ETABLISSEMENT_RE.match(etablissement)
        if match:
            id = match.group('id').strip()
            if id:
                try:
                    return ref.Etablissement.objects.get(id=id)
                except ref.Etablissement.DoesNotExist:
                    pass
            pays = match.group('pays').strip()
            nom = match.group('nom').strip()
            if pays and nom:
                try:
                    return ref.Etablissement.objects.get(
                        nom=nom, pays__nom=pays
                    )
                except ref.Etablissement.DoesNotExist:
                    pass
        return None

    def parse_discipline(self, discipline):
        match = self.DISCIPLINE_RE.match(discipline)
        if match:
            for field in ['id', 'nom']:
                val = match.group(field).strip()
                if val:
                    try:
                        return ref.Discipline.objects.get(**{field: val})
                    except ref.Discipline.DoesNotExist:
                        pass
        return None

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
