# Generated by Django 2.0.5 on 2018-08-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loansApp', '0003_auto_20180817_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='state',
            field=models.CharField(choices=[('V', 'Vigente'), ('C', 'Caducados'), ('P', 'Perdidos')], max_length=1),
        ),
    ]
