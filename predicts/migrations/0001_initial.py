# Generated by Django 4.0.4 on 2022-11-08 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams_and_players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchday', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
                ('hTeamScore', models.IntegerField(blank=True, null=True)),
                ('aTeamScore', models.IntegerField(blank=True, null=True)),
                ('match_id', models.IntegerField()),
                ('league', models.CharField(blank=True, max_length=50, null=True)),
                ('aTeam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='teams_and_players.team')),
                ('goalScorers', models.ManyToManyField(blank=True, related_name='goal_scorers', to='teams_and_players.player')),
                ('hTeam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='teams_and_players.team')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='NumberOfGamesToPredict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EPL', models.IntegerField()),
                ('UCL', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MatchPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homeTeamScore', models.PositiveIntegerField()),
                ('awayTeamScore', models.PositiveIntegerField()),
                ('checked', models.BooleanField(default=False)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('goalScorer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teams_and_players.player')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='predicts.match')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MatchEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField()),
                ('type', models.CharField(max_length=50)),
                ('detail', models.CharField(max_length=50)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='events', to='predicts.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teams_and_players.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teams_and_players.team')),
            ],
        ),
    ]
