# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Appel.code_budgetaire'
        db.add_column('sigma_appel', 'code_budgetaire', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Appel.formulaire_wcs'
        db.add_column('sigma_appel', 'formulaire_wcs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Appel.date_desactivaition'
        db.add_column('sigma_appel', 'date_desactivaition', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Appel.date_debut'
        db.add_column('sigma_appel', 'date_debut', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Appel.date_fin'
        db.add_column('sigma_appel', 'date_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Appel.date_activation'
        db.add_column('sigma_appel', 'date_activation', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Changing field 'Appel.nom'
        db.alter_column('sigma_appel', 'nom', self.gf('django.db.models.fields.CharField')(max_length=255))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Appel.code_budgetaire'
        db.delete_column('sigma_appel', 'code_budgetaire')

        # Deleting field 'Appel.formulaire_wcs'
        db.delete_column('sigma_appel', 'formulaire_wcs')

        # Deleting field 'Appel.date_desactivaition'
        db.delete_column('sigma_appel', 'date_desactivaition')

        # Deleting field 'Appel.date_debut'
        db.delete_column('sigma_appel', 'date_debut')

        # Deleting field 'Appel.date_fin'
        db.delete_column('sigma_appel', 'date_fin')

        # Deleting field 'Appel.date_activation'
        db.delete_column('sigma_appel', 'date_activation')

        # Changing field 'Appel.nom'
        db.alter_column('sigma_appel', 'nom', self.gf('django.db.models.fields.CharField')(max_length=200))
    
    
    models = {
        'sigma.appel': {
            'Meta': {'object_name': 'Appel'},
            'code_budgetaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_activation': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_desactivaition': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'etat': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'formulaire_wcs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['sigma']
