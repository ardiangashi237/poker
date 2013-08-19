# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RegistrationProfile.facebook_id'
        db.add_column('santiago_registrationprofile', 'facebook_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RegistrationProfile.facebook_id'
        db.delete_column('santiago_registrationprofile', 'facebook_id')


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
        'santiago.buyin': {
            'Meta': {'object_name': 'BuyIn'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_chips': ('django.db.models.fields.IntegerField', [], {}),
            'real_chips': ('django.db.models.fields.IntegerField', [], {}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['santiago.PokerTable']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'santiago.chippackage': {
            'Meta': {'object_name': 'ChipPackage'},
            'chip_qty': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'santiago.chiptransaction': {
            'Meta': {'object_name': 'ChipTransaction'},
            'bank_chips': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiating_tx_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'real_chips': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'santiago.membershiplevel': {
            'Meta': {'object_name': 'MembershipLevel'},
            'ad_required_for_top_up': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_chip_purchases': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'daily_top_up_threshold': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly_award': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'signup_award': ('django.db.models.fields.IntegerField', [], {'default': '200'})
        },
        'santiago.pokernetchipcount': {
            'Meta': {'object_name': 'PokernetChipCount', 'db_table': "u'user2money'"},
            'amount': ('django.db.models.fields.BigIntegerField', [], {}),
            'currency_serial': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.BigIntegerField', [], {}),
            'rake': ('django.db.models.fields.BigIntegerField', [], {}),
            'user_serial': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'santiago.pokernetuser': {
            'Meta': {'object_name': 'PokernetUser', 'db_table': "u'users'"},
            'affiliate': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'future_rating': ('django.db.models.fields.FloatField', [], {}),
            'games_count': ('django.db.models.fields.IntegerField', [], {}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '192'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'privilege': ('django.db.models.fields.IntegerField', [], {}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'serial': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skin_image': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'skin_image_type': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'}),
            'skin_outfit': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'skin_url': ('django.db.models.fields.CharField', [], {'max_length': '765'})
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
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined_via_fb': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'santiago.registrationprofileverification': {
            'Meta': {'object_name': 'RegistrationProfileVerification'},
            'client_host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'client_ip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_profile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'verification'", 'unique': 'True', 'to': "orm['santiago.RegistrationProfile']"}),
            'verified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'santiago.securityquestion': {
            'Meta': {'object_name': 'SecurityQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'santiago.userchipcount': {
            'Meta': {'object_name': 'UserChipCount'},
            'bank_chips': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_chips': ('django.db.models.fields.IntegerField', [], {}),
            'real_chips': ('django.db.models.fields.IntegerField', [], {}),
            'serial': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        'santiago.usermembershiplevelhistory': {
            'Meta': {'object_name': 'UserMembershipLevelHistory'},
            'effective_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['santiago.MembershipLevel']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'santiago.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'current_member_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['santiago.MembershipLevel']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'pin_delivery': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'security_answer': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'security_question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['santiago.SecurityQuestion']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'street1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['santiago']