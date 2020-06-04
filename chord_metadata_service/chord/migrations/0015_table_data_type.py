# Generated by Django 2.2.12 on 2020-05-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chord', '0014_remove_table_data_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='data_type',
            field=models.CharField(choices=[('experiment', 'experiment'), ('phenopacket', 'phenopacket')], default='phenopacket', max_length=30),
            preserve_default=False,
        ),
    ]
