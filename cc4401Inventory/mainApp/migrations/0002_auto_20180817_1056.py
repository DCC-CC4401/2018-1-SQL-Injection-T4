# Generated by Django 2.0.5 on 2018-08-17 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['pk'], 'verbose_name_plural': 'Usuarios'},
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='static/img/avatars/'),
        ),
    ]
