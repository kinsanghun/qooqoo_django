# Generated by Django 4.0.6 on 2022-07-27 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0013_employee_outwork'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaborCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('department', models.CharField(max_length=10)),
                ('rank', models.CharField(max_length=10)),
                ('cost', models.IntegerField()),
            ],
        ),
    ]
