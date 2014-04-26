# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomerInformation'
        db.create_table(u'customer_customerinformation', (
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('national_number', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('cif', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bc_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('bc_serial_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('birth_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('bc_place', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'customer', ['CustomerInformation'])

        # Adding model 'ContactInformation'
        db.create_table(u'customer_contactinformation', (
            ('customer', self.gf('django.db.models.fields.related.OneToOneField')(related_name='contact_info', unique=True, primary_key=True, to=orm['customer.CustomerInformation'])),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('cell_number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rose_config.Town'])),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rose_config.Province'])),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'customer', ['ContactInformation'])

        # Adding model 'JobInformation'
        db.create_table(u'customer_jobinformation', (
            ('customer', self.gf('django.db.models.fields.related.OneToOneField')(related_name='job_info', unique=True, primary_key=True, to=orm['customer.CustomerInformation'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rose_config.JobType'])),
            ('job_activity', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Job_certificate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rose_config.JobCertificateType'])),
            ('job_certificate_number', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('job_province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rose_config.Province'])),
            ('job_town', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rose_config.Town'])),
            ('job_contact_number', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('job_postal_code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('job_address', self.gf('django.db.models.fields.CharField')(max_length=700)),
        ))
        db.send_create_signal(u'customer', ['JobInformation'])

        # Adding model 'AssetInformation'
        db.create_table(u'customer_assetinformation', (
            ('customer', self.gf('django.db.models.fields.related.OneToOneField')(related_name='asset_info', unique=True, primary_key=True, to=orm['customer.CustomerInformation'])),
            ('cash', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('account', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('business_place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rose_config.BusinessPlace'])),
            ('business_place_value', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('individual_credit_amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('company_credit_amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('manghool_value', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('no_manghool_value', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('vehicles_value', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('individual_debit_amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('company_debit_amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('bank_debit_amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal(u'customer', ['AssetInformation'])

        # Adding model 'SanadMelkiInformation'
        db.create_table(u'customer_sanadmelkiinformation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sanad_no', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('owner_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('current_value', self.gf('django.db.models.fields.BigIntegerField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'customer', ['SanadMelkiInformation'])

        # Adding model 'BankIncomeInformation'
        db.create_table(u'customer_bankincomeinformation', (
            ('customer', self.gf('django.db.models.fields.related.OneToOneField')(related_name='bank_income_info', unique=True, primary_key=True, to=orm['customer.CustomerInformation'])),
            ('income', self.gf('django.db.models.fields.IntegerField')()),
            ('sanad_melki_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customer.SanadMelkiInformation'], null=True, blank=True)),
        ))
        db.send_create_signal(u'customer', ['BankIncomeInformation'])

        # Adding M2M table for field banks on 'BankIncomeInformation'
        m2m_table_name = db.shorten_name(u'customer_bankincomeinformation_banks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bankincomeinformation', models.ForeignKey(orm[u'customer.bankincomeinformation'], null=False)),
            ('bank', models.ForeignKey(orm[u'rose_config.bank'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bankincomeinformation_id', 'bank_id'])

        # Adding M2M table for field vasighe_types on 'BankIncomeInformation'
        m2m_table_name = db.shorten_name(u'customer_bankincomeinformation_vasighe_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bankincomeinformation', models.ForeignKey(orm[u'customer.bankincomeinformation'], null=False)),
            ('vasighetype', models.ForeignKey(orm[u'rose_config.vasighetype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bankincomeinformation_id', 'vasighetype_id'])


    def backwards(self, orm):
        # Deleting model 'CustomerInformation'
        db.delete_table(u'customer_customerinformation')

        # Deleting model 'ContactInformation'
        db.delete_table(u'customer_contactinformation')

        # Deleting model 'JobInformation'
        db.delete_table(u'customer_jobinformation')

        # Deleting model 'AssetInformation'
        db.delete_table(u'customer_assetinformation')

        # Deleting model 'SanadMelkiInformation'
        db.delete_table(u'customer_sanadmelkiinformation')

        # Deleting model 'BankIncomeInformation'
        db.delete_table(u'customer_bankincomeinformation')

        # Removing M2M table for field banks on 'BankIncomeInformation'
        db.delete_table(db.shorten_name(u'customer_bankincomeinformation_banks'))

        # Removing M2M table for field vasighe_types on 'BankIncomeInformation'
        db.delete_table(db.shorten_name(u'customer_bankincomeinformation_vasighe_types'))


    models = {
        u'customer.assetinformation': {
            'Meta': {'object_name': 'AssetInformation'},
            'account': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'bank_debit_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'business_place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.BusinessPlace']"}),
            'business_place_value': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'cash': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'company_credit_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'company_debit_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'asset_info'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['customer.CustomerInformation']"}),
            'individual_credit_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'individual_debit_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'manghool_value': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'no_manghool_value': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'vehicles_value': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'customer.bankincomeinformation': {
            'Meta': {'object_name': 'BankIncomeInformation'},
            'banks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['rose_config.Bank']", 'symmetrical': 'False'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bank_income_info'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['customer.CustomerInformation']"}),
            'income': ('django.db.models.fields.IntegerField', [], {}),
            'sanad_melki_info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customer.SanadMelkiInformation']", 'null': 'True', 'blank': 'True'}),
            'vasighe_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['rose_config.VasigheType']", 'symmetrical': 'False'})
        },
        u'customer.contactinformation': {
            'Meta': {'object_name': 'ContactInformation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'cell_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contact_info'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['customer.CustomerInformation']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.Province']"}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.Town']"})
        },
        u'customer.customerinformation': {
            'Meta': {'object_name': 'CustomerInformation'},
            'bc_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'bc_place': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bc_serial_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'birth_date': ('django.db.models.fields.DateTimeField', [], {}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cif': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'national_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'customer.jobinformation': {
            'Job_certificate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.JobCertificateType']"}),
            'Meta': {'object_name': 'JobInformation'},
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'job_info'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['customer.CustomerInformation']"}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.JobType']"}),
            'job_activity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'job_address': ('django.db.models.fields.CharField', [], {'max_length': '700'}),
            'job_certificate_number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'job_contact_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'job_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'job_province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.Province']"}),
            'job_town': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.Town']"})
        },
        u'customer.sanadmelkiinformation': {
            'Meta': {'object_name': 'SanadMelkiInformation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'current_value': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'sanad_no': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'rose_config.bank': {
            'Meta': {'object_name': 'Bank'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'rose_config.businesspart': {
            'Meta': {'object_name': 'BusinessPart'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'rose_config.businessplace': {
            'Meta': {'object_name': 'BusinessPlace'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'rose_config.jobcertificatetype': {
            'Meta': {'object_name': 'JobCertificateType'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'rose_config.jobtype': {
            'Meta': {'object_name': 'JobType'},
            'business_part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.BusinessPart']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'rose_config.province': {
            'Meta': {'object_name': 'Province'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'rose_config.town': {
            'Meta': {'object_name': 'Town'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rose_config.Province']"})
        },
        u'rose_config.vasighetype': {
            'Meta': {'object_name': 'VasigheType'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['customer']