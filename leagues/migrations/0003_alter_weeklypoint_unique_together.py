# Generated by Django 4.0.4 on 2023-06-12 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0002_weeklypoint_monthlypoint'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='weeklypoint',
            unique_together=set(),
        ),
    ]