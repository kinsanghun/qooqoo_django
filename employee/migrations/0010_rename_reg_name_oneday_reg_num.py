# Generated by Django 4.0.3 on 2022-07-19 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_oneday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oneday',
            old_name='reg_name',
            new_name='reg_num',
        ),
    ]
