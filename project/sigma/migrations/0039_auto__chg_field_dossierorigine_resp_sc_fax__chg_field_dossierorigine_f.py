# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        if not db.dry_run:
            for column in [
                'resp_sc_fax', 'faculte_adresse', 'resp_inst_courriel',
                'resp_sc_prenom', 'resp_inst_fonction', 'resp_sc_courriel',
                'autre_etablissement_ville', 'resp_inst_telephone',
                'autre_etablissement_nom', 'dir_civilite',
                'faculte_code_postal', 'faculte_nom', 'resp_sc_civilite',
                'resp_inst_nom', 'autre_etablissement_adresse',
                'autre_etablissement_region', 'resp_inst_fax',
                'faculte_ville', 'resp_inst_civilite', 'resp_inst_prenom',
                'resp_sc_telephone', 'autre_etablissement_code_postal',
                'dir_courriel', 'dir_telephone', 'dir_prenom', 'dir_nom',
                'resp_sc_fonction', 'resp_sc_nom'
            ]:
                orm.DossierOrigine.objects \
                        .filter(**{column: None}).update(**{column: ''})
                if not column.startswith('resp_inst_'):
                    orm.DossierAccueil.objects \
                            .filter(**{column: None}).update(**{column: ''})

            for column in ['attribut', 'valeur']:
                orm.AttributWCS.objects \
                        .filter(**{column: None}).update(**{column: ''})

            for column in [
                'intitule_projet', 'mots_clefs', 'these_type',
                'diplome_demande_nom', 'sous_discipline', 'autres_publics',
                'formation_en_cours_diplome'
            ]:
                orm.DossierMobilite.objects \
                        .filter(**{column: None}).update(**{column: ''})

            for column in ['commentaire', 'courriel']:
                orm.Expert.objects \
                        .filter(**{column: None}).update(**{column: ''})

            for column in [
                'candidat_statut', 'candidat_fonction', 'dernier_projet_annee',
                'opportunite_regionale', 'derniere_bourse_annee',
                'dernier_projet_description'
            ]:
                orm.Dossier.objects \
                        .filter(**{column: None}).update(**{column: ''})

            for column in ['nom', 'autre_etablissement_nom']:
                orm.Diplome.objects \
                        .filter(**{column: None}).update(**{column: ''})

            for column in ['nom']:
                orm.Piece.objects \
                        .filter(**{column: None}).update(**{column: ''})

            for column in [
                'code_postal', 'ville', 'telephone_portable', 'region',
                'civilite', 'telephone', 'nom_jeune_fille', 'courriel',
                'adresse_complement', 'adresse'
            ]:
                orm.Candidat.objects \
                        .filter(**{column: None}).update(**{column: ''})

            for column in ['formulaire_wcs', 'periode', 'bareme']:
                orm.Appel.objects \
                        .filter(**{column: None}).update(**{column: ''})

        # Changing field 'DossierOrigine.resp_sc_fax'
        db.alter_column('sigma_dossierorigine', 'resp_sc_fax', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.faculte_adresse'
        db.alter_column('sigma_dossierorigine', 'faculte_adresse', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_inst_courriel'
        db.alter_column('sigma_dossierorigine', 'resp_inst_courriel', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_sc_prenom'
        db.alter_column('sigma_dossierorigine', 'resp_sc_prenom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_inst_fonction'
        db.alter_column('sigma_dossierorigine', 'resp_inst_fonction', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_sc_courriel'
        db.alter_column('sigma_dossierorigine', 'resp_sc_courriel', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.autre_etablissement_ville'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_ville', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_inst_telephone'
        db.alter_column('sigma_dossierorigine', 'resp_inst_telephone', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.autre_etablissement_nom'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),

        # Changing field 'DossierOrigine.dir_civilite'
        db.alter_column('sigma_dossierorigine', 'dir_civilite', self.gf('django.db.models.fields.CharField')(default='', max_length=2))

        # Changing field 'DossierOrigine.faculte_code_postal'
        db.alter_column('sigma_dossierorigine', 'faculte_code_postal', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.faculte_nom'
        db.alter_column('sigma_dossierorigine', 'faculte_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_sc_civilite'
        db.alter_column('sigma_dossierorigine', 'resp_sc_civilite', self.gf('django.db.models.fields.CharField')(default='', max_length=2))

        # Changing field 'DossierOrigine.resp_inst_nom'
        db.alter_column('sigma_dossierorigine', 'resp_inst_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.autre_etablissement_adresse'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_adresse', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.autre_etablissement_region'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_region', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_inst_fax'
        db.alter_column('sigma_dossierorigine', 'resp_inst_fax', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.faculte_ville'
        db.alter_column('sigma_dossierorigine', 'faculte_ville', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_inst_civilite'
        db.alter_column('sigma_dossierorigine', 'resp_inst_civilite', self.gf('django.db.models.fields.CharField')(default='', max_length=2))

        # Changing field 'DossierOrigine.resp_inst_prenom'
        db.alter_column('sigma_dossierorigine', 'resp_inst_prenom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_sc_telephone'
        db.alter_column('sigma_dossierorigine', 'resp_sc_telephone', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.autre_etablissement_code_postal'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_code_postal', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.dir_courriel'
        db.alter_column('sigma_dossierorigine', 'dir_courriel', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.dir_telephone'
        db.alter_column('sigma_dossierorigine', 'dir_telephone', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.dir_prenom'
        db.alter_column('sigma_dossierorigine', 'dir_prenom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.dir_nom'
        db.alter_column('sigma_dossierorigine', 'dir_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_sc_fonction'
        db.alter_column('sigma_dossierorigine', 'resp_sc_fonction', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierOrigine.resp_sc_nom'
        db.alter_column('sigma_dossierorigine', 'resp_sc_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'AttributWCS.attribut'
        db.alter_column('sigma_attributwcs', 'attribut', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'AttributWCS.valeur'
        db.alter_column('sigma_attributwcs', 'valeur', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'DossierMobilite.intitule_projet'
        db.alter_column('sigma_dossiermobilite', 'intitule_projet', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierMobilite.mots_clefs'
        db.alter_column('sigma_dossiermobilite', 'mots_clefs', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierMobilite.these_type'
        db.alter_column('sigma_dossiermobilite', 'these_type', self.gf('django.db.models.fields.CharField')(default='', max_length=2))

        # Changing field 'DossierMobilite.diplome_demande_nom'
        db.alter_column('sigma_dossiermobilite', 'diplome_demande_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierMobilite.sous_discipline'
        db.alter_column('sigma_dossiermobilite', 'sous_discipline', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierMobilite.autres_publics'
        db.alter_column('sigma_dossiermobilite', 'autres_publics', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierMobilite.formation_en_cours_diplome'
        db.alter_column('sigma_dossiermobilite', 'formation_en_cours_diplome', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Expert.commentaire'
        db.alter_column('sigma_expert', 'commentaire', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Expert.courriel'
        db.alter_column('sigma_expert', 'courriel', self.gf('django.db.models.fields.EmailField')(default='', max_length=75))

        # Changing field 'Dossier.candidat_statut'
        db.alter_column('sigma_dossier', 'candidat_statut', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Dossier.candidat_fonction'
        db.alter_column('sigma_dossier', 'candidat_fonction', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Dossier.dernier_projet_annee'
        db.alter_column('sigma_dossier', 'dernier_projet_annee', self.gf('django.db.models.fields.CharField')(default='', max_length=4))

        # Changing field 'Dossier.opportunite_regionale'
        db.alter_column('sigma_dossier', 'opportunite_regionale', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Dossier.derniere_bourse_annee'
        db.alter_column('sigma_dossier', 'derniere_bourse_annee', self.gf('django.db.models.fields.CharField')(default='', max_length=4))

        # Changing field 'Dossier.dernier_projet_description'
        db.alter_column('sigma_dossier', 'dernier_projet_description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Diplome.nom'
        db.alter_column('sigma_diplome', 'nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Diplome.autre_etablissement_nom'
        db.alter_column('sigma_diplome', 'autre_etablissement_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Piece.nom'
        db.alter_column('sigma_piece', 'nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Candidat.code_postal'
        db.alter_column('sigma_candidat', 'code_postal', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Candidat.ville'
        db.alter_column('sigma_candidat', 'ville', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Candidat.telephone_portable'
        db.alter_column('sigma_candidat', 'telephone_portable', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Candidat.region'
        db.alter_column('sigma_candidat', 'region', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Candidat.civilite'
        db.alter_column('sigma_candidat', 'civilite', self.gf('django.db.models.fields.CharField')(default='', max_length=2))

        # Changing field 'Candidat.telephone'
        db.alter_column('sigma_candidat', 'telephone', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Candidat.nom_jeune_fille'
        db.alter_column('sigma_candidat', 'nom_jeune_fille', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Candidat.courriel'
        db.alter_column('sigma_candidat', 'courriel', self.gf('django.db.models.fields.EmailField')(default='', max_length=255))

        # Changing field 'Candidat.adresse_complement'
        db.alter_column('sigma_candidat', 'adresse_complement', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Candidat.adresse'
        db.alter_column('sigma_candidat', 'adresse', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.resp_sc_fax'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_fax', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.faculte_adresse'
        db.alter_column('sigma_dossieraccueil', 'faculte_adresse', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.resp_sc_prenom'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_prenom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.resp_sc_courriel'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_courriel', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.autre_etablissement_ville'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_ville', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.autre_etablissement_nom'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.dir_civilite'
        db.alter_column('sigma_dossieraccueil', 'dir_civilite', self.gf('django.db.models.fields.CharField')(default='', max_length=2))

        # Changing field 'DossierAccueil.faculte_code_postal'
        db.alter_column('sigma_dossieraccueil', 'faculte_code_postal', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.faculte_nom'
        db.alter_column('sigma_dossieraccueil', 'faculte_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.resp_sc_civilite'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_civilite', self.gf('django.db.models.fields.CharField')(default='', max_length=2))

        # Changing field 'DossierAccueil.dir_courriel'
        db.alter_column('sigma_dossieraccueil', 'dir_courriel', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.autre_etablissement_region'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_region', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.faculte_ville'
        db.alter_column('sigma_dossieraccueil', 'faculte_ville', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.resp_sc_telephone'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_telephone', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.autre_etablissement_code_postal'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_code_postal', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.autre_etablissement_adresse'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_adresse', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.dir_telephone'
        db.alter_column('sigma_dossieraccueil', 'dir_telephone', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.dir_nom'
        db.alter_column('sigma_dossieraccueil', 'dir_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.dir_prenom'
        db.alter_column('sigma_dossieraccueil', 'dir_prenom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.resp_sc_fonction'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_fonction', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'DossierAccueil.resp_sc_nom'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_nom', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Appel.formulaire_wcs'
        db.alter_column('sigma_appel', 'formulaire_wcs', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Appel.periode'
        db.alter_column('sigma_appel', 'periode', self.gf('django.db.models.fields.CharField')(default='', max_length=32))

        # Changing field 'Appel.bareme'
        db.alter_column('sigma_appel', 'bareme', self.gf('django.db.models.fields.CharField')(default='', max_length=32))


    def backwards(self, orm):
        
        # Changing field 'DossierOrigine.resp_sc_fax'
        db.alter_column('sigma_dossierorigine', 'resp_sc_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.faculte_adresse'
        db.alter_column('sigma_dossierorigine', 'faculte_adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_inst_courriel'
        db.alter_column('sigma_dossierorigine', 'resp_inst_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_sc_prenom'
        db.alter_column('sigma_dossierorigine', 'resp_sc_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_inst_fonction'
        db.alter_column('sigma_dossierorigine', 'resp_inst_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_sc_courriel'
        db.alter_column('sigma_dossierorigine', 'resp_sc_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.autre_etablissement_ville'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_inst_telephone'
        db.alter_column('sigma_dossierorigine', 'resp_inst_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.autre_etablissement_nom'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.dir_civilite'
        db.alter_column('sigma_dossierorigine', 'dir_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'DossierOrigine.faculte_code_postal'
        db.alter_column('sigma_dossierorigine', 'faculte_code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.faculte_nom'
        db.alter_column('sigma_dossierorigine', 'faculte_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_sc_civilite'
        db.alter_column('sigma_dossierorigine', 'resp_sc_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'DossierOrigine.resp_inst_nom'
        db.alter_column('sigma_dossierorigine', 'resp_inst_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.autre_etablissement_adresse'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.autre_etablissement_region'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_inst_fax'
        db.alter_column('sigma_dossierorigine', 'resp_inst_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.faculte_ville'
        db.alter_column('sigma_dossierorigine', 'faculte_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_inst_civilite'
        db.alter_column('sigma_dossierorigine', 'resp_inst_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'DossierOrigine.resp_inst_prenom'
        db.alter_column('sigma_dossierorigine', 'resp_inst_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_sc_telephone'
        db.alter_column('sigma_dossierorigine', 'resp_sc_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.autre_etablissement_code_postal'
        db.alter_column('sigma_dossierorigine', 'autre_etablissement_code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.dir_courriel'
        db.alter_column('sigma_dossierorigine', 'dir_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.dir_telephone'
        db.alter_column('sigma_dossierorigine', 'dir_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.dir_prenom'
        db.alter_column('sigma_dossierorigine', 'dir_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.dir_nom'
        db.alter_column('sigma_dossierorigine', 'dir_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_sc_fonction'
        db.alter_column('sigma_dossierorigine', 'resp_sc_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierOrigine.resp_sc_nom'
        db.alter_column('sigma_dossierorigine', 'resp_sc_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'AttributWCS.attribut'
        db.alter_column('sigma_attributwcs', 'attribut', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'AttributWCS.valeur'
        db.alter_column('sigma_attributwcs', 'valeur', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'DossierMobilite.intitule_projet'
        db.alter_column('sigma_dossiermobilite', 'intitule_projet', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierMobilite.mots_clefs'
        db.alter_column('sigma_dossiermobilite', 'mots_clefs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierMobilite.these_type'
        db.alter_column('sigma_dossiermobilite', 'these_type', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'DossierMobilite.diplome_demande_nom'
        db.alter_column('sigma_dossiermobilite', 'diplome_demande_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierMobilite.sous_discipline'
        db.alter_column('sigma_dossiermobilite', 'sous_discipline', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierMobilite.autres_publics'
        db.alter_column('sigma_dossiermobilite', 'autres_publics', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierMobilite.formation_en_cours_diplome'
        db.alter_column('sigma_dossiermobilite', 'formation_en_cours_diplome', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Expert.commentaire'
        db.alter_column('sigma_expert', 'commentaire', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Expert.courriel'
        db.alter_column('sigma_expert', 'courriel', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

        # Changing field 'Dossier.candidat_statut'
        db.alter_column('sigma_dossier', 'candidat_statut', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Dossier.candidat_fonction'
        db.alter_column('sigma_dossier', 'candidat_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Dossier.dernier_projet_annee'
        db.alter_column('sigma_dossier', 'dernier_projet_annee', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))

        # Changing field 'Dossier.opportunite_regionale'
        db.alter_column('sigma_dossier', 'opportunite_regionale', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Dossier.derniere_bourse_annee'
        db.alter_column('sigma_dossier', 'derniere_bourse_annee', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))

        # Changing field 'Dossier.dernier_projet_description'
        db.alter_column('sigma_dossier', 'dernier_projet_description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Diplome.nom'
        db.alter_column('sigma_diplome', 'nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Diplome.autre_etablissement_nom'
        db.alter_column('sigma_diplome', 'autre_etablissement_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Piece.nom'
        db.alter_column('sigma_piece', 'nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Candidat.code_postal'
        db.alter_column('sigma_candidat', 'code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Candidat.ville'
        db.alter_column('sigma_candidat', 'ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Candidat.telephone_portable'
        db.alter_column('sigma_candidat', 'telephone_portable', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Candidat.region'
        db.alter_column('sigma_candidat', 'region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Candidat.civilite'
        db.alter_column('sigma_candidat', 'civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'Candidat.telephone'
        db.alter_column('sigma_candidat', 'telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Candidat.nom_jeune_fille'
        db.alter_column('sigma_candidat', 'nom_jeune_fille', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Candidat.courriel'
        db.alter_column('sigma_candidat', 'courriel', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True))

        # Changing field 'Candidat.adresse_complement'
        db.alter_column('sigma_candidat', 'adresse_complement', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Candidat.adresse'
        db.alter_column('sigma_candidat', 'adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.resp_sc_fax'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.faculte_adresse'
        db.alter_column('sigma_dossieraccueil', 'faculte_adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.resp_sc_prenom'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.resp_sc_courriel'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.autre_etablissement_ville'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.autre_etablissement_nom'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.dir_civilite'
        db.alter_column('sigma_dossieraccueil', 'dir_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'DossierAccueil.faculte_code_postal'
        db.alter_column('sigma_dossieraccueil', 'faculte_code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.faculte_nom'
        db.alter_column('sigma_dossieraccueil', 'faculte_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.resp_sc_civilite'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'DossierAccueil.dir_courriel'
        db.alter_column('sigma_dossieraccueil', 'dir_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.autre_etablissement_region'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.faculte_ville'
        db.alter_column('sigma_dossieraccueil', 'faculte_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.resp_sc_telephone'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.autre_etablissement_code_postal'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.autre_etablissement_adresse'
        db.alter_column('sigma_dossieraccueil', 'autre_etablissement_adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.dir_telephone'
        db.alter_column('sigma_dossieraccueil', 'dir_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.dir_nom'
        db.alter_column('sigma_dossieraccueil', 'dir_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.dir_prenom'
        db.alter_column('sigma_dossieraccueil', 'dir_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.resp_sc_fonction'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'DossierAccueil.resp_sc_nom'
        db.alter_column('sigma_dossieraccueil', 'resp_sc_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Appel.formulaire_wcs'
        db.alter_column('sigma_appel', 'formulaire_wcs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Appel.periode'
        db.alter_column('sigma_appel', 'periode', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Appel.bareme'
        db.alter_column('sigma_appel', 'bareme', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'coda.projetposte': {
            'Meta': {'managed': 'False', 'object_name': 'ProjetPoste', '_ormbases': ['managedcoda.ProjetPoste'], 'proxy': 'True'}
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'managedcoda.projetposte': {
            'Meta': {'object_name': 'ProjetPoste', 'db_table': "'coda_projetposte'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '72', 'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'timestamp': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'managedref.bureau': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Bureau', 'db_table': "u'ref_bureau'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Implantation']", 'db_column': "'implantation'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Region']", 'db_column': "'region'"})
        },
        'managedref.discipline': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Discipline', 'db_table': "u'ref_discipline'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'managedref.etablissement': {
            'Meta': {'ordering': "['pays__nom', 'nom']", 'object_name': 'Etablissement', 'db_table': "u'ref_etablissement'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cedex': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'db_column': "'implantation'", 'to': "orm['managedref.Implantation']"}),
            'membre': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'membre_adhesion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to_field': "'code'", 'db_column': "'pays'", 'to': "orm['managedref.Pays']"}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'qualite': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'db_column': "'region'", 'to': "orm['managedref.Region']"}),
            'responsable_genre': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'responsable_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'responsable_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'statut': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'managedref.implantation': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Implantation', 'db_table': "u'ref_implantation'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'adresse_physique_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'adresse_physique_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_physique'", 'to_field': "'code'", 'db_column': "'adresse_physique_pays'", 'to': "orm['managedref.Pays']"}),
            'adresse_physique_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'adresse_postale_boite_postale': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'adresse_postale_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_postale'", 'to_field': "'code'", 'db_column': "'adresse_postale_pays'", 'to': "orm['managedref.Pays']"}),
            'adresse_postale_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bureau_rattachement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Implantation']", 'db_column': "'bureau_rattachement'"}),
            'code_meteo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'courriel_interne': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'date_extension': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fermeture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_inauguration': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_ouverture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fax_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fuseau_horaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hebergement_convention': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'hebergement_convention_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hebergement_etablissement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modif_date': ('django.db.models.fields.DateField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Region']", 'db_column': "'region'"}),
            'remarque': ('django.db.models.fields.TextField', [], {}),
            'responsable_implantation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'statut': ('django.db.models.fields.IntegerField', [], {}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'managedref.pays': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Pays', 'db_table': "u'ref_pays'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'code_bureau': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Bureau']", 'to_field': "'code'", 'null': 'True', 'db_column': "'code_bureau'", 'blank': 'True'}),
            'code_iso3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'developpement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monnaie': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nord_sud': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Region']", 'db_column': "'region'"})
        },
        'managedref.region': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Region', 'db_table': "u'ref_region'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation_bureau': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gere_region'", 'null': 'True', 'db_column': "'implantation_bureau'", 'to': "orm['managedref.Implantation']"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'references.bureau': {
            'Meta': {'managed': 'False', 'ordering': "['nom']", 'object_name': 'Bureau', 'db_table': "u'ref_bureau'", '_ormbases': ['managedref.Bureau'], 'proxy': 'True'}
        },
        'references.discipline': {
            'Meta': {'managed': 'False', 'ordering': "['nom']", 'object_name': 'Discipline', 'db_table': "u'ref_discipline'", '_ormbases': ['managedref.Discipline'], 'proxy': 'True'}
        },
        'references.etablissement': {
            'Meta': {'managed': 'False', 'ordering': "['pays__nom', 'nom']", 'object_name': 'Etablissement', 'db_table': "u'ref_etablissement'", '_ormbases': ['managedref.Etablissement'], 'proxy': 'True'}
        },
        'references.implantation': {
            'Meta': {'managed': 'False', 'ordering': "['nom']", 'object_name': 'Implantation', 'db_table': "u'ref_implantation'", '_ormbases': ['managedref.Implantation'], 'proxy': 'True'}
        },
        'references.pays': {
            'Meta': {'managed': 'False', 'ordering': "['nom']", 'object_name': 'Pays', 'db_table': "u'ref_pays'", '_ormbases': ['managedref.Pays'], 'proxy': 'True'}
        },
        'references.region': {
            'Meta': {'managed': 'False', 'ordering': "['nom']", 'object_name': 'Region', 'db_table': "u'ref_region'", '_ormbases': ['managedref.Region'], 'proxy': 'True'}
        },
        'sigma.appel': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Appel'},
            'appel_en_ligne': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bareme': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'code_budgetaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedcoda.ProjetPoste']"}),
            'conformites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sigma.TypeConformite']", 'null': 'True', 'blank': 'True'}),
            'date_debut_appel': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_debut_mobilite': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin_appel': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin_mobilite': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'formulaire_wcs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'montant_allocation_unique': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'montant_mensuel_accueil_nord': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'montant_mensuel_accueil_sud': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'montant_mensuel_origine_nord': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'montant_mensuel_origine_sud': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'montant_perdiem_nord': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'montant_perdiem_sud': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'periode': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'prime_installation_nord': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prime_installation_sud': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Region']"}),
            'types_piece': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sigma.TypePiece']", 'null': 'True', 'blank': 'True'})
        },
        'sigma.attributwcs': {
            'Meta': {'object_name': 'AttributWCS'},
            'attribut': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributs_wcs'", 'to': "orm['sigma.Dossier']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valeur': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'sigma.candidat': {
            'Meta': {'object_name': 'Candidat'},
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_complement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'date_creation': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'candidat'", 'unique': 'True', 'to': "orm['sigma.Dossier']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naissance_date': ('django.db.models.fields.DateField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nationalite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Pays']", 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_jeune_fille': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pays'", 'null': 'True', 'to': "orm['managedref.Pays']"}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone_portable': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'sigma.categoriebourse': {
            'Meta': {'object_name': 'CategorieBourse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sigma.commentaire': {
            'Meta': {'object_name': 'Commentaire'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'texte': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'sigma.conformite': {
            'Meta': {'object_name': 'Conformite'},
            'conforme': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.Dossier']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.TypeConformite']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'sigma.diplome': {
            'Meta': {'object_name': 'Diplome'},
            'autre_etablissement_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'etablissement_pays'", 'null': 'True', 'to': "orm['managedref.Pays']"}),
            'date': ('django.db.models.fields.DateField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.Dossier']"}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Etablissement']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niveau': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'sigma.dossier': {
            'Meta': {'ordering': "['appel__nom', 'candidat__nom', 'candidat__prenom']", 'object_name': 'Dossier'},
            'annotations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sigma.Commentaire']", 'null': 'True', 'blank': 'True'}),
            'appel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appel'", 'to': "orm['sigma.Appel']"}),
            'bureau_rattachement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Bureau']", 'null': 'True', 'blank': 'True'}),
            'candidat_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'candidat_statut': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dernier_projet_annee': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'dernier_projet_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'derniere_bourse_annee': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'derniere_bourse_categorie': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bourse_categorie'", 'null': 'True', 'to': "orm['sigma.CategorieBourse']"}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Discipline']", 'null': 'True', 'blank': 'True'}),
            'etat': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'experts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'dossiers'", 'blank': 'True', 'to': "orm['sigma.Expert']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moyenne_academique': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'moyenne_votes': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'opportunite_regionale': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'sigma.dossieraccueil': {
            'Meta': {'object_name': 'DossierAccueil'},
            'autre_etablissement_adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_pays': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Pays']", 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dir_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'dir_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dir_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dir_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dir_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'accueil'", 'unique': 'True', 'to': "orm['sigma.Dossier']"}),
            'etablissement': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['managedref.Etablissement']", 'null': 'True', 'blank': 'True'}),
            'faculte_adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'faculte_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'faculte_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'faculte_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'accueil_pays'", 'to_field': "'code'", 'null': 'True', 'to': "orm['managedref.Pays']"}),
            'resp_sc_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'resp_sc_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'sigma.dossiermobilite': {
            'Meta': {'object_name': 'DossierMobilite'},
            'autres_publics': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_debut_accueil': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_debut_origine': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin_accueil': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin_origine': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'diplome_demande_niveau': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'diplome_demande_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Discipline']", 'null': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mobilite'", 'unique': 'True', 'to': "orm['sigma.Dossier']"}),
            'formation_en_cours_diplome': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'formation_en_cours_niveau': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intitule_projet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'mots_clefs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'public_vise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.Public']", 'null': 'True', 'blank': 'True'}),
            'sous_discipline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'these_date_inscription': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'these_soutenance_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'these_soutenance_pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'soutenance_pays'", 'null': 'True', 'to': "orm['managedref.Pays']"}),
            'these_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'type_intervention': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.Intervention']", 'null': 'True', 'blank': 'True'})
        },
        'sigma.dossierorigine': {
            'Meta': {'object_name': 'DossierOrigine'},
            'autre_etablissement_adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_pays': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Pays']", 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'autre_etablissement_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dir_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'dir_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dir_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dir_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dir_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'origine'", 'unique': 'True', 'to': "orm['sigma.Dossier']"}),
            'etablissement': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['managedref.Etablissement']", 'null': 'True', 'blank': 'True'}),
            'faculte_adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'faculte_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'faculte_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'faculte_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'origine_pays'", 'to_field': "'code'", 'null': 'True', 'to': "orm['managedref.Pays']"}),
            'resp_inst_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'resp_inst_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_inst_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_inst_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_inst_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_inst_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_inst_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'resp_sc_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resp_sc_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'sigma.expert': {
            'Meta': {'ordering': "['nom', 'prenom']", 'object_name': 'Expert'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'commentaire': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['managedref.Discipline']", 'null': 'True', 'blank': 'True'}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Etablissement']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['managedref.Region']"})
        },
        'sigma.intervention': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Intervention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sigma.note': {
            'Meta': {'object_name': 'Note'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notes'", 'to': "orm['sigma.Dossier']"}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.Expert']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'sigma.piece': {
            'Meta': {'object_name': 'Piece'},
            'conforme': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pieces'", 'to': "orm['sigma.Dossier']"}),
            'fichier': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'sigma.public': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Public'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sigma.typeconformite': {
            'Meta': {'object_name': 'TypeConformite'},
            'field_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sigma.typepiece': {
            'Meta': {'ordering': "['nom']", 'object_name': 'TypePiece'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sigma.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['managedref.Discipline']", 'null': 'True', 'blank': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['managedref.Region']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"})
        },
        'workflow.workflowcommentaire': {
            'Meta': {'object_name': 'WorkflowCommentaire'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'etat_final': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'etat_initial': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'texte': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sigma']
