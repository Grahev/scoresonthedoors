# Generated by Django 4.0.4 on 2023-09-04 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predicts', '0008_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(verbose_name=range(1, 12))),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
    ]