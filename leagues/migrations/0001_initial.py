# Generated by Django 4.0.4 on 2022-06-16 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('pin', models.IntegerField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('rules', models.TextField(blank=True, max_length=500)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='league_admin', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='leagues', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
