# Generated by Django 4.0.3 on 2022-07-19 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_workparttimer'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkOneday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=30)),
                ('reg_num', models.CharField(max_length=30)),
                ('pay', models.IntegerField()),
                ('content', models.TextField()),
            ],
        ),
    ]