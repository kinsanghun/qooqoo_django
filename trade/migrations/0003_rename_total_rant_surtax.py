# Generated by Django 4.0.5 on 2022-06-19 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_etc_rant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rant',
            old_name='total',
            new_name='surtax',
        ),
    ]
