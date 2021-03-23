from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Player(models.Model):
    # Be careful of homonymy
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PlayerCard(models.Model):
    """
    Users have Player Cards that represent a football player.
    There can be multiple Player Cards of the same player.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    bonus = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.player} – {self.bonus}"
