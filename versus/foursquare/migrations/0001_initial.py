# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('foursquare_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_checkin_update', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('foursquare', ['UserProfile'])

        # Adding model 'Venue'
        db.create_table('foursquare_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fsq_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('foursquare', ['Venue'])

        # Adding model 'Checkin'
        db.create_table('foursquare_checkin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fsq_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foursquare.UserProfile'])),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foursquare.Venue'])),
        ))
        db.send_create_signal('foursquare', ['Checkin'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('foursquare_userprofile')

        # Deleting model 'Venue'
        db.delete_table('foursquare_venue')

        # Deleting model 'Checkin'
        db.delete_table('foursquare_checkin')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'foursquare.checkin': {
            'Meta': {'object_name': 'Checkin'},
            'fsq_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['foursquare.UserProfile']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['foursquare.Venue']"})
        },
        'foursquare.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checkin_update': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'visited_venues': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['foursquare.Venue']", 'through': "orm['foursquare.Checkin']", 'symmetrical': 'False'})
        },
        'foursquare.venue': {
            'Meta': {'object_name': 'Venue'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'fsq_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'visitors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['foursquare.UserProfile']", 'through': "orm['foursquare.Checkin']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['foursquare']
