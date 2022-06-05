# Generated by Django 4.0.4 on 2022-06-05 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams_and_players', '0001_initial'),
        ('predicts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchprediction',
            name='goalScorer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teams_and_players.player'),
        ),
        migrations.AlterField(
            model_name='matchprediction',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='predicts.match'),
        ),
    ]
