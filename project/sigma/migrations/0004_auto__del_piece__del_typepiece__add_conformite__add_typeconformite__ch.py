# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting model 'Piece'
        db.delete_table('sigma_piece')

        # Deleting model 'TypePiece'
        db.delete_table('sigma_typepiece')

        # Adding model 'Conformite'
        db.create_table('sigma_conformite', (
            ('dossier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Dossier'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.TypeConformite'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('conforme', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('sigma', ['Conformite'])

        # Adding model 'TypeConformite'
        db.create_table('sigma_typeconformite', (
            ('field_type', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('sigma', ['TypeConformite'])

        # Changing field 'DossierOrigine.dossier'
        db.alter_column('sigma_dossierorigine', 'dossier_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['sigma.Dossier']))

        # Adding unique constraint on 'DossierOrigine', fields ['dossier']
        db.create_unique('sigma_dossierorigine', ['dossier_id'])

        # Changing field 'DossierAccueil.dossier'
        db.alter_column('sigma_dossieraccueil', 'dossier_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['sigma.Dossier']))

        # Adding unique constraint on 'DossierAccueil', fields ['dossier']
        db.create_unique('sigma_dossieraccueil', ['dossier_id'])

        # Renaming column for 'Expert.region' to match new field type.
        db.rename_column('sigma_expert', 'region', 'region_id')
        # Changing field 'Expert.region'
        db.alter_column('sigma_expert', 'region_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datamaster_modeles.Region']))

        # Adding index on 'Expert', fields ['region']
        db.create_index('sigma_expert', ['region_id'])

        # Deleting field 'Candidat.sexe'
        db.delete_column('sigma_candidat', 'sexe')

        # Adding field 'Candidat.genre'
        db.add_column('sigma_candidat', 'genre', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True), keep_default=False)

        # Changing field 'Candidat.dossier'
        db.alter_column('sigma_candidat', 'dossier_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['sigma.Dossier']))

        # Adding unique constraint on 'Candidat', fields ['dossier']
        db.create_unique('sigma_candidat', ['dossier_id'])

        # Deleting field 'Appel.date_fin'
        db.delete_column('sigma_appel', 'date_fin')

        # Deleting field 'Appel.date_debut'
        db.delete_column('sigma_appel', 'date_debut')

        # Adding field 'Appel.date_fin_appel'
        db.add_column('sigma_appel', 'date_fin_appel', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Appel.date_debut_appel'
        db.add_column('sigma_appel', 'date_debut_appel', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Appel.date_debut_mobilite'
        db.add_column('sigma_appel', 'date_debut_mobilite', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Appel.date_fin_mobilite'
        db.add_column('sigma_appel', 'date_fin_mobilite', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding M2M table for field conformites on 'Appel'
        db.create_table('sigma_appel_conformites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('appel', models.ForeignKey(orm['sigma.appel'], null=False)),
            ('typeconformite', models.ForeignKey(orm['sigma.typeconformite'], null=False))
        ))
        db.create_unique('sigma_appel_conformites', ['appel_id', 'typeconformite_id'])
    
    
    def backwards(self, orm):
        
        # Adding model 'Piece'
        db.create_table('sigma_piece', (
            ('dossier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Dossier'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.TypePiece'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conforme', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('sigma', ['Piece'])

        # Adding model 'TypePiece'
        db.create_table('sigma_typepiece', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['TypePiece'])

        # Deleting model 'Conformite'
        db.delete_table('sigma_conformite')

        # Deleting model 'TypeConformite'
        db.delete_table('sigma_typeconformite')

        # Changing field 'DossierOrigine.dossier'
        db.alter_column('sigma_dossierorigine', 'dossier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Dossier']))

        # Removing unique constraint on 'DossierOrigine', fields ['dossier']
        db.delete_unique('sigma_dossierorigine', ['dossier_id'])

        # Changing field 'DossierAccueil.dossier'
        db.alter_column('sigma_dossieraccueil', 'dossier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Dossier']))

        # Removing unique constraint on 'DossierAccueil', fields ['dossier']
        db.delete_unique('sigma_dossieraccueil', ['dossier_id'])

        # Renaming column for 'Expert.region' to match new field type.
        db.rename_column('sigma_expert', 'region_id', 'region')
        # Changing field 'Expert.region'
        db.alter_column('sigma_expert', 'region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True))

        # Removing index on 'Expert', fields ['region']
        db.delete_index('sigma_expert', ['region_id'])

        # Adding field 'Candidat.sexe'
        db.add_column('sigma_candidat', 'sexe', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True), keep_default=False)

        # Deleting field 'Candidat.genre'
        db.delete_column('sigma_candidat', 'genre')

        # Changing field 'Candidat.dossier'
        db.alter_column('sigma_candidat', 'dossier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sigma.Dossier']))

        # Removing unique constraint on 'Candidat', fields ['dossier']
        db.delete_unique('sigma_candidat', ['dossier_id'])

        # Adding field 'Appel.date_fin'
        db.add_column('sigma_appel', 'date_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Appel.date_debut'
        db.add_column('sigma_appel', 'date_debut', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Appel.date_fin_appel'
        db.delete_column('sigma_appel', 'date_fin_appel')

        # Deleting field 'Appel.date_debut_appel'
        db.delete_column('sigma_appel', 'date_debut_appel')

        # Deleting field 'Appel.date_debut_mobilite'
        db.delete_column('sigma_appel', 'date_debut_mobilite')

        # Deleting field 'Appel.date_fin_mobilite'
        db.delete_column('sigma_appel', 'date_fin_mobilite')

        # Removing M2M table for field conformites on 'Appel'
        db.delete_table('sigma_appel_conformites')
    
    
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
