# Generated by Django 2.2.12 on 2020-05-19 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chord', '0015_table_data_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableownership',
            name='service_id',
            field=models.CharField(max_length=200),
        ),
    ]
