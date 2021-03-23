from django.db import models
from card.models import Player
from tournament.models import Tournament


class PlayerTournamentStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    # can a player play multiple games during a tournament?
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
