# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Appel'
        db.create_table('sigma_appel', (
            ('etat', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sigma', ['Appel'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Appel'
        db.delete_table('sigma_appel')
    
    
    models = {
        'sigma.appel': {
            'Meta': {'object_name': 'Appel'},
            'etat': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['sigma']
