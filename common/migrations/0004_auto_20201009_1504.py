# Generated by Django 3.1.2 on 2020-10-09 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_dashboardimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardimage',
            name='image',
            field=models.ImageField(upload_to='dashboard'),
        ),
    ]
