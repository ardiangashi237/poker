# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FaqCategory.title'
        db.add_column('faq_faqcategory', 'title',
                      self.gf('django.db.models.fields.CharField')(default='FAQs', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FaqCategory.title'
        db.delete_column('faq_faqcategory', 'title')


    models = {
        'faq.faq': {
            'Meta': {'object_name': 'Faq'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faq.FaqCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sequence': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'faq.faqcategory': {
            'Meta': {'object_name': 'FaqCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'sequence': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "u'djangodbmodelsfieldscharfield'", 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['faq']