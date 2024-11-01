# Generated by Django 5.0.6 on 2024-08-21 05:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GameResult', '0001_initial'),
        ('GameSession', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresult',
            name='game_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='GameSession.gamesession'),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_games', to='GameSession.participant'),
        ),
    ]
