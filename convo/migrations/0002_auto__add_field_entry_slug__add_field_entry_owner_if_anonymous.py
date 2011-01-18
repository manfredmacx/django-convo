# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		
		# Adding field 'Entry.slug'
		db.add_column('convo_entry', 'slug', self.gf('django.db.models.fields.SlugField')(default='FIXME', max_length=250, db_index=True, unique=True), keep_default=False)

		# Adding field 'Entry.owner_if_anonymous'
		db.add_column('convo_entry', 'owner_if_anonymous', self.gf('django.db.models.fields.CharField')(max_length=150, null=True), keep_default=False)
		
		# Adding field 'Entry.owner_if_anonymous'
		db.add_column('convo_entry', 'url_if_anonymous', self.gf('django.db.models.fields.URLField')(max_length=1000, null=True), keep_default=False)

		# Adding field 'Entry.owner_if_anonymous'
		db.add_column('convo_entry', 'published', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)
	
	def backwards(self, orm):
		
		# Deleting field 'Entry.slug'
		db.delete_column('convo_entry', 'slug')
	
		# Deleting field 'Entry.owner_if_anonymous'
		db.delete_column('convo_entry', 'owner_if_anonymous')
	
		# Deleting field 'Entry.owner_if_anonymous'
		db.delete_column('convo_entry', 'url_if_anonymous')
		
		# Deleting field 'Entry.owner_if_anonymous'
		db.delete_column('convo_entry', 'published')
	
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
		'convo.edit': {
			'Meta': {'object_name': 'Edit'},
			'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
			'edit_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
			'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['convo.Entry']"}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
		},
		'convo.entry': {
			'Meta': {'object_name': 'Entry'},
			'body': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
			'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
			'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'level': ('django.db.models.fields.IntegerField', [], {}),
			'original': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orginal_entry'", 'null': 'True', 'to': "orm['convo.Entry']"}),
			'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
			'owner_if_anonymous': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
			'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_entry'", 'null': 'True', 'to': "orm['convo.Entry']"}),
			'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250', 'db_index': 'True'}),
			'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
		}
	}
	
	complete_apps = ['convo']
	
