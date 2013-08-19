# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.real_chips'
        db.add_column('santiago_userprofile', 'real_chips',
                      self.gf('django.db.models.fields.IntegerField')(default=200),
                      keep_default=False)

        # Adding field 'UserProfile.live_chips'
        db.add_column('santiago_userprofile', 'live_chips',
                      self.gf('django.db.models.fields.IntegerField')(default=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.real_chips'
        db.delete_column('santiago_userprofile', 'real_chips')

        # Deleting field 'UserProfile.live_chips'
        db.delete_column('santiago_userprofile', 'live_chips')


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
        'santiago.chippackage': {
            'Meta': {'object_name': 'ChipPackage'},
            'chip_qty': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'santiago.pokertable': {
            'Meta': {'object_name': 'PokerTable', 'db_table': "u'pokertables'"},
            'average_pot': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'betting_structure': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'currency_serial': ('django.db.models.fields.IntegerField', [], {}),
            'hands_per_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'muck_timeout': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'observers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'percent_flop': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'player_timeout': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'players': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'resthost_serial': ('django.db.models.fields.IntegerField', [], {}),
            'seats': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'skin': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'tourney_serial': ('django.db.models.fields.IntegerField', [], {}),
            'variant': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'waiting': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'santiago.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'client_host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'client_ip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'santiago.securityquestion': {
            'Meta': {'object_name': 'SecurityQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'santiago.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_chips': ('django.db.models.fields.IntegerField', [], {}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'pin_delivery': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'real_chips': ('django.db.models.fields.IntegerField', [], {}),
            'security_answer': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'security_question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['santiago.SecurityQuestion']"}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'street1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['santiago']