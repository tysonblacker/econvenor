# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Meeting'
        db.create_table(u'core_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'core', ['Meeting'])

        # Adding model 'Participant'
        db.create_table(u'core_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'core', ['Participant'])

        # Adding model 'Item'
        db.create_table(u'core_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Meeting'])),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('background', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('variety', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('minute_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Item'])

        # Adding model 'Decision'
        db.create_table(u'core_decision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Meeting'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Item'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Decision'])

        # Adding model 'Task'
        db.create_table(u'core_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Meeting'], null=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Item'], null=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Participant'], null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('deadline', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'core', ['Task'])


    def backwards(self, orm):
        # Deleting model 'Meeting'
        db.delete_table(u'core_meeting')

        # Deleting model 'Participant'
        db.delete_table(u'core_participant')

        # Deleting model 'Item'
        db.delete_table(u'core_item')

        # Deleting model 'Decision'
        db.delete_table(u'core_decision')

        # Deleting model 'Task'
        db.delete_table(u'core_task')


    models = {
        u'core.decision': {
            'Meta': {'object_name': 'Decision'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Item']"}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Meeting']"})
        },
        u'core.item': {
            'Meta': {'object_name': 'Item'},
            'background': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Meeting']"}),
            'minute_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'variety': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'core.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {})
        },
        u'core.participant': {
            'Meta': {'object_name': 'Participant'},
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'core.task': {
            'Meta': {'object_name': 'Task'},
            'deadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Item']", 'null': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Meeting']", 'null': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Participant']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['core']