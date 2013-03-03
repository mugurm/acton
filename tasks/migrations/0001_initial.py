# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'tasks_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_tasks', to=orm['accounts.User'])),
            ('taken_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taken_tasks', to=orm['accounts.User'])),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('expire', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('bounty', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tasks', ['Task'])

        # Adding model 'Update'
        db.create_table(u'tasks_update', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('update_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('quote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Quote'], null=True, blank=True)),
        ))
        db.send_create_signal(u'tasks', ['Update'])

        # Adding model 'Quote'
        db.create_table(u'tasks_quote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('deliver_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'tasks', ['Quote'])

        # Adding model 'Subscriber'
        db.create_table(u'tasks_subscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'tasks', ['Subscriber'])

        # Adding model 'Attachment'
        db.create_table(u'tasks_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'tasks', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table(u'tasks_task')

        # Deleting model 'Update'
        db.delete_table(u'tasks_update')

        # Deleting model 'Quote'
        db.delete_table(u'tasks_quote')

        # Deleting model 'Subscriber'
        db.delete_table(u'tasks_subscriber')

        # Deleting model 'Attachment'
        db.delete_table(u'tasks_attachment')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'remote_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tasks.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        u'tasks.quote': {
            'Meta': {'object_name': 'Quote'},
            'deliver_date': ('django.db.models.fields.DateTimeField', [], {}),
            'details': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'tasks.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bounty': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_tasks'", 'to': u"orm['accounts.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expire': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'taken_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taken_tasks'", 'to': u"orm['accounts.User']"}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'tasks.update': {
            'Meta': {'object_name': 'Update'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'quote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Quote']", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'update_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        }
    }

    complete_apps = ['tasks']