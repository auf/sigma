# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Appel.date_desactivaition'
        db.delete_column('sigma_appel', 'date_desactivaition')

        # Adding field 'Appel.date_desactivation'
        db.add_column('sigma_appel', 'date_desactivation', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Adding field 'Appel.date_desactivaition'
        db.add_column('sigma_appel', 'date_desactivaition', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Appel.date_desactivation'
        db.delete_column('sigma_appel', 'date_desactivation')
    
    
    models = {
        'sigma.appel': {
            'Meta': {'object_name': 'Appel'},
            'code_budgetaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_activation': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_desactivation': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'etat': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'formulaire_wcs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['sigma']
