# Generated by Django 4.0.5 on 2022-07-15 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_parttimer'),
    ]

    operations = [
        migrations.AddField(
            model_name='parttimer',
            name='pay',
            field=models.IntegerField(default=9150),
            preserve_default=False,
        ),
    ]
