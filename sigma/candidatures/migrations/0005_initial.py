# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Expert'
        db.create_table('sigma_expert', (
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('prenom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('commentaire', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Region'])),
            ('etablissement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Etablissement'], null=True, blank=True)),
            ('courriel', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('actif', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['Expert'])

        # Adding M2M table for field dossiers on 'Expert'
        db.create_table('sigma_expert_dossiers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('expert', models.ForeignKey(orm['sigma.expert'], null=False)),
            ('dossier', models.ForeignKey(orm['sigma.dossier'], null=False))
        ))
        db.create_unique('sigma_expert_dossiers', ['expert_id', 'dossier_id'])

        # Adding M2M table for field disciplines on 'Expert'
        db.create_table('sigma_expert_disciplines', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('expert', models.ForeignKey(orm['sigma.expert'], null=False)),
            ('discipline', models.ForeignKey(orm['datamaster_modeles.discipline'], null=False))
        ))
        db.create_unique('sigma_expert_disciplines', ['expert_id', 'discipline_id'])

        # Adding model 'UserProfile'
        db.create_table('sigma_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('sigma', ['UserProfile'])

        # Adding M2M table for field disciplines on 'UserProfile'
        db.create_table('sigma_userprofile_disciplines', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['sigma.userprofile'], null=False)),
            ('discipline', models.ForeignKey(orm['datamaster_modeles.discipline'], null=False))
        ))
        db.create_unique('sigma_userprofile_disciplines', ['userprofile_id', 'discipline_id'])

        # Adding model 'Appel'
        db.create_table('sigma_appel', (
            ('etat', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code_budgetaire', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('formulaire_wcs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Region'])),
            ('date_fin_appel', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_debut_appel', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_desactivation', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_activation', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_debut_mobilite', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_fin_mobilite', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['Appel'])

        # Adding M2M table for field conformites on 'Appel'
        db.create_table('sigma_appel_conformites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('appel', models.ForeignKey(orm['sigma.appel'], null=False)),
            ('typeconformite', models.ForeignKey(orm['sigma.typeconformite'], null=False))
        ))
        db.create_unique('sigma_appel_conformites', ['appel_id', 'typeconformite_id'])

        # Adding model 'Candidat'
        db.create_table('sigma_candidat', (
            ('ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pays', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pays', null=True, to=orm['datamaster_modeles.Pays'])),
            ('naissance_date', self.gf('django.db.models.fields.DateField')(max_length=255, null=True, blank=True)),
            ('courriel_perso', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('telephone_pro', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom_jeune_fille', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('courriel_pro', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_modification', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nationalite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Pays'], null=True, blank=True)),
            ('adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('genre', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('date_creation', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('telephone_perso', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('prenom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dossier', self.gf('django.db.models.fields.related.OneToOneField')(related_name='candidat', unique=True, to=orm['sigma.Dossier'])),
            ('naissance_pays', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='naissance_pays', null=True, to=orm['datamaster_modeles.Pays'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('fax_pro', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('naissance_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('fax_perso', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('sigma', ['Candidat'])

        # Adding model 'CategorieBourse'
        db.create_table('sigma_categoriebourse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['CategorieBourse'])

        # Adding model 'NiveauEtude'
        db.create_table('sigma_niveauetude', (
            ('annees', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['NiveauEtude'])

        # Adding model 'Note'
        db.create_table('sigma_note', (
            ('dossier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notes', to=orm['sigma.Dossier'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('note', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Expert'])),
        ))
        db.send_create_signal('sigma', ['Note'])

        # Adding model 'Commentaire'
        db.create_table('sigma_commentaire', (
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('texte', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('sigma', ['Commentaire'])

        # Adding model 'Dossier'
        db.create_table('sigma_dossier', (
            ('etat', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('moyenne_academique', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('opportunite_regionale', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('derniere_bourse_categorie', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bourse_categorie', null=True, to=orm['sigma.CategorieBourse'])),
            ('candidat_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dernier_projet_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('moyenne_votes', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('dernier_projet_annee', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('appel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='appel', to=orm['sigma.Appel'])),
            ('discipline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Discipline'], null=True, blank=True)),
            ('bureau_rattachement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Bureau'], null=True, blank=True)),
            ('candidat_statut', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('derniere_bourse_annee', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['Dossier'])

        # Adding M2M table for field annotations on 'Dossier'
        db.create_table('sigma_dossier_annotations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dossier', models.ForeignKey(orm['sigma.dossier'], null=False)),
            ('commentaire', models.ForeignKey(orm['sigma.commentaire'], null=False))
        ))
        db.create_unique('sigma_dossier_annotations', ['dossier_id', 'commentaire_id'])

        # Adding model 'DossierOrigine'
        db.create_table('sigma_dossierorigine', (
            ('resp_inst_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_pays', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Pays'], null=True, blank=True)),
            ('resp_inst_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resp_sc_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_inst_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_inst_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('resp_inst_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_erreur', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_inst_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('autre_etablissement_valide', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('resp_inst_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dossier', self.gf('django.db.models.fields.related.OneToOneField')(related_name='origine', unique=True, to=orm['sigma.Dossier'])),
            ('etablissement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Etablissement'], null=True, blank=True)),
            ('resp_sc_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('sigma', ['DossierOrigine'])

        # Adding model 'DossierAccueil'
        db.create_table('sigma_dossieraccueil', (
            ('resp_inst_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_pays', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Pays'], null=True, blank=True)),
            ('resp_inst_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resp_sc_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_inst_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_inst_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('resp_inst_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_adresse', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_erreur', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_ville', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_inst_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('autre_etablissement_valide', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('resp_inst_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autre_etablissement_code_postal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_courriel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('faculte_fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dossier', self.gf('django.db.models.fields.related.OneToOneField')(related_name='accueil', unique=True, to=orm['sigma.Dossier'])),
            ('etablissement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Etablissement'], null=True, blank=True)),
            ('resp_sc_fonction', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resp_sc_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('sigma', ['DossierAccueil'])

        # Adding model 'Public'
        db.create_table('sigma_public', (
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['Public'])

        # Adding model 'Intervention'
        db.create_table('sigma_intervention', (
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['Intervention'])

        # Adding model 'DossierMobilite'
        db.create_table('sigma_dossiermobilite', (
            ('intitule_projet', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type_intervention', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Intervention'], null=True, blank=True)),
            ('diplome_demande_niveau', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='diplome_demande_niveau', null=True, to=orm['sigma.NiveauEtude'])),
            ('dir_ori_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dir_acc_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sous_discipline', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('autres_publics', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dir_ori_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alternance_accueil_puis_origine', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('alternance_nb_mois_accueil', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('diplome_demande_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('discipline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Discipline'], null=True, blank=True)),
            ('mots_clefs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_debut', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('formation_en_cours_diplome', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('alternance_nb_mois_origine', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('these_soutenance_pays', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='soutenance_pays', null=True, to=orm['datamaster_modeles.Pays'])),
            ('these_date_obtention_prevue', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('public_vise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Public'], null=True, blank=True)),
            ('dir_acc_civilite', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('duree', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dir_acc_prenom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('these_type_autre', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('these_date_inscription', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('these_soutenance_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('formation_en_cours_niveau', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='formation_en_cours_niveau', null=True, to=orm['sigma.NiveauEtude'])),
            ('dossier', self.gf('django.db.models.fields.related.OneToOneField')(related_name='mobilite', unique=True, to=orm['sigma.Dossier'])),
            ('these_type', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('dir_ori_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('sigma', ['DossierMobilite'])

        # Adding model 'Diplome'
        db.create_table('sigma_diplome', (
            ('etablissement_nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dossier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Dossier'])),
            ('niveau', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='niveau', null=True, to=orm['sigma.NiveauEtude'])),
            ('date', self.gf('django.db.models.fields.DateField')(max_length=255, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('etablissement_pays', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='etablissement_pays', null=True, to=orm['datamaster_modeles.Pays'])),
        ))
        db.send_create_signal('sigma', ['Diplome'])

        # Adding model 'GroupeRegional'
        db.create_table('sigma_grouperegional', (
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Region'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['GroupeRegional'])

        # Adding M2M table for field users on 'GroupeRegional'
        db.create_table('sigma_grouperegional_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('grouperegional', models.ForeignKey(orm['sigma.grouperegional'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('sigma_grouperegional_users', ['grouperegional_id', 'user_id'])

        # Adding model 'TypeConformite'
        db.create_table('sigma_typeconformite', (
            ('field_type', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('sigma', ['TypeConformite'])

        # Adding model 'Conformite'
        db.create_table('sigma_conformite', (
            ('dossier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Dossier'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.TypeConformite'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('conforme', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('sigma', ['Conformite'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Expert'
        db.delete_table('sigma_expert')

        # Removing M2M table for field dossiers on 'Expert'
        db.delete_table('sigma_expert_dossiers')

        # Removing M2M table for field disciplines on 'Expert'
        db.delete_table('sigma_expert_disciplines')

        # Deleting model 'UserProfile'
        db.delete_table('sigma_userprofile')

        # Removing M2M table for field disciplines on 'UserProfile'
        db.delete_table('sigma_userprofile_disciplines')

        # Deleting model 'Appel'
        db.delete_table('sigma_appel')

        # Removing M2M table for field conformites on 'Appel'
        db.delete_table('sigma_appel_conformites')

        # Deleting model 'Candidat'
        db.delete_table('sigma_candidat')

        # Deleting model 'CategorieBourse'
        db.delete_table('sigma_categoriebourse')

        # Deleting model 'NiveauEtude'
        db.delete_table('sigma_niveauetude')

        # Deleting model 'Note'
        db.delete_table('sigma_note')

        # Deleting model 'Commentaire'
        db.delete_table('sigma_commentaire')

        # Deleting model 'Dossier'
        db.delete_table('sigma_dossier')

        # Removing M2M table for field annotations on 'Dossier'
        db.delete_table('sigma_dossier_annotations')

        # Deleting model 'DossierOrigine'
        db.delete_table('sigma_dossierorigine')

        # Deleting model 'DossierAccueil'
        db.delete_table('sigma_dossieraccueil')

        # Deleting model 'Public'
        db.delete_table('sigma_public')

        # Deleting model 'Intervention'
        db.delete_table('sigma_intervention')

        # Deleting model 'DossierMobilite'
        db.delete_table('sigma_dossiermobilite')

        # Deleting model 'Diplome'
        db.delete_table('sigma_diplome')

        # Deleting model 'GroupeRegional'
        db.delete_table('sigma_grouperegional')

        # Removing M2M table for field users on 'GroupeRegional'
        db.delete_table('sigma_grouperegional_users')

        # Deleting model 'TypeConformite'
        db.delete_table('sigma_typeconformite')

        # Deleting model 'Conformite'
        db.delete_table('sigma_conformite')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datamaster_modeles.bureau': {
            'Meta': {'object_name': 'Bureau', 'db_table': "u'ref_bureau'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Implantation']", 'db_column': "'implantation'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"})
        },
        'datamaster_modeles.discipline': {
            'Meta': {'object_name': 'Discipline', 'db_table': "u'ref_discipline'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'datamaster_modeles.etablissement': {
            'Meta': {'object_name': 'Etablissement', 'db_table': "u'ref_etablissement'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cedex': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'code_implantation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'code_gere_etablissement'", 'to_field': "'code'", 'db_column': "'code_implantation'", 'to': "orm['datamaster_modeles.Implantation']"}),
            'code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gere_etablissement'", 'db_column': "'implantation'", 'to': "orm['datamaster_modeles.Implantation']"}),
            'membre': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'membre_adhesion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Pays']", 'to_field': "'code'", 'db_column': "'pays'"}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"}),
            'responsable_genre': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'responsable_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'responsable_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'datamaster_modeles.implantation': {
            'Meta': {'object_name': 'Implantation', 'db_table': "u'ref_implantation'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'adresse_physique_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'adresse_physique_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_physique'", 'to_field': "'code'", 'db_column': "'adresse_physique_pays'", 'to': "orm['datamaster_modeles.Pays']"}),
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
            'adresse_postale_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_postale'", 'to_field': "'code'", 'db_column': "'adresse_postale_pays'", 'to': "orm['datamaster_modeles.Pays']"}),
            'adresse_postale_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bureau_rattachement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Implantation']", 'db_column': "'bureau_rattachement'"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
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
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'modif_date': ('django.db.models.fields.DateField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"}),
            'remarque': ('django.db.models.fields.TextField', [], {}),
            'responsable_implantation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'statut': ('django.db.models.fields.IntegerField', [], {}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'datamaster_modeles.pays': {
            'Meta': {'object_name': 'Pays', 'db_table': "u'ref_pays'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'code_bureau': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Bureau']", 'to_field': "'code'", 'db_column': "'code_bureau'"}),
            'code_iso3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3', 'blank': 'True'}),
            'developpement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'monnaie': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nord_sud': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"})
        },
        'datamaster_modeles.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'ref_region'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'implantation_bureau': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gere_region'", 'db_column': "'implantation_bureau'", 'to': "orm['datamaster_modeles.Implantation']"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sigma.appel': {
            'Meta': {'object_name': 'Appel'},
            'code_budgetaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'conformites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sigma.TypeConformite']", 'null': 'True', 'blank': 'True'}),
            'date_activation': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_debut_appel': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_debut_mobilite': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_desactivation': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin_appel': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin_mobilite': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'etat': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'formulaire_wcs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']"})
        },
        'sigma.candidat': {
            'Meta': {'object_name': 'Candidat'},
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'courriel_perso': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'courriel_pro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_creation': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'candidat'", 'unique': 'True', 'to': "orm['sigma.Dossier']"}),
            'fax_perso': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fax_pro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naissance_date': ('django.db.models.fields.DateField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'naissance_pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'naissance_pays'", 'null': 'True', 'to': "orm['datamaster_modeles.Pays']"}),
            'naissance_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nationalite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Pays']", 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_jeune_fille': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pays'", 'null': 'True', 'to': "orm['datamaster_modeles.Pays']"}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telephone_perso': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telephone_pro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'date': ('django.db.models.fields.DateField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.Dossier']"}),
            'etablissement_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'etablissement_pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'etablissement_pays'", 'null': 'True', 'to': "orm['datamaster_modeles.Pays']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niveau': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'niveau'", 'null': 'True', 'to': "orm['sigma.NiveauEtude']"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'sigma.dossier': {
            'Meta': {'object_name': 'Dossier'},
            'annotations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sigma.Commentaire']", 'null': 'True', 'blank': 'True'}),
            'appel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appel'", 'to': "orm['sigma.Appel']"}),
            'bureau_rattachement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Bureau']", 'null': 'True', 'blank': 'True'}),
            'candidat_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'candidat_statut': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dernier_projet_annee': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'dernier_projet_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'derniere_bourse_annee': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'derniere_bourse_categorie': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bourse_categorie'", 'null': 'True', 'to': "orm['sigma.CategorieBourse']"}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Discipline']", 'null': 'True', 'blank': 'True'}),
            'etat': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moyenne_academique': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'moyenne_votes': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'opportunite_regionale': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'sigma.dossieraccueil': {
            'Meta': {'object_name': 'DossierAccueil'},
            'autre_etablissement_adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_erreur': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_pays': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Pays']", 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_valide': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'autre_etablissement_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'accueil'", 'unique': 'True', 'to': "orm['sigma.Dossier']"}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Etablissement']", 'null': 'True', 'blank': 'True'}),
            'faculte_adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resp_inst_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'resp_inst_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'resp_sc_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'sigma.dossiermobilite': {
            'Meta': {'object_name': 'DossierMobilite'},
            'alternance_accueil_puis_origine': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'alternance_nb_mois_accueil': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'alternance_nb_mois_origine': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'autres_publics': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'diplome_demande_niveau': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'diplome_demande_niveau'", 'null': 'True', 'to': "orm['sigma.NiveauEtude']"}),
            'diplome_demande_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dir_acc_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'dir_acc_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dir_acc_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dir_ori_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'dir_ori_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dir_ori_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Discipline']", 'null': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mobilite'", 'unique': 'True', 'to': "orm['sigma.Dossier']"}),
            'duree': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'formation_en_cours_diplome': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'formation_en_cours_niveau': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'formation_en_cours_niveau'", 'null': 'True', 'to': "orm['sigma.NiveauEtude']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intitule_projet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mots_clefs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'public_vise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.Public']", 'null': 'True', 'blank': 'True'}),
            'sous_discipline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'these_date_inscription': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'these_date_obtention_prevue': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'these_soutenance_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'these_soutenance_pays': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'soutenance_pays'", 'null': 'True', 'to': "orm['datamaster_modeles.Pays']"}),
            'these_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'these_type_autre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type_intervention': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sigma.Intervention']", 'null': 'True', 'blank': 'True'})
        },
        'sigma.dossierorigine': {
            'Meta': {'object_name': 'DossierOrigine'},
            'autre_etablissement_adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_erreur': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_pays': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Pays']", 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autre_etablissement_valide': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'autre_etablissement_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dossier': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'origine'", 'unique': 'True', 'to': "orm['sigma.Dossier']"}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Etablissement']", 'null': 'True', 'blank': 'True'}),
            'faculte_adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'faculte_ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resp_inst_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'resp_inst_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_inst_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_civilite': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'resp_sc_courriel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resp_sc_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'sigma.expert': {
            'Meta': {'object_name': 'Expert'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['datamaster_modeles.Discipline']", 'null': 'True', 'blank': 'True'}),
            'dossiers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'experts'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sigma.Dossier']"}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Etablissement']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']"})
        },
        'sigma.grouperegional': {
            'Meta': {'object_name': 'GroupeRegional'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groupes_regionaux'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'sigma.intervention': {
            'Meta': {'object_name': 'Intervention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sigma.niveauetude': {
            'Meta': {'object_name': 'NiveauEtude'},
            'annees': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
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
        'sigma.public': {
            'Meta': {'object_name': 'Public'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sigma.typeconformite': {
            'Meta': {'object_name': 'TypeConformite'},
            'field_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sigma.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['datamaster_modeles.Discipline']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
