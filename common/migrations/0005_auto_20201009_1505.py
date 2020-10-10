# Generated by Django 3.1.2 on 2020-10-09 10:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20201009_1504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dashboardimage',
            options={'ordering': ['dt_show']},
        ),
        migrations.AlterField(
            model_name='dashboardimage',
            name='dt_show',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
