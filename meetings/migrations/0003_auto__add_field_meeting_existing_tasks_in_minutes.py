# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Meeting.existing_tasks_in_minutes'
        db.add_column(u'meetings_meeting', 'existing_tasks_in_minutes',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Meeting.existing_tasks_in_minutes'
        db.delete_column(u'meetings_meeting', 'existing_tasks_in_minutes')


    models = {
        u'accounts.group': {
            'Meta': {'object_name': 'Group'},
            'account_status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '20', 'blank': 'True'}),
            'account_type': ('django.db.models.fields.CharField', [], {'default': "'Free'", 'max_length': '20', 'blank': 'True'}),
            'aim': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'focus': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'meetings.distributionrecord': {
            'Meta': {'object_name': 'DistributionRecord'},
            'covering_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distribution_list': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'doc_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetings.Meeting']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'meetings.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'agenda_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'apologies': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'attendance': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_agenda_version': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'current_minutes_version': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_actual': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_scheduled': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_time_actual': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'existing_tasks_in_minutes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facilitator_actual': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'facilitator_act'", 'null': 'True', 'to': u"orm['participants.Participant']"}),
            'facilitator_scheduled': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'facilitator_sch'", 'null': 'True', 'to': u"orm['participants.Participant']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions_actual': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'instructions_scheduled': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'location_actual': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'location_scheduled': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meeting_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meeting_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'meeting_status': ('django.db.models.fields.CharField', [], {'default': "'Scheduled'", 'max_length': '30', 'blank': 'True'}),
            'meeting_type': ('django.db.models.fields.CharField', [], {'default': "'Ordinary Meeting'", 'max_length': '30', 'blank': 'True'}),
            'minute_taker_actual': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'minutetaker_act'", 'null': 'True', 'to': u"orm['participants.Participant']"}),
            'minute_taker_scheduled': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'minutetaker_sch'", 'null': 'True', 'to': u"orm['participants.Participant']"}),
            'minutes_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'next_meeting_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'next_meeting_facilitator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'facilitator_next'", 'null': 'True', 'to': u"orm['participants.Participant']"}),
            'next_meeting_instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'next_meeting_location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'next_meeting_minute_taker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'minutetaker_next'", 'null': 'True', 'to': u"orm['participants.Participant']"}),
            'next_meeting_start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'reminder_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'start_time_actual': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'start_time_scheduled': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'participants.participant': {
            'Meta': {'object_name': 'Participant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'reminders': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['meetings']