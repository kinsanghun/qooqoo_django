# Generated by Django 4.0.3 on 2022-08-25 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0018_alter_workstaff_breaktime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='insurance',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
