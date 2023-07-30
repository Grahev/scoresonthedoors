# Generated by Django 4.0.4 on 2023-06-21 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predicts', '0006_matchresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveLeague',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league_id', models.IntegerField()),
                ('league_name', models.CharField(max_length=100)),
                ('league_logo', models.CharField(max_length=100)),
                ('season', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]