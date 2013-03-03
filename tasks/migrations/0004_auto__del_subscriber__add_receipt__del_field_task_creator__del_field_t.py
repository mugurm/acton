# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Subscriber'
        db.delete_table(u'tasks_subscriber')

        # Adding model 'Receipt'
        db.create_table(u'tasks_receipt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks_sent', to=orm['accounts.User'])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks_received', to=orm['accounts.User'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
        ))
        db.send_create_signal(u'tasks', ['Receipt'])

        # Deleting field 'Task.creator'
        db.delete_column(u'tasks_task', 'creator_id')

        # Deleting field 'Task.title'
        db.delete_column(u'tasks_task', 'title')

        # Deleting field 'Task.taken_by'
        db.delete_column(u'tasks_task', 'taken_by_id')

        # Adding field 'Task.sender'
        db.add_column(u'tasks_task', 'sender',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='created_tasks', to=orm['accounts.User']),
                      keep_default=False)

        # Adding field 'Task.accepted_by'
        db.add_column(u'tasks_task', 'accepted_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='taken_tasks', null=True, to=orm['accounts.User']),
                      keep_default=False)

        # Adding field 'Task.can_change'
        db.add_column(u'tasks_task', 'can_change',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Task.can_forward'
        db.add_column(u'tasks_task', 'can_forward',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Removing M2M table for field to_users on 'Task'
        db.delete_table('tasks_task_to_users')

        # Adding M2M table for field involved on 'Task'
        db.create_table(u'tasks_task_involved', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm[u'tasks.task'], null=False)),
            ('user', models.ForeignKey(orm[u'accounts.user'], null=False))
        ))
        db.create_unique(u'tasks_task_involved', ['task_id', 'user_id'])

        # Adding field 'Quote.status'
        db.add_column(u'tasks_quote', 'status',
                      self.gf('django.db.models.fields.CharField')(default='PE', max_length=2),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Subscriber'
        db.create_table(u'tasks_subscriber', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=2)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
        ))
        db.send_create_signal(u'tasks', ['Subscriber'])

        # Deleting model 'Receipt'
        db.delete_table(u'tasks_receipt')


        # User chose to not deal with backwards NULL issues for 'Task.creator'
        raise RuntimeError("Cannot reverse this migration. 'Task.creator' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Task.title'
        raise RuntimeError("Cannot reverse this migration. 'Task.title' and its values cannot be restored.")
        # Adding field 'Task.taken_by'
        db.add_column(u'tasks_task', 'taken_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='taken_tasks', null=True, to=orm['accounts.User'], blank=True),
                      keep_default=False)

        # Deleting field 'Task.sender'
        db.delete_column(u'tasks_task', 'sender_id')

        # Deleting field 'Task.accepted_by'
        db.delete_column(u'tasks_task', 'accepted_by_id')

        # Deleting field 'Task.can_change'
        db.delete_column(u'tasks_task', 'can_change')

        # Deleting field 'Task.can_forward'
        db.delete_column(u'tasks_task', 'can_forward')

        # Adding M2M table for field to_users on 'Task'
        db.create_table(u'tasks_task_to_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm[u'tasks.task'], null=False)),
            ('user', models.ForeignKey(orm[u'accounts.user'], null=False))
        ))
        db.create_unique(u'tasks_task_to_users', ['task_id', 'user_id'])

        # Removing M2M table for field involved on 'Task'
        db.delete_table('tasks_task_involved')

        # Deleting field 'Quote.status'
        db.delete_column(u'tasks_quote', 'status')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'remote_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'tasks.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks_sent'", 'to': u"orm['accounts.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks_received'", 'to': u"orm['accounts.User']"})
        },
        u'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'accepted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taken_tasks'", 'null': 'True', 'to': u"orm['accounts.User']"}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bounty': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'can_change': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_forward': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expire': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'involved': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['accounts.User']", 'symmetrical': 'False'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_tasks'", 'to': u"orm['accounts.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        },
        u'tasks.update': {
            'Meta': {'object_name': 'Update'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'quote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Quote']", 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'update_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        }
    }

    complete_apps = ['tasks']